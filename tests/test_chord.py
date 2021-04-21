from chord_progressions.chord import get_template_from_notes

EXPECTATIONS = [
    {"notes": ["C-1", "A4", "G9"], "template": [1, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0]}
]


def test_get_template_from_notes():
    for ex in EXPECTATIONS:
        assert get_template_from_notes(ex["notes"]) == ex["template"]
