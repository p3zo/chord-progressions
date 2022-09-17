import pytest

from chord_progressions.chord import Chord
from chord_progressions.progression import Progression

TWO_CHORDS = [Chord(["C2", "A4", "G6"]), Chord(["C-1", "A4", "G9"])]


def test_instantiate_progression():
    p = Progression(chords=TWO_CHORDS)
    assert len(p) == len(TWO_CHORDS)

    failing_args = [
        "a",
        [1, 2, 3],
        [[1, 2, 3], [4, 5, 6]],
        ["E4", "C4"],
        [["E4", "C4"], ["G10"]],
        [["E4", "C4"], "G4"],
    ]
    with pytest.raises(Exception):
        for arg in failing_args:
            assert Progression(arg)

    valid_args = [[["E4", "C4"], ["G4", "A4", "B5"]]]
    for arg in valid_args:
        assert Progression(arg)


def test_get_new_solution():
    p = Progression(chords=TWO_CHORDS)
    p2 = p.get_new_solution()

    assert p.chords[0].id != p2.chords[0].id
    assert p.chords[1].id != p2.chords[1].id


def test_get_addition():
    p = Progression(chords=TWO_CHORDS)
    p2 = p.get_addition()

    # make sure ids are preserved for existing chords
    assert p[0].id == p2[0].id
    assert p[1].id == p2[1].id

    assert len(p) + 1 == len(p2)
