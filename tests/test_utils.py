from chord_progressions.utils import is_circular_match, shift_arr_by_one


def test_shift_arr_by_one():

    assert shift_arr_by_one([1, 2, 3]) == [3, 1, 2]

    template = [1, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0]
    expected = [0, 1, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0]
    assert shift_arr_by_one(template) == expected

    assert shift_arr_by_one([1]) == [1]


def test_is_circular_match():
    assert is_circular_match([1, 2, 3], [3, 1, 2])
    assert is_circular_match([0, 0, 0], [0, 0, 0])
    assert is_circular_match([0], [0])
