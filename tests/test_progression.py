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


def test_key_of_major_progression():
    # I - IV - V7 - I in C
    p = Progression([[48, 64, 67], [53, 65, 69], [55, 59, 65], [48, 64, 67, 72]])
    assert p.key == "C major"


def test_key_of_minor_progression():
    # i - iv - V - i in A minor
    p = Progression([[45, 60, 64], [50, 65, 69], [52, 59, 68], [45, 60, 64, 69]])
    assert p.key == "A minor"


def test_key_follows_transposition():
    chords = [[48, 64, 67], [53, 65, 69], [55, 59, 65], [48, 64, 67, 72]]
    p = Progression([[n + 6 for n in c] for c in chords])
    assert p.key == "F# major"


def test_key_weighs_chords_by_duration():
    # C major and A minor triads; whichever lasts longer decides the key
    chords = [[48, 64, 67], [45, 60, 64]]
    assert Progression(chords, durations=["2m", "4n"]).key == "C major"
    assert Progression(chords, durations=["4n", "2m"]).key == "A minor"


def test_key_of_empty_progression_raises():
    with pytest.raises(ValueError):
        Progression().key
