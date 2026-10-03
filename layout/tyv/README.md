# **Tuvan (tyv) native iOS/macOS keyboards.**

## Tuvan iOS
There are 2 layers: tyv-3-rows and tyv-4-rows. 3 rows layout is default one. It uses swapping/replacing less frequent letters (ФЩЦ) to ӨҢҮ letters, making less frequent letters accessible via longpress.

4 rows keyboard is additional for people who don't like to longpress letters, also its 2-4 rows are exactly same as Russian keyboard – so it can be called `Tuvan based on Russian`.

Versions sorting for iPhone:
* tyv-3-rows.yaml
* tyv-4-rows.yaml

For iPad keyboard versions there is only 1 version, because there are enough space to put Tuvan letters.

## Tuvan macOS

Keyboard uses swapping/replacing less frequent letters (ФЩЦ) to ӨҢҮ letters, making less frequent letters accessible via `Option` (aka `ALT`).

Ң sits in place of Щ. Both letters have the same descender (tail), which makes it easy to remember. This keeps Г and Ш in their usual Russian positions, so the rest of the layout stays identical to ЙЦУКЕН:

```
Russian: й ц у к е н г ш щ з х ъ
Tuvan:   й ү у к е н г ш ң з х ъ
```

The replaced letters stay available via `Option`: Ц (on Ү), Щ (on Ң), Ф (on Ө).

# Tuvan keyNames

I have translated this using the most common phrases and a soft, commanding (request) way as Tuvans usually prefer.
