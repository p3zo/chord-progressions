from chord_progressions.rhythm import get_euclidean_sequence
from chord_progressions.utils import is_circular_match


def test_get_euclidean_sequence():

    eleven_four = [1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0]
    eleven_five = [1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 0]
    twelve_five = [1, 0, 0, 1, 0, 1, 0, 0, 1, 0, 1, 0]
    thirteen_five = [1, 0, 0, 1, 0, 1, 0, 0, 1, 0, 1, 0, 0]
    sixteen_five = [1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0]

    assert is_circular_match(get_euclidean_sequence(4, 3), [1, 0, 1, 1])
    assert is_circular_match(get_euclidean_sequence(5, 2), [1, 0, 1, 0, 0])
    assert is_circular_match(get_euclidean_sequence(5, 3), [1, 0, 1, 0, 1])
    assert is_circular_match(get_euclidean_sequence(6, 5), [1, 0, 1, 1, 1, 1])
    assert is_circular_match(get_euclidean_sequence(7, 3), [1, 0, 1, 0, 1, 0, 0])
    assert is_circular_match(get_euclidean_sequence(7, 5), [1, 1, 1, 0, 1, 1, 0])
    assert is_circular_match(get_euclidean_sequence(8, 3), [1, 0, 0, 1, 0, 0, 1, 0])
    assert is_circular_match(get_euclidean_sequence(8, 5), [1, 0, 1, 1, 0, 1, 1, 0])
    assert is_circular_match(get_euclidean_sequence(8, 7), [1, 0, 1, 1, 1, 1, 1, 1])
    assert is_circular_match(get_euclidean_sequence(9, 4), [1, 0, 1, 0, 1, 0, 1, 0, 0])
    assert is_circular_match(get_euclidean_sequence(9, 5), [1, 0, 1, 0, 1, 0, 1, 0, 1])
    assert is_circular_match(get_euclidean_sequence(11, 4), eleven_four)
    assert is_circular_match(get_euclidean_sequence(11, 5), eleven_five)
    assert is_circular_match(get_euclidean_sequence(12, 5), twelve_five)
    assert is_circular_match(get_euclidean_sequence(13, 5), thirteen_five)
    assert is_circular_match(get_euclidean_sequence(16, 5), sixteen_five)
