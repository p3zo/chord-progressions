import numpy as np
import pytest
from chord_progressions.evaluate import get_set_tension
from chord_progressions.progression_measures import (
    get_contour_fit,
    get_final_lengthening,
    get_mean_tension,
    get_metric_conflict,
    get_pitch_class_emphasis,
    get_transposed_repetition,
    returns_to_opening,
)

C, F, G = [0, 4, 7], [5, 9, 0], [7, 11, 2]
CLUSTER = [0, 1, 2]


def test_mean_tension_weights_chords_by_length():
    equal = get_mean_tension([C, CLUSTER], [4, 4])
    assert equal == pytest.approx((get_set_tension(C) + get_set_tension(CLUSTER)) / 2)
    assert get_mean_tension([C, CLUSTER], [4, 12]) > equal


def test_pitch_class_emphasis_counts_sounding_time():
    emphasis = get_pitch_class_emphasis([C, G], [3, 1])
    assert emphasis.sum() == pytest.approx(1)
    # G sounds in both chords, C and E only in the first, B and D only in the second.
    assert emphasis[7] > emphasis[0] == emphasis[4] > emphasis[11] == emphasis[2]
    assert emphasis[1] == 0


def test_contour_fit_measures_shape_over_time():
    rise_and_fall = ((0, 0.5, 1), (0, 1, 0))
    tensions = [0.0, 1.0, 0.0]
    assert get_contour_fit(tensions, [1, 1, 1], *rise_and_fall) == pytest.approx(1)
    inverted = get_contour_fit([1.0, 0.0, 1.0], [1, 1, 1], *rise_and_fall)
    assert inverted == pytest.approx(-1)
    # Level and scale do not matter, only shape.
    scaled = get_contour_fit([5.0, 9.0, 5.0], [1, 1, 1], *rise_and_fall)
    assert scaled == pytest.approx(1)
    assert get_contour_fit([0.3, 0.3, 0.3], [1, 1, 1], *rise_and_fall) == 0
    # Lengths move each chord's midpoint: a long first chord pushes the peak late.
    build = ((0, 1), (0, 1))
    assert get_contour_fit([0.0, 1.0], [6, 2], *build) == pytest.approx(1)
    assert get_contour_fit(tensions, [6, 1, 1], *rise_and_fall) < 1


@pytest.mark.parametrize(
    "beats, conflict",
    [
        ([4, 4, 4, 4], 0),
        ([2, 2, 2, 2], 0),
        ([1.5, 2.5, 4], 1 / 3),  # the second chord starts off the beat
        ([1, 2, 1], 0.5 / 3),  # a half note starting on beat 2
        ([1, 1, 2], 0),  # a half note starting on beat 3
    ],
)
def test_metric_conflict_in_four_four(beats, conflict):
    assert get_metric_conflict(beats) == pytest.approx(conflict)


def test_final_lengthening_compares_the_last_chord_with_the_mean():
    assert get_final_lengthening([4, 4, 4, 4]) == 1
    assert get_final_lengthening([2, 2, 8]) == 2
    assert get_final_lengthening([4, 4, 1]) < 1


def test_transposed_repetition_finds_sequences_but_not_stasis():
    # C F, then D G and E A: the pair restated a step up, twice.
    sequence = [C, F, [2, 6, 9], [7, 11, 2], [4, 8, 11], [9, 1, 4]]
    assert get_transposed_repetition(sequence) == 1
    assert get_transposed_repetition([C, C, C, C]) == 0
    assert get_transposed_repetition([C, F, G, CLUSTER]) < 1
    assert get_transposed_repetition([C, F]) == 0


def test_returns_to_opening():
    assert returns_to_opening([C, F, G, C])
    assert not returns_to_opening([C, F, G])
    assert not returns_to_opening([C, C, C])
    assert not returns_to_opening([C, C])


@pytest.mark.parametrize(
    "measure",
    [
        lambda beats: get_mean_tension([C, F], beats),
        lambda beats: get_pitch_class_emphasis([C, F], beats),
        get_metric_conflict,
        get_final_lengthening,
    ],
)
def test_lengths_must_be_positive(measure):
    with pytest.raises(ValueError):
        measure([4, 0])


def test_emphasis_needs_one_length_per_chord():
    with pytest.raises(ValueError):
        get_pitch_class_emphasis([C, F, G], np.array([4, 4]))
