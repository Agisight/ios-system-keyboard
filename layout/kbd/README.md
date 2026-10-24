# East Circassian / Kabardian (kbd) native iOS keyboard

## Language

East Circassian (Адыгэбзэ), also called Kabardian or Kabardino-Cherkess, is a Northwest Caucasian
language spoken in Kabardino-Balkaria and Karachay-Cherkessia (Russia) and by a large diaspora,
mainly in Turkey. It is written in Cyrillic. Its close relative West Circassian (Adyghe, `ady`)
has its own layout in `layout/ady`.

Language codes:
- ISO 639-2 / 639-3: `kbd`

## Design

`kbd-3-rows.yaml` uses the same additive design as `ady`: the Russian ЙЦУКЕН keyboard stays
untouched, with `ъ` added after `х` and the palochka `ӏ` after `э`:

```
й ц у к е н г ш щ з х ъ
ф ы в а п р о л д ж э ӏ
⇧ я ч с м и т ь б ю ⌫
```

Like Adyghe, every Kabardian letter outside the Russian alphabet is a digraph with `ъ`, `ь` or `ӏ`,
so these two keys are all that is missing. Both are very frequent
(corpus counts from `rf-keyboard-corpora/data/kbd/adiga.ai/frequencies`):

| Character | Share of letters | Inside |
|---|---|---|
| `ъ` | ~6.4% | къ (2.3%), гъ (2.1%), лъ, хъ |
| `ӏ` | ~5.2% | кӏ (1.8%), щӏ (1.3%), фӏ, цӏ, пӏ, тӏ, лӏ, and alone |

The single-character inventory of Kabardian and Adyghe is the same, so the visible layer is the
same. The two layouts differ in long-press, which follows each language's own digraphs
(Kabardian has `фӏ` and `щӏ`; Adyghe has `шъ`, `шӏ`, `жъ`, `чъ`, `чӏ`).

## Long-press

Most frequent first:

- `к → къ кӏ`, `г → гъ`, `ж → жь`, `л → лъ лӏ`, `п → пӏ`, `т → тӏ`, `ф → фӏ`
- `х → хь хъ`, `ц → цӏ`, `щ → щӏ`, `д → дж дз`
- `е → ё`

## Encoding notes: the palochka

The keyboard emits the real palochka: `ӏ` (U+04CF) lowercase, `Ӏ` (U+04C0) uppercase.

This matters for Kabardian in particular: in the corpus behind the frequency file, about a third of
palochka occurrences (`КІ`, 1.75% of letters) are typed with the Ukrainian/Belarusian `І` (U+0406)
instead of `Ӏ`, because people have no palochka key. Text processing should treat U+04C0, U+04CF,
U+0406/U+0456, Latin `I`/`l` and the digit `1` in this position as the same letter.

## To do

- Test with native speakers (Kabardino-Balkaria, Karachay-Cherkessia and the diaspora).
- Translate the system key names (`kbd-keynames.yaml`), checked by a native speaker.
