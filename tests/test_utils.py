from chord_progressions.utils import (
    is_circular_match,
    round_to_base,
    shift_arr_by_one,
)


def test_shift_arr_by_one():

    assert shift_arr_by_one([1, 2, 3]) == [3, 1, 2]

    template = [1, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0]
    expected = [0, 1, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0]
    assert shift_arr_by_one(template) == expected

    assert shift_arr_by_one([1]) == [1]


def test_round_to_base():
    assert round_to_base(1.3, 0.5) == 1.5
    assert round_to_base(1.3, 0.25) == 1.25
    assert round_to_base(1.5, 0.25) == 1.5
    assert round_to_base(1.5, 1) == 2
    assert round_to_base(1, 1) == 1


def test_is_circular_match():
    assert is_circular_match([1, 2, 3], [3, 1, 2])
    assert is_circular_match([0, 0, 0], [0, 0, 0])
    assert is_circular_match([0], [0])
