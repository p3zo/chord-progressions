import pytest

from chord_progressions.chord import Chord


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
