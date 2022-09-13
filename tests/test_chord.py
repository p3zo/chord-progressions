from chord_progressions.chord import Chord, get_midi_nums_list_from_midi_nums_str


def test_get_template_from_notes():
    expectations = [
        {"notes": ["C-1", "A4", "G9"], "template": [1, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0]}
    ]
    for ex in expectations:
        assert Chord(ex["notes"]).template == ex["template"]


def test_get_midi_nums_list_from_midi_nums_str():
    expectations = [
        {"midi_nums_str": "60-48_62-50", "midi_nums_list": [[60, 48], [62, 50]]},
        {"midi_nums_str": "60-48_", "midi_nums_list": [[60, 48]]},
        {"midi_nums_str": "60-48_a", "midi_nums_list": [[60, 48]]},
    ]
    for ex in expectations:
        assert (
            get_midi_nums_list_from_midi_nums_str(ex["midi_nums_str"])
            == ex["midi_nums_list"]
        )
