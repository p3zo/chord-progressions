import pytest
from chord_progressions.chord import Chord
from chord_progressions.progression import (
    Progression,
    duration_to_seconds,
    seconds_to_duration,
)

TWO_CHORDS = [Chord(["C2", "A4", "G6"]), Chord(["C-1", "A4", "G9"])]


def test_instantiate_progression():
    p = Progression(chords=TWO_CHORDS)
    assert len(p) == len(TWO_CHORDS)

    failing_inputs = [
        "a",
        [1, 2, 3],
        [[1, 2, 3], [4, 5, 6]],
        ["E4", "C4"],
        [["E4", "C4"], ["G10"]],
        [["E4", "C4"], "G4"],
    ]
    with pytest.raises(Exception):
        for arg in failing_inputs:
            assert Progression(arg)

    valid_inputs = [[["E4", "C4"], ["G4", "A4", "B5"]]]
    for arg in valid_inputs:
        assert Progression(arg)

    p = Progression(["E4", "C4"], durations=["1m", "2m"])
    assert p.durations == ["1m", "2m"]


def test_get_new_solution():
    p = Progression(chords=TWO_CHORDS)
    p2 = p.get_new_solution()

    assert p.chords[0].id != p2.chords[0].id
    assert p.chords[1].id != p2.chords[1].id

    # Durations should be preserved
    p3 = Progression(chords=TWO_CHORDS, durations=["1m", "2m"])
    assert p3.get_new_solution().durations == ["1m", "2m"]


def test_get_addition():
    p = Progression(chords=TWO_CHORDS)
    p2 = p.get_addition()

    # make sure ids are preserved for existing chords
    assert p[0].id == p2[0].id
    assert p[1].id == p2[1].id

    assert len(p) + 1 == len(p2)

    # Durations should be preserved
    p3 = Progression(chords=TWO_CHORDS, durations=["1m", "2m"])
    assert p3.get_addition().durations == ["1m", "2m", "1m"]


def test_duration_to_seconds():
    assert duration_to_seconds("4n", 120) == 0.5
    assert duration_to_seconds("2n", 120) == 1.0
    assert duration_to_seconds("1m", 120) == 2.0


def test_seconds_to_duration():
    assert seconds_to_duration(0.0001, 120) == "8n"
    assert seconds_to_duration(0.5, 120) == "4n"
    assert seconds_to_duration(1, 120) == "2n"
    assert seconds_to_duration(1.5, 120) == "2n."
    assert seconds_to_duration(2.0, 120) == "1m"
    assert seconds_to_duration(4.0, 120) == "2m"
    assert seconds_to_duration(100.0, 120) == "2m"
