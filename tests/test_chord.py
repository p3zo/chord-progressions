from chord_progressions.chord import Chord

EXPECTATIONS = [
    {"notes": ["C-1", "A4", "G9"], "template": [1, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0]}
]


def test_get_template_from_notes():
    for ex in EXPECTATIONS:
        assert Chord(ex['notes']).template == ex["template"]
