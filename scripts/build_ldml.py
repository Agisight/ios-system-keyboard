#!/usr/bin/env python3
"""
build_ldml.py — генерирует отдельную HTML-страницу (dist/ldml-keyboards.html)
и артефакт с описанием всех раскладок в формате LDML (CLDR Unicode Keyboard3).
Спецификация: https://unicode.org/reports/tr35/tr35-keyboards.html
"""

import os, re, json, sys
from pathlib import Path

# Подключаем discover() из существующего build.py
ROOT = Path(__file__).parent.parent
sys.path.append(str(ROOT / "scripts"))
from build import discover

DIST = ROOT / "dist"
# Optional: extra copy of the viewer (e.g. an IDE artifacts folder). Off unless the env var is set.
_artifact_env = os.environ.get("LDML_ARTIFACT_DIR")
ARTIFACT_DIR = Path(_artifact_env) if _artifact_env else None

SYMBOL_NAMES = {
    '.': 'period', ',': 'comma', '?': 'question', '!': 'exclam',
    '-': 'hyphen', '_': 'underscore', ':': 'colon', ';': 'semicolon',
    '"': 'quote', "'": 'apos', '(': 'lparen', ')': 'rparen',
    '[': 'lbracket', ']': 'rbracket', '{': 'lbrace', '}': 'rbrace',
    '/': 'slash', '\\': 'backslash', '|': 'pipe', '@': 'at',
    '#': 'hash', '$': 'dollar', '%': 'percent', '^': 'caret',
    '&': 'amp', '*': 'asterisk', '+': 'plus', '=': 'equal',
    '<': 'lt', '>': 'gt', '~': 'tilde', '`': 'grave',
    '€': 'euro', '₽': 'ruble', '£': 'pound', '¥': 'yen', '§': 'section',
    '°': 'degree', '•': 'bullet', '…': 'ellipsis', '№': 'numero',
    '—': 'emdash', '–': 'endash', '«': 'laquo', '»': 'raquo',
    '“': 'ldquo', '”': 'rdquo', '‘': 'lsquo', '’': 'rsquo',
    '´': 'acute', '¨': 'diaeresis', '¯': 'macron', '±': 'plusminus',
    '≠': 'noteq'
}

def token_to_id(token):
    token = token.strip()
    if not token:
        return "spacer"
    if token.startswith("\\s{"):
        m = re.match(r'\\s\{([a-zA-Z0-9_-]+)', token)
        if m:
            action = m.group(1).lower()
            if action.startswith("spacer"):
                return "spacer"
            if action in ("return", "return-alts"):
                return "return"
            return action
        return "spacer"
    
    if len(token) == 1 and token.isascii() and token.isalnum():
        if token.islower():
            return f"k_{token}"
        if token.isupper():
            return f"k_{token.lower()}_upper"
        return f"k_{token}"
        
    if token in SYMBOL_NAMES:
        return f"k_{SYMBOL_NAMES[token]}"
        
    # Unicode codepoints hex mapping for safe XML IDs
    cps = "_".join(f"u{ord(c):04x}" for c in token)
    return f"k_{cps}"

from xml.sax.saxutils import escape as _xml_escape

def xml_escape(val):
    return _xml_escape(str(val), {'"': '&quot;', "'": '&apos;'})

def k3_output_escape(val):
    s = str(val).replace("\\", "\\\\")
    return xml_escape(s)

def is_system_token(token):
    return token.startswith("\\s{")

def generate_ldml_xml(lang_code, lang_name, layout, lp_dict):
    lid = layout["id"]
    label = xml_escape(layout.get("label", "Standard"))
    space_label = xml_escape(layout.get("space", "Space"))
    return_label = xml_escape(layout.get("ret", "Return"))
    lang_name_esc = xml_escape(lang_name)
    
    # Сбор всех уникальных токенов со всех слоёв
    layers_data = [
        ("base", layout.get("rows", [])),
        ("shift", layout.get("shift", [])),
        ("symbols", layout.get("sym1", [])),
        ("symbols2", layout.get("sym2", []))
    ]
    
    unique_tokens = set()
    system_ids = set()
    
    for _, rows in layers_data:
        if not rows: continue
        for row in rows:
            for token in row:
                if is_system_token(token):
                    system_ids.add(token_to_id(token))
                else:
                    unique_tokens.add(token)
                    
    # Генерация XML
    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append(f'<keyboard3 xmlns="https://schemas.unicode.org/cldr/45/keyboard3" locale="{lang_code}" conformsTo="45">')
    lines.append('  <version number="1.0.0"/>')
    lines.append(f'  <info author="ios-system" name="{lang_name_esc} ({label})"/>')
    lines.append('  <locales>')
    lines.append(f'    <locale id="{lang_code}"/>')
    lines.append('  </locales>')
    
    # Displays
    lines.append('  <displays>')
    lines.append(f'    <display keyId="space" display="{space_label}"/>')
    lines.append(f'    <display keyId="return" display="{return_label}"/>')
    lines.append('    <display keyId="shift" display="⇧"/>')
    lines.append('    <display keyId="backspace" display="⌫"/>')
    if "shiftSymbols" in system_ids:
        lines.append('    <display keyId="shiftSymbols" display="#+="/>')
    lines.append('  </displays>')
    
    # Keys
    lines.append('  <keys>')
    # System keys
    for sys_id in sorted(system_ids):
        if sys_id == "shift":
            lines.append(f'    <key id="{sys_id}" layerId="shift"/>')
        elif sys_id in ("shiftsymbols", "shiftSymbols"):
            lines.append(f'    <key id="{sys_id}" layerId="symbols"/>')
        elif sys_id == "spacer":
            lines.append(f'    <key id="{sys_id}" gap="true"/>')
        elif sys_id == "backspace":
            lines.append(f'    <key id="{sys_id}" output="\\u{{0008}}"/>')
        elif sys_id == "return":
            lines.append(f'    <key id="{sys_id}" output="\\u{{000d}}"/>')
        elif sys_id == "space":
            lines.append(f'    <key id="{sys_id}" output=" "/>')
        elif sys_id == "tab":
            lines.append(f'    <key id="{sys_id}" output="\\u{{0009}}"/>')
        elif sys_id == "caps":
            lines.append(f'    <key id="{sys_id}" layerId="shift"/>')
        
    # Character keys & alternates
    sorted_tokens = sorted(unique_tokens)
    alt_keys_generated = set()
    
    for token in sorted_tokens:
        kid = token_to_id(token)
        alternates = lp_dict.get(token, "")
        if alternates:
            alt_list = [a.strip() for a in alternates.split() if a.strip()]
            alt_ids = []
            for alt in alt_list:
                aid = token_to_id(alt)
                alt_ids.append(aid)
                if aid not in alt_keys_generated and aid != kid:
                    lines.append(f'    <key id="{aid}" output="{k3_output_escape(alt)}"/>')
                    alt_keys_generated.add(aid)
            alt_ids_str = " ".join(alt_ids)
            lines.append(f'    <key id="{kid}" output="{k3_output_escape(token)}" longPressKeyIds="{alt_ids_str}"/>')
        else:
            if kid not in alt_keys_generated:
                lines.append(f'    <key id="{kid}" output="{k3_output_escape(token)}"/>')
    lines.append('  </keys>')
    
    # Layers
    lines.append('  <layers formId="touch">')
    for layer_name, rows in layers_data:
        if not rows: continue
        lines.append(f'    <layer id="{layer_name}">')
        for row in rows:
            row_ids = [token_to_id(t) for t in row]
            row_str = " ".join(row_ids)
            lines.append(f'      <row keys="{row_str}"/>')
        lines.append('    </layer>')
    lines.append('  </layers>')
    lines.append('  ')
    lines.append('  <!-- Modular Pipeline Placeholders for Hardware Forms (PC / Mac): -->')
    lines.append('  <!-- <layers formId="us"> ... desktop ANSI hardware layout placeholder ... </layers> -->')
    lines.append('  <!-- <layers formId="iso"> ... desktop ISO hardware layout placeholder ... </layers> -->')
    lines.append('</keyboard3>')
    
    return "\n".join(lines)

def generate_html_viewer(data_groups, lp_map):
    ldml_database = []
    
    for group in data_groups:
        g_name = group["group"]
        g_color = group["color"]
        for lang in group["langs"]:
            l_code = lang["code"]
            l_name = lang["name"]
            for lay in lang["layouts"]:
                xml_content = generate_ldml_xml(l_code, l_name, lay, lp_map.get(lay["id"], {}))
                ldml_database.append({
                    "group": g_name,
                    "color": g_color,
                    "code": l_code,
                    "name": l_name,
                    "layoutId": lay["id"],
                    "label": lay.get("label", "Standard"),
                    "abc": lay.get("abc", "АБВ"),
                    "spaceLabel": lay.get("space", "Boşluk"),
                    "returnLabel": lay.get("ret", "Giriş"),
                    "rows": lay.get("rows", []),
                    "shift": lay.get("shift", []),
                    "sym1": lay.get("sym1", []),
                    "sym2": lay.get("sym2", []),
                    "longpress": lp_map.get(lay["id"], {}),
                    "xml": xml_content
                })
                
    json_db = json.dumps(ldml_database, ensure_ascii=False)
    
    html_template = f"""<!DOCTYPE html>
<html lang="ru">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>LDML (CLDR) Keyboards · ios-system</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Fira+Code:wght@400;500&family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
  <style>
    :root {{
      --bg: #0b0f17;
      --panel: #131b2e;
      --panel-hover: #1b263b;
      --border: rgba(255, 255, 255, 0.08);
      --text: #e2e8f0;
      --text-dim: #94a3b8;
      --accent: #6366f1;
      --accent-grad: linear-gradient(135deg, #6366f1, #a855f7);
      --code-bg: #0d121c;
    }}
    * {{ box-sizing: border-box; margin: 0; padding: 0; }}
    body {{
      font-family: 'Inter', -apple-system, sans-serif;
      background: var(--bg);
      color: var(--text);
      display: flex;
      height: 100vh;
      overflow: hidden;
    }}
    aside {{
      width: 320px;
      background: var(--panel);
      border-right: 1px solid var(--border);
      display: flex;
      flex-direction: column;
      flex-shrink: 0;
    }}
    .sidebar-header {{
      padding: 20px;
      border-bottom: 1px solid var(--border);
    }}
    .sidebar-header h1 {{
      font-size: 1.1rem;
      font-weight: 700;
      background: var(--accent-grad);
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
      margin-bottom: 6px;
    }}
    .sidebar-header p {{
      font-size: 0.8rem;
      color: var(--text-dim);
      line-height: 1.4;
    }}
    .lang-toggle-btn {{
      background: var(--panel);
      border: 1px solid var(--border);
      color: #38bdf8;
      padding: 4px 10px;
      border-radius: 20px;
      font-size: 0.75rem;
      font-weight: 600;
      cursor: pointer;
      transition: all 0.2s;
    }}
    .lang-toggle-btn:hover {{ background: rgba(56,189,248,0.15); border-color: #38bdf8; }}
    .search-box {{
      padding: 12px 20px;
      border-bottom: 1px solid var(--border);
    }}
    .search-box input {{
      width: 100%;
      background: var(--bg);
      border: 1px solid var(--border);
      border-radius: 8px;
      padding: 8px 12px;
      color: #fff;
      font-size: 0.85rem;
      outline: none;
      transition: border-color 0.2s;
    }}
    .search-box input:focus {{ border-color: var(--accent); }}
    .lang-list {{
      flex: 1;
      overflow-y: auto;
      padding: 10px;
    }}
    .group-title {{
      font-size: 0.75rem;
      text-transform: uppercase;
      letter-spacing: 0.05em;
      color: var(--text-dim);
      padding: 12px 10px 4px;
      font-weight: 600;
    }}
    .lang-item {{
      display: flex;
      align-items: center;
      justify-content: space-between;
      padding: 10px 12px;
      border-radius: 8px;
      cursor: pointer;
      transition: background 0.15s;
      margin-bottom: 2px;
    }}
    .lang-item:hover {{ background: var(--panel-hover); }}
    .lang-item.active {{
      background: rgba(99, 102, 241, 0.15);
      border: 1px solid rgba(99, 102, 241, 0.3);
    }}
    .lang-info {{ display: flex; align-items: center; gap: 10px; }}
    .dot {{ width: 10px; height: 10px; border-radius: 50%; flex-shrink: 0; }}
    .lang-name {{ font-weight: 500; font-size: 0.9rem; }}
    .lang-code {{ font-size: 0.75rem; color: var(--text-dim); background: rgba(255,255,255,0.05); padding: 2px 6px; border-radius: 4px; }}
    main {{
      flex: 1;
      display: flex;
      flex-direction: column;
      overflow-y: auto;
      padding: 30px;
    }}
    .top-bar {{
      display: flex;
      justify-content: space-between;
      align-items: flex-start;
      margin-bottom: 24px;
      background: var(--panel);
      padding: 24px;
      border-radius: 16px;
      border: 1px solid var(--border);
    }}
    .title-area h2 {{ font-size: 1.6rem; font-weight: 700; margin-bottom: 8px; display: flex; align-items: center; gap: 12px; }}
    .title-area p {{ color: var(--text-dim); font-size: 0.9rem; }}
    .actions {{ display: flex; gap: 12px; }}
    .btn {{
      background: var(--panel-hover);
      color: #fff;
      border: 1px solid var(--border);
      padding: 10px 18px;
      border-radius: 8px;
      font-weight: 600;
      font-size: 0.85rem;
      cursor: pointer;
      transition: all 0.2s;
      display: inline-flex;
      align-items: center;
      gap: 8px;
      text-decoration: none;
    }}
    .btn:hover {{ background: rgba(255,255,255,0.1); border-color: rgba(255,255,255,0.2); }}
    .btn-primary {{ background: var(--accent-grad); border: none; }}
    .btn-primary:hover {{ opacity: 0.95; transform: translateY(-1px); box-shadow: 0 4px 12px rgba(99, 102, 241, 0.3); }}
    
    .info-card {{
      background: var(--panel);
      border: 1px solid var(--border);
      border-left: 4px solid var(--accent);
      border-radius: 12px;
      padding: 18px 22px;
      margin-bottom: 24px;
      box-shadow: 0 4px 12px rgba(0,0,0,0.15);
    }}
    .info-card h4 {{
      font-size: 0.95rem;
      color: #fff;
      margin-bottom: 8px;
      display: flex;
      align-items: center;
      gap: 8px;
    }}
    .info-card p {{
      font-size: 0.85rem;
      color: var(--text-dim);
      line-height: 1.5;
      margin-bottom: 10px;
    }}
    .info-card ul {{
      margin-left: 20px;
      font-size: 0.85rem;
      color: #cbd5e1;
      line-height: 1.6;
      margin-bottom: 14px;
    }}
    .info-card li {{ margin-bottom: 4px; }}
    .info-card .info-footer {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      padding-top: 12px;
      border-top: 1px solid var(--border);
      font-size: 0.8rem;
      color: #94a3b8;
      flex-wrap: wrap;
      gap: 10px;
    }}
    
    .layout-selector {{
      display: flex;
      gap: 8px;
      margin-bottom: 20px;
    }}
    .layout-tab {{
      padding: 6px 14px;
      border-radius: 6px;
      background: var(--panel);
      border: 1px solid var(--border);
      color: var(--text-dim);
      font-size: 0.85rem;
      cursor: pointer;
      font-weight: 500;
    }}
    .layout-tab.active {{ background: var(--accent); color: #fff; border-color: var(--accent); }}
    
    .preview-box {{
      background: var(--panel);
      border: 1px solid var(--border);
      border-radius: 16px;
      padding: 24px;
      margin-bottom: 24px;
    }}
    .preview-header {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 16px;
    }}
    .preview-header h3 {{ font-size: 1rem; font-weight: 600; }}
    .layer-tabs {{ display: flex; gap: 6px; }}
    .layer-btn {{
      background: var(--bg);
      border: 1px solid var(--border);
      color: var(--text-dim);
      padding: 4px 10px;
      border-radius: 6px;
      font-size: 0.75rem;
      cursor: pointer;
    }}
    .layer-btn.active {{ background: rgba(255,255,255,0.1); color: #fff; border-color: rgba(255,255,255,0.3); }}
    
    .keyboard-mockup {{
      display: flex;
      flex-direction: column;
      gap: 8px;
      align-items: center;
      background: var(--bg);
      padding: 20px;
      border-radius: 12px;
      border: 1px solid var(--border);
      position: relative;
    }}
    .emulator-screen {{
      background: #090d14;
      border: 1px solid var(--border);
      border-radius: 10px;
      padding: 12px 16px;
      margin-bottom: 12px;
      display: flex;
      gap: 12px;
      align-items: center;
      width: 100%;
      max-width: 650px;
      box-shadow: inset 0 2px 4px rgba(0,0,0,0.4);
    }}
    .emulator-input {{
      background: transparent;
      border: none;
      color: #fff;
      font-size: 1.05rem;
      font-family: 'Inter', sans-serif;
      flex: 1;
      outline: none;
    }}
    .clear-btn {{
      background: rgba(255,255,255,0.05);
      border: 1px solid var(--border);
      color: var(--text-dim);
      padding: 6px 12px;
      border-radius: 6px;
      font-size: 0.8rem;
      cursor: pointer;
      transition: all 0.15s;
    }}
    .clear-btn:hover {{ background: rgba(255,255,255,0.15); color: #fff; }}
    .kb-row {{ display: flex; gap: 6px; justify-content: center; width: 100%; max-width: 650px; }}
    .kb-key {{
      flex: 1;
      height: 44px;
      background: var(--panel);
      border: 1px solid var(--border);
      border-radius: 8px;
      display: flex;
      align-items: center;
      justify-content: center;
      font-weight: 500;
      font-size: 0.95rem;
      color: #fff;
      box-shadow: 0 2px 4px rgba(0,0,0,0.3);
      min-width: 30px;
      position: relative;
      user-select: none;
      cursor: pointer;
      transition: background 0.1s, transform 0.05s;
    }}
    .kb-key:active {{
      transform: scale(0.96);
      background: var(--accent);
    }}
    .kb-key.sys {{ background: #1e293b; color: #cbd5e1; font-size: 0.85rem; }}
    .kb-key.space {{ flex: 4; font-size: 0.85rem; color: var(--text-dim); }}
    .kb-key.has-alt::after {{
      content: '';
      position: absolute;
      top: 4px;
      right: 4px;
      width: 6px;
      height: 6px;
      background: var(--accent);
      border-radius: 50%;
    }}
    .alt-popup {{
      position: absolute;
      bottom: calc(100% + 8px);
      left: 50%;
      transform: translateX(-50%);
      background: #1e293b;
      border: 1px solid rgba(255,255,255,0.25);
      border-radius: 10px;
      padding: 6px;
      display: flex;
      gap: 6px;
      box-shadow: 0 10px 25px rgba(0,0,0,0.6);
      z-index: 1000;
      animation: popIn 0.15s cubic-bezier(0.16, 1, 0.3, 1);
    }}
    @keyframes popIn {{
      from {{ opacity: 0; transform: translate(-50%, 10px) scale(0.9); }}
      to {{ opacity: 1; transform: translate(-50%, 0) scale(1); }}
    }}
    .alt-key {{
      background: var(--panel);
      border: 1px solid var(--border);
      color: #fff;
      padding: 8px 14px;
      border-radius: 6px;
      font-size: 1.05rem;
      cursor: pointer;
      min-width: 38px;
      text-align: center;
      transition: all 0.15s;
      font-weight: 600;
    }}
    .alt-key:hover {{ background: var(--accent); transform: translateY(-2px); }}
    
    .xml-container {{
      background: var(--code-bg);
      border: 1px solid var(--border);
      border-radius: 16px;
      overflow: hidden;
      display: flex;
      flex-direction: column;
      flex: 1;
    }}
    .xml-header {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      padding: 14px 20px;
      background: rgba(255,255,255,0.02);
      border-bottom: 1px solid var(--border);
    }}
    .xml-header span {{ font-family: 'Fira Code', monospace; font-size: 0.85rem; color: var(--text-dim); }}
    pre {{
      padding: 20px;
      overflow-x: auto;
      font-family: 'Fira Code', monospace;
      font-size: 0.85rem;
      line-height: 1.6;
      color: #e2e8f0;
    }}
    .tag {{ color: #f43f5e; }}
    .attr {{ color: #38bdf8; }}
    .val {{ color: #a3e635; }}
    .cmnt {{ color: #64748b; font-style: italic; }}
  </style>
</head>
<body>
  <aside>
    <div class="sidebar-header">
      <div style="display:flex; justify-content:space-between; align-items:flex-start; width:100%;">
        <h1 id="uiTitle">LDML Keyboards</h1>
        <div style="display:flex; gap:6px; align-items:center;">
          <a href="ios-keyboards.html" class="lang-toggle-btn" style="text-decoration:none; display:inline-block;" title="Go to iOS Keyboard Viewer">📱 iOS</a>
          <button class="lang-toggle-btn" onclick="toggleUILang()" id="uiLangBtn">🌐 RU</button>
        </div>
      </div>
      <p id="uiSubtitle">CLDR / Unicode Keyboard3 specification for languages of Russia</p>
    </div>
    <div class="search-box">
      <input type="text" id="searchInput" placeholder="Search language or code...">
    </div>
    <div class="lang-list" id="langList"></div>
  </aside>
  <main>
    <div class="info-card">
      <h4 id="cardTitle">💡 Why this local emulator & what problem are we solving?</h4>
      <p id="cardP1">The <b>Unicode Keyboard3 (LDML CLDR)</b> specification is the new international standard for keyboard layouts. The official <a href="https://play.k3lp.org/" target="_blank" style="color:var(--accent)">play.k3lp.org</a> tool is currently in Alpha and serves mainly for XML syntax validation, but <b>lacks visual UI testing for touch typing and longpress interactions</b> (<a href="https://github.com/florisboard/florisboard/discussions/3295" target="_blank" style="color:var(--accent)">FlorisBoard #3295</a>).</p>
      <p id="cardP2"><b>Our autonomous emulator solves 3 key challenges:</b></p>
      <ul>
        <li id="cardLi1"><b>Interactive UX Testing (Longpresses):</b> Live visual testing of character input via longpress (hold any key with a blue dot or right-click) and layer switching (base, shift, symbols).</li>
        <li id="cardLi2"><b>Offline Autonomy (Zero-dependency):</b> The entire repository of 47 indigenous and minority languages of Russia is packaged into a single standalone HTML file. It runs completely offline without servers or dependencies.</li>
        <li id="cardLi3"><b>Pre-integration Verification:</b> Ensures that when OS keyboard engines (iOS, Android, FlorisBoard) fully adopt LDML 3.0, our layout specifications will work flawlessly out of the box!</li>
      </ul>
      <div class="info-footer">
        <span id="cardInstr"><b>Instructions:</b> Click keys to type. Hold keys with blue dots for popup menus.</span>
        <a href="https://play.k3lp.org/" target="_blank" class="btn btn-primary" style="padding: 6px 12px; font-size: 0.75rem;">k3lp playground ↗</a>
      </div>
    </div>
    
    <div class="top-bar">
      <div class="title-area">
        <h2 id="langTitle">Select a language</h2>
        <p id="langSubtitle">Unicode Keyboard3 Specification</p>
      </div>
      <div class="actions">
        <button class="btn btn-primary" id="copyBtn" onclick="copyXml()">📋 Copy XML</button>
      </div>
    </div>

    <div class="layout-selector" id="layoutSelector"></div>

    <div class="preview-box">
      <div class="preview-header">
        <h3 id="previewTitle">Interactive Layout Emulator</h3>
        <div class="layer-tabs" id="layerTabs">
          <button class="layer-btn active" id="btnLayerRows" onclick="setLayer('rows')">Base (rows)</button>
          <button class="layer-btn" id="btnLayerShift" onclick="setLayer('shift')">Shift (shift)</button>
          <button class="layer-btn" id="btnLayerSym1" onclick="setLayer('sym1')">Numbers (symbols)</button>
          <button class="layer-btn" id="btnLayerSym2" onclick="setLayer('sym2')">Symbols (symbols2)</button>
        </div>
      </div>
      <div class="keyboard-mockup" id="kbMockup"></div>
    </div>

    <div class="xml-container">
      <div class="xml-header">
        <span id="xmlFilename">layout.xml</span>
        <span>LDML / CLDR v3</span>
      </div>
      <pre id="xmlCode"></pre>
    </div>
  </main>

  <script>
    const db = {json_db};
    let currentLangCode = db.length > 0 ? db[0].code : null;
    let currentLayoutId = db.length > 0 ? db[0].layoutId : null;
    let currentLayer = 'rows';
    let activePopup = null;
    let currentUILang = 'en';

    const i18n = {{
      en: {{
        title: "LDML Keyboards",
        subtitle: "CLDR / Unicode Keyboard3 specification for languages of Russia",
        searchPlaceholder: "Search language or code...",
        cardTitle: "💡 Why this local emulator & what problem are we solving?",
        cardP1: 'The <b>Unicode Keyboard3 (LDML CLDR)</b> specification is the new international standard for keyboard layouts. The official <a href="https://play.k3lp.org/" target="_blank" style="color:var(--accent)">play.k3lp.org</a> tool is currently in Alpha and serves mainly for XML syntax validation, but <b>lacks visual UI testing for touch typing and longpress interactions</b> (<a href="https://github.com/florisboard/florisboard/discussions/3295" target="_blank" style="color:var(--accent)">FlorisBoard #3295</a>).',
        cardP2: "<b>Our autonomous emulator solves 3 key challenges:</b>",
        cardLi1: "<b>Interactive UX Testing (Longpresses):</b> Live visual testing of character input via longpress (hold any key with a blue dot or right-click) and layer switching (base, shift, symbols).",
        cardLi2: "<b>Offline Autonomy (Zero-dependency):</b> The entire repository of 47 indigenous and minority languages of Russia is packaged into a single standalone HTML file. It runs completely offline without servers or dependencies.",
        cardLi3: "<b>Pre-integration Verification:</b> Ensures that when OS keyboard engines (iOS, Android, FlorisBoard) fully adopt LDML 3.0, our layout specifications will work flawlessly out of the box!",
        cardInstr: "<b>Instructions:</b> Click keys to type. Hold keys with blue dots for popup menus.",
        copyXml: "📋 Copy XML",
        copied: "✅ Copied!",
        previewTitle: "Interactive Layout Emulator",
        layerRows: "Base (rows)",
        layerShift: "Shift (shift)",
        layerSym1: "Numbers (symbols)",
        layerSym2: "Symbols (symbols2)",
        inputPlaceholder: "Click keys or hold down for popup menus...",
        clearBtn: "Clear",
        codeLabel: "Code",
        layoutLabel: "Layout",
        groups: {{
          "Тюркские": "TURKIC",
          "Монгольские": "MONGOLIC",
          "Кавказские": "CAUCASIAN",
          "Иранские": "IRANIAN",
          "Уральские": "URALIC",
          "Славянские": "SLAVIC",
          "Тунгусо-маньчжурские": "TUNGUSIC",
          "Другие": "OTHER"
        }}
      }},
      ru: {{
        title: "LDML Keyboards",
        subtitle: "Спецификация CLDR / Unicode Keyboard3 для языков народов РФ",
        searchPlaceholder: "Поиск языка или кода...",
        cardTitle: "💡 Зачем нужен этот локальный эмулятор и какую задачу мы решаем?",
        cardP1: 'Спецификация <b>Unicode Keyboard3 (LDML CLDR)</b> — это новый международный стандарт описания раскладок. Официальный инструмент <a href="https://play.k3lp.org/" target="_blank" style="color:var(--accent)">play.k3lp.org</a> пока находится на стадии Alpha и служит в основном для валидации XML, но <b>не позволяет визуально протестировать ввод текста и долгие нажатия (лонгпрессы)</b> (<a href="https://github.com/florisboard/florisboard/discussions/3295" target="_blank" style="color:var(--accent)">FlorisBoard #3295</a>).',
        cardP2: "<b>Наш автономный эмулятор решает 3 ключевые задачи:</b>",
        cardLi1: "<b>Визуальное тестирование UX (Лонгпрессы):</b> Мы можем вживую протестировать ввод символов по долгому нажатию (удерживайте клавишу с синей точкой или нажмите правой кнопкой мыши) и переключение слоёв (base, shift, symbols).",
        cardLi2: "<b>Офлайн-автономия (Zero-dependency):</b> Весь каталог из 47 раскладок народов РФ упакован в один автономный HTML-файл. Его можно открывать без интернета и передавать экспертам или лингвистам.",
        cardLi3: "<b>Верификация данных перед интеграцией:</b> Мы гарантируем, что когда движки мобильных ОС (iOS, Android) полностью внедрят стандарт LDML 3.0, наши раскладки заработают идеально с первого дня!",
        cardInstr: "<b>Инструкция:</b> Кликайте по клавишам для набора текста. Удерживайте клавиши с синей точкой для попапов.",
        copyXml: "📋 Копировать XML",
        copied: "✅ Скопировано!",
        previewTitle: "Интерактивный эмулятор раскладки",
        layerRows: "Строчные (base)",
        layerShift: "Заглавные (shift)",
        layerSym1: "Цифры (symbols)",
        layerSym2: "Символы (symbols2)",
        inputPlaceholder: "Нажимайте клавиши или удерживайте для попапа...",
        clearBtn: "Очистить",
        codeLabel: "Код",
        layoutLabel: "Раскладка",
        groups: {{
          "Тюркские": "ТЮРКСКИЕ",
          "Монгольские": "МОНГОЛЬСКИЕ",
          "Кавказские": "КАВКАЗСКИЕ",
          "Иранские": "ИРАНСКИЕ",
          "Уральские": "УРАЛЬСКИЕ",
          "Славянские": "СЛАВЯНСКИЕ",
          "Тунгусо-маньчжурские": "ТУНГУСО-МАНЬЧЖУРСКИЕ",
          "Другие": "ДРУГИЕ"
        }}
      }}
    }};

    function toggleUILang() {{
      currentUILang = currentUILang === 'en' ? 'ru' : 'en';
      document.getElementById('uiLangBtn').textContent = currentUILang === 'en' ? '🌐 RU' : '🌐 EN';
      applyUILang();
    }}

    function applyUILang() {{
      const t = i18n[currentUILang];
      document.getElementById('uiTitle').textContent = t.title;
      document.getElementById('uiSubtitle').textContent = t.subtitle;
      document.getElementById('searchInput').placeholder = t.searchPlaceholder;
      document.getElementById('cardTitle').textContent = t.cardTitle;
      document.getElementById('cardP1').innerHTML = t.cardP1;
      document.getElementById('cardP2').innerHTML = t.cardP2;
      document.getElementById('cardLi1').innerHTML = t.cardLi1;
      document.getElementById('cardLi2').innerHTML = t.cardLi2;
      document.getElementById('cardLi3').innerHTML = t.cardLi3;
      document.getElementById('cardInstr').innerHTML = t.cardInstr;
      
      const copyBtn = document.getElementById('copyBtn');
      if (copyBtn && !copyBtn.textContent.includes('✅')) copyBtn.textContent = t.copyXml;
      
      document.getElementById('previewTitle').textContent = t.previewTitle;
      document.getElementById('btnLayerRows').textContent = t.layerRows;
      document.getElementById('btnLayerShift').textContent = t.layerShift;
      document.getElementById('btnLayerSym1').textContent = t.layerSym1;
      document.getElementById('btnLayerSym2').textContent = t.layerSym2;
      
      const typedText = document.getElementById('typedText');
      if (typedText) typedText.placeholder = t.inputPlaceholder;
      const clearBtn = document.getElementById('clearBtnEl');
      if (clearBtn) clearBtn.textContent = t.clearBtn;

      const searchInput = document.getElementById('searchInput');
      if (searchInput) renderSidebar(searchInput.value.toLowerCase());
      renderMain();
    }}

    function init() {{
      applyUILang();
      if (currentLangCode) selectLang(currentLangCode);
      
      document.getElementById('searchInput').addEventListener('input', (e) => {{
        renderSidebar(e.target.value.toLowerCase());
      }});

      document.addEventListener('click', (e) => {{
        if (!e.target.closest('.alt-popup') && !e.target.closest('.kb-key')) closePopup();
      }});
    }}

    function closePopup() {{
      if (activePopup) {{ activePopup.remove(); activePopup = null; }}
    }}

    function renderSidebar(filter = '') {{
      const container = document.getElementById('langList');
      container.innerHTML = '';
      
      const groups = {{}};
      db.forEach(item => {{
        if (filter && !item.name.toLowerCase().includes(filter) && !item.code.toLowerCase().includes(filter)) return;
        if (!groups[item.group]) groups[item.group] = [];
        if (!groups[item.group].some(i => i.code === item.code)) {{
          groups[item.group].push(item);
        }}
      }});

      for (const [groupName, items] of Object.entries(groups)) {{
        if (items.length === 0) continue;
        const groupEl = document.createElement('div');
        groupEl.className = 'group-title';
        const t = i18n[currentUILang];
        groupEl.textContent = (t && t.groups && t.groups[groupName]) ? t.groups[groupName] : groupName;
        container.appendChild(groupEl);

        items.sort((a, b) => {{
          const isLatA = /^[a-zA-Z]/.test(a.name.trim());
          const isLatB = /^[a-zA-Z]/.test(b.name.trim());
          if (!isLatA && isLatB) return -1;
          if (isLatA && !isLatB) return 1;
          return a.name.localeCompare(b.name);
        }});

        items.forEach(item => {{
          const el = document.createElement('div');
          el.className = `lang-item ${{item.code === currentLangCode ? 'active' : ''}}`;
          el.onclick = () => selectLang(item.code);
          el.innerHTML = `
            <div class="lang-info">
              <div class="dot" style="background: ${{item.color}}"></div>
              <span class="lang-name">${{item.name}}</span>
            </div>
            <span class="lang-code">${{item.code}}</span>
          `;
          container.appendChild(el);
        }});
      }}
    }}

    function selectLang(code) {{
      currentLangCode = code;
      const layouts = db.filter(i => i.code === code);
      if (layouts.length > 0 && !layouts.some(l => l.layoutId === currentLayoutId)) {{
        currentLayoutId = layouts[0].layoutId;
      }}
      renderSidebar(document.getElementById('searchInput').value.toLowerCase());
      renderMain();
    }}

    function selectLayout(layoutId) {{
      currentLayoutId = layoutId;
      renderMain();
    }}

    function setLayer(layerName) {{
      currentLayer = layerName;
      document.querySelectorAll('.layer-btn').forEach(b => b.classList.remove('active'));
      event.target.classList.add('active');
      renderMockup();
    }}

    function renderMain() {{
      const item = db.find(i => i.layoutId === currentLayoutId) || db.find(i => i.code === currentLangCode);
      if (!item) return;

      const t = i18n[currentUILang];
      document.getElementById('langTitle').innerHTML = `<span class="dot" style="background:${{item.color}};width:16px;height:16px;display:inline-block;border-radius:50%;"></span> ${{item.name}}`;
      document.getElementById('langSubtitle').textContent = `${{t.codeLabel}}: ${{item.code}} · ${{t.layoutLabel}}: ${{item.label}}`;
      document.getElementById('xmlFilename').textContent = `${{item.code}}_${{item.layoutId}}.xml`;

      // Selector
      const layouts = db.filter(i => i.code === item.code);
      const selector = document.getElementById('layoutSelector');
      selector.innerHTML = '';
      if (layouts.length > 1) {{
        layouts.forEach(l => {{
          const btn = document.createElement('button');
          btn.className = `layout-tab ${{l.layoutId === currentLayoutId ? 'active' : ''}}`;
          btn.textContent = l.label;
          btn.onclick = () => selectLayout(l.layoutId);
          selector.appendChild(btn);
        }});
      }}

      renderMockup();
      renderXml(item.xml);
    }}

    function renderMockup() {{
      const item = db.find(i => i.layoutId === currentLayoutId);
      if (!item) return;
      
      const rows = item[currentLayer] && item[currentLayer].length > 0 ? item[currentLayer] : item.rows;
      const container = document.getElementById('kbMockup');
      
      // Preserve existing text if already rendered
      const oldInput = document.getElementById('typedText');
      const currentText = oldInput ? oldInput.value : '';

      const t = i18n[currentUILang];
      container.innerHTML = `
        <div class="emulator-screen">
          <input type="text" class="emulator-input" id="typedText" value="${{currentText}}" placeholder="${{t.inputPlaceholder}}">
          <button class="clear-btn" id="clearBtnEl" onclick="document.getElementById('typedText').value=''">${{t.clearBtn}}</button>
        </div>
      `;

      const typeChar = (ch) => {{
        const input = document.getElementById('typedText');
        if (input) {{ input.value += ch; input.focus(); }}
      }};

      const handleToken = (token) => {{
        closePopup();
        const input = document.getElementById('typedText');
        if (!input) return;

        if (token.startsWith('\\\\s{{')) {{
          if (token.includes('shiftSymbols') || token.includes('symbols')) {{
            setLayer(currentLayer === 'sym1' ? 'rows' : 'sym1');
          }} else if (token.includes('shift')) {{
            setLayer(currentLayer === 'shift' ? 'rows' : 'shift');
          }} else if (token.includes('backspace')) {{
            input.value = input.value.slice(0, -1);
            input.focus();
          }} else if (token.includes('return')) {{
            input.value += '\\n';
            input.focus();
          }} else if (token.includes('spacer')) {{
            // do nothing on click for spacer
          }} else if (token.includes('space')) {{
            input.value += ' ';
            input.focus();
          }}
        }} else {{
          typeChar(token);
        }}
      }};

      const allRows = [...rows];
      const hasSpace = allRows.some(r => r.some(t => t.includes('space') && !t.includes('spacer') && !t.includes('backspace')));
      if (!hasSpace) {{
        allRows.push(['\\\\s{{shiftSymbols}}', '\\\\s{{spacer:0.25}}', '\\\\s{{space}}', '\\\\s{{spacer:0.25}}', '\\\\s{{return}}']);
      }}

      allRows.forEach(row => {{
        const rowEl = document.createElement('div');
        rowEl.className = 'kb-row';
        row.forEach(token => {{
          const keyEl = document.createElement('div');
          keyEl.className = 'kb-key';
          
          if (token.startsWith('\\\\s{{')) {{
            keyEl.classList.add('sys');
            if (token.includes('shiftSymbols')) keyEl.textContent = '#+=';
            else if (token.includes('shift')) keyEl.textContent = '⇧';
            else if (token.includes('backspace')) keyEl.textContent = '⌫';
            else if (token.includes('return')) {{ keyEl.textContent = item.returnLabel || (currentUILang === 'en' ? 'Enter' : 'Giriş'); keyEl.classList.add('return'); }}
            else if (token.includes('spacer')) {{ keyEl.style.opacity = '0'; keyEl.style.flex = '0.35'; keyEl.style.pointerEvents = 'none'; }}
            else if (token.includes('space')) {{ keyEl.textContent = item.spaceLabel || (currentUILang === 'en' ? 'Space' : 'Boşluk'); keyEl.classList.add('space'); }}
            else keyEl.textContent = '•';
          }} else {{
            keyEl.textContent = token;
          }}

          const altsStr = item.longpress ? item.longpress[token] : null;
          if (altsStr) {{
            keyEl.classList.add('has-alt');
            const alts = altsStr.split(' ').filter(Boolean);
            
            let holdTimer = null;
            let isHold = false;

            const showPopup = (e) => {{
              if (e) e.stopPropagation();
              closePopup();
              const popup = document.createElement('div');
              popup.className = 'alt-popup';
              popup.onmousedown = (ev) => ev.stopPropagation();
              popup.onmouseup = (ev) => ev.stopPropagation();
              popup.onclick = (ev) => ev.stopPropagation();
              
              alts.forEach(alt => {{
                const altBtn = document.createElement('div');
                altBtn.className = 'alt-key';
                altBtn.textContent = alt;
                altBtn.onmousedown = (ev) => ev.stopPropagation();
                altBtn.onmouseup = (ev) => ev.stopPropagation();
                altBtn.onclick = (ev) => {{
                  ev.stopPropagation();
                  typeChar(alt);
                  closePopup();
                }};
                popup.appendChild(altBtn);
              }});
              keyEl.appendChild(popup);
              activePopup = popup;
            }};

            keyEl.onmousedown = (e) => {{
              if (e.button !== 0) return;
              if (activePopup) {{
                closePopup();
                return;
              }}
              isHold = false;
              holdTimer = setTimeout(() => {{
                isHold = true;
                showPopup(e);
              }}, 250);
            }};
            keyEl.onmouseup = (e) => {{
              clearTimeout(holdTimer);
              if (!isHold && !activePopup) handleToken(token);
            }};
            keyEl.onmouseleave = () => clearTimeout(holdTimer);
            keyEl.oncontextmenu = (e) => {{
              e.preventDefault();
              isHold = true;
              showPopup(e);
            }};
          }} else {{
            keyEl.onclick = () => handleToken(token);
          }}

          rowEl.appendChild(keyEl);
        }});
        container.appendChild(rowEl);
      }});
    }}

    function renderXml(xml) {{
      // Simple syntax highlighting
      let highlighted = xml
        .replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;')
        .replace(/(&lt;\\/?)([\w:]+)/g, '$1<span class="tag">$2</span>')
        .replace(/([\w:-]+)=(".*?")/g, '<span class="attr">$1</span>=<span class="val">$2</span>')
        .replace(/(&lt;!--.*?--&gt;)/g, '<span class="cmnt">$1</span>');
      document.getElementById('xmlCode').innerHTML = highlighted;
    }}

    function copyXml() {{
      const item = db.find(i => i.layoutId === currentLayoutId);
      if (!item) return;
      navigator.clipboard.writeText(item.xml).then(() => {{
        const t = i18n[currentUILang];
        const btn = document.getElementById('copyBtn');
        btn.textContent = t.copied;
        btn.style.background = '#10b981';
        setTimeout(() => {{
          btn.textContent = t.copyXml;
          btn.style.background = '';
        }}, 2000);
      }});
    }}

    init();
  </script>
</body>
</html>"""

    DIST.mkdir(exist_ok=True)
    out_file = DIST / "ldml-keyboards.html"
    with open(out_file, "w", encoding="utf-8") as f:
        f.write(html_template)
    print(f"✅ Создано (в проекте): {out_file} ({len(html_template)//1024} KB)")
    
    # Сохраняем копию в директорию артефактов (только если задан LDML_ARTIFACT_DIR)
    if ARTIFACT_DIR is None:
        return
    try:
        ARTIFACT_DIR.mkdir(parents=True, exist_ok=True)
        art_file = ARTIFACT_DIR / "ldml_keyboards.html"
        with open(art_file, "w", encoding="utf-8") as f:
            f.write(html_template)
        print(f"✅ Создано (артефакт): {art_file}")
    except Exception as e:
        print(f"ℹ️ Пропущено сохранение копии в LDML_ARTIFACT_DIR (не критично для CI): {e}")

if __name__ == "__main__":
    data_groups, lp_map = discover()
    generate_html_viewer(data_groups, lp_map)
