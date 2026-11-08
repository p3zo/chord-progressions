import numpy as np
import pytest
from chord_progressions.evaluate import (
    get_evenness,
    get_fourier_coefficients,
    get_interval_class_vector,
    get_interval_class_vector_from_pitch_classes,
    get_pitch_class_voice_leading_distance,
    get_root_salience,
    get_roughness,
    get_set_tension,
    get_voice_leading_distance,
)

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
        assert get_interval_class_vector(ex["notes"]) == ex["icv"]


def test_get_evenness():
    tolerance = 0.01

    for ex in EXPECTATIONS:
        assert get_evenness(ex["icv"]) - ex["evenness"] < tolerance


C_MAJOR = [0, 4, 7]
DIATONIC = [0, 2, 4, 5, 7, 9, 11]


def test_get_interval_class_vector_from_pitch_classes():
    assert get_interval_class_vector_from_pitch_classes(C_MAJOR) == [0, 0, 1, 1, 1, 0]
    assert get_interval_class_vector_from_pitch_classes(DIATONIC) == [2, 5, 4, 3, 6, 1]
    assert get_interval_class_vector_from_pitch_classes(range(12)) == [12] * 5 + [6]


def test_set_tension_orders_fifth_triad_cluster_and_semitone():
    fifth, triad = get_set_tension([0, 7]), get_set_tension(C_MAJOR)
    cluster, semitone = get_set_tension([0, 1, 2]), get_set_tension([0, 1])
    assert fifth < triad < cluster < semitone
    assert get_set_tension([0]) == fifth


def test_fourier_coefficients_identify_even_sets():
    f = get_fourier_coefficients
    assert abs(f(DIATONIC)[4]) == pytest.approx((2 + np.sqrt(3)) / 7)
    assert abs(f([0, 4, 8])[2]) == pytest.approx(1)
    assert abs(f([0, 3, 6, 9])[3]) == pytest.approx(1)
    assert abs(f([0, 2, 4, 6, 8, 10])[5]) == pytest.approx(1)
    assert np.allclose(np.abs(f(range(12))), 0, atol=1e-12)
    # Transposition by a fifth rotates the f5 phase by 5 * 7 / 12 of a turn.
    turn = np.angle(f([7, 11, 2])[4] / f(C_MAJOR)[4]) / (2 * np.pi)
    assert (turn - (-35 / 12)) % 1 == pytest.approx(0)


@pytest.mark.parametrize(
    "a,b,distance",
    [
        ([60, 64, 67], [60, 64, 67], 0),
        ([60, 64, 67], [60, 65, 69], 3),
        ([60, 64, 67], [59, 62, 67], 3),
        ([60, 67], [60, 64, 67], 3),
        ([60], [48, 72], 24),
        ([48, 60, 64, 67], [60, 65, 69], 15),
    ],
)
def test_get_voice_leading_distance(a, b, distance):
    assert get_voice_leading_distance(a, b) == distance
    assert get_voice_leading_distance(b, a) == distance


def test_pitch_class_voice_leading_respects_octave_equivalence():
    d = get_pitch_class_voice_leading_distance
    assert d(C_MAJOR, [7, 11, 2]) == 3
    assert d(C_MAJOR, [4, 7, 11]) == 1
    assert d([11], [0]) == 1
    assert d(C_MAJOR, [1, 5, 8]) == 3
    assert d([0, 6], [5, 11]) == 2


def test_roughness_is_higher_for_close_low_intervals():
    assert get_roughness([60, 61]) > get_roughness([60, 67])
    assert get_roughness([36, 40]) > get_roughness([72, 76])
    assert get_roughness([36, 48, 55, 64]) < get_roughness([36, 40, 43, 48])
    assert get_roughness([]) == 0


def test_root_salience_finds_triad_roots():
    salience = get_root_salience(C_MAJOR)
    assert max(salience, key=salience.get) == 0
    minor = get_root_salience([9, 0, 4])
    assert max(minor, key=minor.get) == 9
    whole_tone = get_root_salience([0, 2, 4, 6, 8, 10])
    assert len(set(whole_tone.values())) == 1
