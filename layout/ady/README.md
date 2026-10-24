# West Circassian / Adyghe (ady) native iOS keyboard

## Language

West Circassian (Адыгабзэ), also called Adyghe, is a Northwest Caucasian language spoken in the
Republic of Adygea (Russia) and by a large diaspora, mainly in Turkey. It is written in Cyrillic.
Its close relative East Circassian (Kabardian, `kbd`) has its own layout in `layout/kbd`.

Language codes:
- ISO 639-2 / 639-3: `ady`

## Design

`ady-3-rows.yaml` is an **additive** layout: the Russian ЙЦУКЕН keyboard stays exactly as people
know it, and two keys are added at the ends of the first two rows:

```
й ц у к е н г ш щ з х ъ
ф ы в а п р о л д ж э ӏ
⇧ я ч с м и т ь б ю ⌫
```

Why only two keys: every Adyghe letter outside the Russian alphabet is a **digraph** of Russian
letters plus `ъ`, `ь` or `ӏ` (`гъ`, `къ`, `кӏ`, `шъ`, `шӏ`, `хь`, `жь`, `дж`, `дз`, …). So the only
characters missing from a Russian keyboard are the palochka `ӏ`, and `ъ`, which the Russian iPhone
keyboard hides behind a long-press on `ь`.

Both are among the most frequent characters in Adyghe text
(corpus counts from `rf-keyboard-corpora/data/ady/adiga.ai/frequencies`):

| Character | Share of letters | Inside |
|---|---|---|
| `ъ` | ~8.5% | гъ (4.0%), къ (2.0%), лъ, хъ, шъ, жъ, чъ |
| `ӏ` | ~5.2% | кӏ (2.1%), шӏ, пӏ, цӏ, лӏ, чӏ, тӏ, and alone (1.3%) |

Hiding either behind a long-press would mean an extra gesture every few words, so both go on the
visible layer. The same pattern is already used in this repository for Avar (`ava`: `ъ` after `х`,
`ӏ` on row 2) and Chechen (`che`).

On iPad (9-inch) `ӏ` takes the place of `ъ` at the end of row 3 and `ъ` moves to the end of row 1;
on iPad (12-inch) `ӏ` replaces `ё`, which moves to a long-press on `е`.

## Long-press

Digraphs are offered on the base letter as a shortcut, most frequent first:

- `к → кӏ къ`, `г → гъ`, `ж → жь жъ`, `л → лъ лӏ`, `п → пӏ`, `т → тӏ`
- `х → хь хъ`, `ц → цӏ`, `ч → чӏ чъ`, `ш → шӏ шъ`, `д → дж дз`
- `е → ё`

## Encoding notes: the palochka

The keyboard emits the real palochka: `ӏ` (U+04CF) on the lowercase layer and `Ӏ` (U+04C0) on the
uppercase layer, the same convention as the Chechen layout.

Without a palochka key people type look-alikes instead: Latin `I`, lowercase `l`, the digit `1`, or
the Ukrainian/Belarusian `І` (U+0406). The same word then exists in several spellings, which hurts
search, spell-checking and machine-learning data. The Kabardian frequency file in this project shows
the problem directly: about a third of its palochka occurrences are `І` (U+0406) rather than `Ӏ`.

Most published Adyghe text uses U+04C0 in both cases, so text processing (search, autocorrection,
training data) should treat U+04C0, U+04CF and the look-alikes above as the same letter.

## To do

- Test with native speakers (Adygea and the Turkish diaspora).
- Translate the system key names (`ady-keynames.yaml`); they must be checked by a native speaker.
- Latin-script Adyghe: the diaspora uses Latin orthographies (for example the one used by the
  Adıge Dil Derneği in Turkey). That needs a separate layout once the orthography is fixed.
