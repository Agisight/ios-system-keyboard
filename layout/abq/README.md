# Abaza (`abq`) keyboard — work in progress

> **Status: not ready yet.**
>
> The Abaza keyboard layout is still being designed and tested with native
> speakers and community representatives. The repository currently preserves
> localized system key names and the alphabet reference, but does not yet
> contain a finalized keyboard layout.

Русская версия: [README.ru.md](README.ru.md)

## Alphabet reference

The alphabet below is preserved from a community-provided Abaza alphabet chart
used during the keyboard design discussion.

**72 entries:**

```text
А Б В Г ГӀ ГӀВ ГВ ГЪ ГЪВ ГЪЬ ГЬ Д ДЖ ДЖВ ДЖЬ ДЗ Ж ЖВ ЖЬ З Й К КӀ КӀВ КӀЬ КВ КЪ КЪВ КЪЬ КЬ Л ЛЬ М Н П ПӀ Р С Т ТӀ ТЛ ТШ У Ф Х ХӀ ХӀВ ХВ ХЪ ХЪВ ХЬ Ц ЦӀ Ч ЧӀ ЧӀВ ЧВ Ш ШӀ ШВ Щ Ъ Е Ё И О Ы Э Ю Я Ӏ Ь
```

Lowercase:

```text
а б в г гӏ гӏв гв гъ гъв гъь гь д дж джв джь дз ж жв жь з й к кӏ кӏв кӏь кв къ къв къь кь л ль м н п пӏ р с т тӏ тл тш у ф х хӏ хӏв хв хъ хъв хь ц цӏ ч чӏ чӏв чв ш шӏ шв щ ъ е ё и о ы э ю я ӏ ь
```

Some entries are digraphs or multi-character Cyrillic sequences, including
forms with the Cyrillic palochka `Ӏ`. They must not be treated as single Unicode
code points merely because they function as alphabet entries.

This list is stored here so that the alphabet reference is not lost while the
keyboard geometry is still under discussion.

## Keyboard design status

The final physical/touch layout is **not finalized**.

The design discussion has included:

- compact 3-row and 4-row layouts;
- long-press groups for related letters;
- possible dynamic/contextual access to less frequent combinations;
- usability testing with native speakers before choosing a final layout.

No unfinished layout is presented here as a production standard.

## Available data

Currently available in this folder:

- `abq-keynames.yaml` — localized labels for Space, Return, Search, Go, Send,
  Join, Route, Done, Next, Continue, Emergency, Cancel, Undo and Redo;
- `README.md` / `README.ru.md` — project status and preserved alphabet reference.

## Community review

The keyboard work has been discussed with Abaza speakers and community
representatives. A full keyboard layout should be added only after key
placement and long-press behavior have been reviewed and tested.
