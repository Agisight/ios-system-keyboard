# Kazakh (`kaz`) keyboard

## Status

`layout/kaz/` currently contains:

- **Kazakh Arabic** (`kaz-Arab` / `kk-Arab`) — Töte jazu / төте жазу
- **Kazakh Latin** (`kaz-Latn` / `kk-Latn`) — an **experimental desktop/PC layout**

Kazakh Cyrillic keyboard layout is not included yet. Script-specific localized
system key names are available for Arabic, Cyrillic and Latin.

Files:

- `kaz-arab-3-rows.yaml` — Kazakh Arabic 3-row layout
- `kaz-arab-longpress.yaml` — Kazakh Arabic long-press mappings
- `kaz-arab-keynames.yaml` — Kazakh Arabic system key names
- `kaz-cyrl-keynames.yaml` — Kazakh Cyrillic system key names
- `kaz-latn-keynames.yaml` — Kazakh Latin system key names
- `kaz-latn-macos-experimental.yaml` — experimental Kazakh Latin desktop/PC layout

---

## Kazakh Arabic — Töte jazu

### Layout origin

The Arabic-script layout follows the design developed by **Murat Karibay**.

Murat formalized and published this design as the **Kazakh (Arabic)** keyboard
in Keyman. The Keyman version was submitted in May 2025 for `kk_Arab`, reviewed
by the Keyman team, and approved after technical and packaging revisions.

References:

- https://keyman.com/keyboards/kazakh_arabic
- https://github.com/keymanapp/keyboards/tree/master/release/k/kazakh_arabic
- https://github.com/keymanapp/keyboards/pull/3547

This project follows Murat Karibay's design and uses the Keyman implementation
as the public technical reference.

### Implementation

Main letter layout:

```text
ق ۋ ە ر ت ي ۇ ى و پ
ا س د ء گ ح ج ك ل
  ز ش ع ڭ ب ن م
```

The four additional letters are available through Shift and long-press:

```text
ء → ف
ح → ھ
ع → چ
ڭ → ۆ
```

Other implementation details:

- Murat Karibay's layout uses `ء` (`U+0621 ARABIC LETTER HAMZA`) as the
  word-initial front-vowel marker.
- Kazakh Arabic input is handled as **RTL**.
- The script identifier is **`Arab`** (`kaz-Arab` / `kk-Arab`).

The implementation also received a **private technical review from a keyboard
engineer at a major technology company**.

---

## Kazakh Latin — experimental desktop layout

`kaz-latn-macos-experimental.yaml` is an **experimental desktop layout**.
It is not intended to define a final or standardized Kazakh Latin keyboard.

The base letter placement follows the public QWERTY-style keyboard scheme shown in materials from the 2021 Kazakh Latin alphabet reform discussion:

- https://primeminister.kz/ru/news/a-mamin-provel-zasedanie-nackomissii-po-perevodu-alfavita-kazahskogo-yazyka-na-latinskuyu-grafiku-280497

The cited government material describes an improved Latin alphabet with
31 letters and presents a proposed order of Kazakh letters on a keyboard.

A later April 2021 revision reported by ARNA News changed the relevant Latin
letter from the earlier `Ŋ/ŋ` form to `Ñ/ñ`, citing technical difficulties
with text input. This experimental layout follows that later revision:

- https://arna-news.kz/arna_kz/chto-izmenilos-v-novom-variante-alfavita-kazahskogo-yazyka-na-latinice/

This is still treated here as reform-discussion material rather than a claim
that the experimental keyboard is a finalized current standard.

### Base desktop layout

```text
Q W E R T Y U I O P Ö Ñ
A S D F G H J K L Ş İ Ü
Z X C V B N M Ğ Ū Ä
```

Lowercase output:

```text
q w e r t y u ı o p ö ñ
a s d f g h j k l ş i ü
z x c v b n m ğ ū ä
```

The `I` / `İ` distinction is intentional:

```text
I ↔ ı
İ ↔ i
```

This follows the alphabet shown in the source material, where `I ı` and `İ i`
are distinct letter pairs.

### Desktop implementation

The source scheme is a **Desktop/QWERTY layout**, not a mobile keyboard. The YAML
therefore uses the repository's desktop `macOS.primary.layers` format.

The layout uses ISO desktop geometry because the proposed second letter row
contains 12 keys. The extra ISO key before `Z` is kept as `\` / `|`, allowing
`Z` to remain on the physical Z key.

Command-modified layers preserve standard Latin physical outputs for common macOS shortcuts.

### Experimental status

This layout is included for:

- technical preview;
- keyboard ergonomics research;
- testing against Kazakh Latin language data;
- comparison with future or alternative Kazakh Latin layouts.

The alphabet, punctuation layers, modifier behavior and physical placement may
be revised as additional standards, official specifications, usability studies
or community feedback become available.

It should therefore be treated as **experimental**, not as a production
keyboard standard.

---

## Kazakh system key names

Localized system/action key names are stored separately by script.

- Arabic: `kaz-arab-keynames.yaml` — included by `kaz-arab-3-rows.yaml`
- Cyrillic: `kaz-cyrl-keynames.yaml` — ready for a future Kazakh Cyrillic layout
- Latin: `kaz-latn-keynames.yaml` — ready for a future Kazakh Latin touch layout

The sets cover Space, Return, contextual Return actions (Search, Go, Send,
Join, Continue, Done, Next, Route), Emergency, Cancel, Undo and Redo.

---

## Licensing

This repository is MIT-licensed.

The Keyman `kazakh_arabic` keyboard is licensed under the **MIT License**:

- Copyright © 2025–2026 Murat Karibay
- https://github.com/keymanapp/keyboards/blob/master/release/k/kazakh_arabic/LICENSE.md
