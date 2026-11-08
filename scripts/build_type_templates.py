"""
Prints the TYPE_TEMPLATES entries for the classes in Ladma's list of the 351 non-empty pitch class
set classes (12-tone equal temperament, under transposition) that TYPE_TEMPLATES does not have yet.

    python scripts/build_type_templates.py

The output is appended to the end of TYPE_TEMPLATES so that existing type ids do not change.
Existing names were edited by hand and are left as they are.

Classes without a name on the page take the name of their transpositions. Classes with no names
at all are named after their pitch classes, e.g. "pitch-class set 0-1-5".
"""

import html
import re
import urllib.request

from chord_progressions.type_templates import TYPE_TEMPLATES

# The `id_` suffix serves the original page without the Wayback Machine toolbar
SOURCE_URL = "https://web.archive.org/web/20221116234056id_/https://vladimir_ladma.sweb.cz/english/music/structs/mus_rot.htm"

# e.g. "  15  4 12 000000001111  1 1 1( 9)    321000 : Name"
CLASS_ROW = re.compile(r"^\s*\d+\s+\d+\s+\d+\s+([01]{12})\s.*?:(.*)$")
# e.g. "   0/0123  1 1 1( 9)    c,c#,d,d#   : Name"
TRANSPOSITION_ROW = re.compile(r"^\s*\d+/\S+\s.*?:(.*)$")


def normalize_name(name):
    """e.g. "Italian sixth, Incomplete Dominant-seventh Chord.1" -> "italian sixth|incomplete dominant-seventh chord 1" """
    name = name.strip().lower().replace('"', "'")
    name = re.sub(r"\s*/\s*", " / ", name)
    name = re.sub(r"\.(\d)$", r" \1", name)
    return "|".join(part.strip() for part in name.split(","))


def parse_classes(page):
    """Returns (template, class name, [transposition names]) for each class on the page."""
    text = html.unescape(re.sub(r"<[^>]+>", "", page))
    classes = []

    for block in text.split("------------"):
        class_rows = [m for m in map(CLASS_ROW.match, block.splitlines()) if m]
        if not class_rows:
            continue
        if len(class_rows) != 1:
            raise ValueError(f"Expected one class row per block, got {len(class_rows)}")

        binary, class_name = class_rows[0].groups()
        transposition_names = [
            m.group(1).strip()
            for m in map(TRANSPOSITION_ROW.match, block.splitlines())
            if m and m.group(1).strip()
        ]

        # The page writes pitch class 0 as the rightmost bit; templates put it first
        classes.append((binary[::-1], class_name.strip(), transposition_names))

    return classes


def get_name(template, class_name, transposition_names):
    if class_name:
        return normalize_name(class_name)

    if transposition_names:
        names = [normalize_name(n) for n in transposition_names]
        return "|".join(dict.fromkeys(names))

    pitch_classes = [str(ix) for ix, bit in enumerate(template) if bit == "1"]
    return "pitch-class set " + "-".join(pitch_classes)


def main():
    with urllib.request.urlopen(SOURCE_URL) as response:
        page = response.read().decode("latin-1")

    classes = parse_classes(page)
    if len(classes) != 352:
        raise ValueError(f"Expected 352 classes, got {len(classes)}")

    existing_templates = set(TYPE_TEMPLATES.values())

    for template, class_name, transposition_names in classes:
        if template == "0" * 12 or template in existing_templates:
            continue

        name = get_name(template, class_name, transposition_names)
        if name in TYPE_TEMPLATES:
            raise ValueError(f"{name} is already a type with a different template")

        print(f'    "{name}": "{template}",')


if __name__ == "__main__":
    main()
