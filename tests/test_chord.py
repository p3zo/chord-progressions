import pytest

from chord_progressions.chord import Chord, get_midi_nums_list_from_midi_nums_str


def test_instantiate_chord():
    assert Chord().midi_nums == []

    c = Chord(["C4", "E4", "G4"])
    assert c.midi_nums == [60, 64, 67]
    assert isinstance(c.duration, int)

    with pytest.raises(ValueError):
        assert Chord([-1])

    cd = Chord(["C4", "E4", "G4"], 2)
    assert cd.midi_nums == [60, 64, 67]
    assert cd.duration == 2


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
