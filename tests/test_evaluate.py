from chord_progressions.chord import Chord
from chord_progressions.evaluate import get_evenness, get_interval_class_vector

EXPECTATIONS = [
    {"notes": ["C4"], "icv": [0, 0, 0, 0, 0, 0], "evenness": 0},  # unison
    {"notes": ["C4", "C#4"], "icv": [1, 0, 0, 0, 0, 0], "evenness": 0.51},  # semitone
    {
        "notes": ["C4", "D#4"],  # minor third
        "icv": [0, 0, 1, 0, 0, 0],
        "evenness": 1.41,
    },
    {
        "notes": ["C4", "E4"],  # major third
        "icv": [0, 0, 0, 1, 0, 0],
        "evenness": 1.73,
    },
    {
        "notes": ["D4", "A5"],  # perfect fourth
        "icv": [0, 0, 0, 0, 1, 0],
        "evenness": 1.93,
    },
    {
        "notes": ["D4", "E5", "D#6", "F#7"],  # major-second tetracluster 2
        "icv": [2, 2, 1, 1, 0, 0],
        "evenness": 6.18,
    },
    {
        "notes": ["F2", "B2", "D3", "G#3"],  # diminished seventh
        "icv": [0, 0, 4, 0, 0, 2],
        "evenness": 9.66,
    },
]


def test_get_interval_class_vector():

    for ex in EXPECTATIONS:
        assert get_interval_class_vector(Chord(ex["notes"])) == ex["icv"]


def test_get_evenness():

    tolerance = 0.01

    for ex in EXPECTATIONS:
        assert get_evenness(ex["icv"]) - ex["evenness"] < tolerance
