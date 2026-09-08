# Kazakh (`kaz`) keyboard

## Status

`layout/kaz/` currently contains **Kazakh in the Arabic script (Töte jazu / төте жазу) only**.

Files:

- `kaz-arab-3-rows.yaml` — 3-row layout
- `kaz-arab-longpress.yaml` — long-press mappings

Kazakh Cyrillic and Latin layouts are not included yet.

## Layout origin

The layout follows the design developed by **Murat Karibay**.

Murat formalized and published this design as the **Kazakh (Arabic)** keyboard in Keyman. The Keyman version was submitted in May 2025 for `kk_Arab`, reviewed by the Keyman team, and approved after technical and packaging revisions.

References:

- https://keyman.com/keyboards/kazakh_arabic
- https://github.com/keymanapp/keyboards/tree/master/release/k/kazakh_arabic
- https://github.com/keymanapp/keyboards/pull/3547

This project follows Murat Karibay's design and uses the Keyman implementation as the public technical reference.

## Implementation

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

- Murat Karibay's layout uses `ء` (`U+0621 ARABIC LETTER HAMZA`) as the word-initial front-vowel marker.
- Kazakh Arabic input is handled as **RTL**.
- The script identifier is **`Arab`** (`kaz-Arab` / `kk-Arab`).

The implementation also received a **private technical review from a keyboard engineer at a major technology company**.

## Licensing
This repository is MIT-licensed.

The Keyman `kazakh_arabic` keyboard is licensed under the **MIT License**:

- Copyright © 2025–2026 Murat Karibay
- https://github.com/keymanapp/keyboards/blob/master/release/k/kazakh_arabic/LICENSE.md
