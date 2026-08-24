# Avar Keyboard Layouts for iOS

Three Avar keyboard layouts are provided:

* **ava-4-rows** — new 4-row layout, primary option
* **ava-3-rows** — 3-row layout, primary fallback option
* **ava-4-rows-legacy** — previous 4-row layout, additional fallback option

These layouts support different implementation options.

The new 4-row layout is the primary and preferred option. It is intended to be implemented first. It places all Avar letters directly on the primary layer without letter replacement.

If the new 4-row layout cannot be implemented due to technical limitations, key size, keyboard geometry, or other platform constraints, the 3-row layout is used as the primary fallback option.

If the 3-row layout has already been implemented and the new 4-row layout is not possible, the previous 4-row layout may be added as an additional alternative if it can be implemented technically.

The preferred implementation order is therefore:
1. new 4-row layout;
2. 3-row layout;
3. previous 4-row layout — only as an additional alternative after the 3-row layout has been implemented.

Depending on technical limitations, the following combinations may be available:
* new 4-row + 3-row;
* 3-row + previous 4-row;
* 3-row only.

## Long-press

Long-press is used to access:
* stress marks
* secondary symbols

## iPhone Versions

The following three layouts are available for iPhone:
* new 4-row layout
* 3-row layout
* previous 4-row layout

Their priority and implementation order follow the rules described above.

## iPad Versions

The same three layouts are available for iPad:
* new 4-row layout
* 3-row layout
* previous 4-row layout

Their priority and implementation order are the same as for iPhone.

## Avar macOS

Avar-specific letters (including ӏ) — 33 letters — are placed directly on the primary layer using standard ANSI keyboard geometry.

No letter replacement is used.

Stress marks are available via dead keys.

## Avar keyNames

Key names are translated into Avar using natural interface phrasing.

### Stress marks

Stress marks (combining acute accent U+0301) are optional and are primarily used for:
* educational purposes
* disambiguation

They should be ignored during:
* autocorrection
* search
* tokenization
* frequency analysis

### Recommended preprocessing

For linguistic processing (such as search, tokenization, or frequency analysis), it is recommended to:
1. apply Unicode NFD normalization
2. remove combining diacritical marks

This ensures that words are processed identically regardless of whether stress marks are present.
