from chord_progressions.chord import get_template_from_notes
from chord_progressions.solver import (
    get_all_rotations_of_template,
    get_n_common_ones,
    get_n_max_matches_between_templates,
    get_notes_from_template_range,
    get_possible_rotations,
    get_template_str,
    high_enough_match,
    select_chords,
    template_meets_constraints,
)


def test_get_template_str():
    t1 = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    t2 = [1, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0]

    assert get_template_str(t1) == "111111111111"
    assert get_template_str(t2) == "100100001000"


def test_template_meets_constraints():

    pct_notes_common = 1

    t1 = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    t2 = [0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0]
    t3 = [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

    t4 = get_template_from_notes(["E2", "B2", "F#3", "G#3", "C#5", "A#5"])
    t5 = get_template_from_notes(["E4", "F#4", "A4", "C5", "D5"])

    """
    2 matches when not rotated:
        t4: [0, 1, 0, 0, 1, 0, 1, 0, 1, 0, 1, 1]
        t5: [1, 0, 1, 0, 1, 0, 1, 0, 0, 1, 0, 0]

    5 matches when t4 is rotated 8 places:
        t4: [1, 0, 1, 0, 1, 0, 1, 1, 0, 1, 0, 0]
        t5: [1, 0, 1, 0, 1, 0, 1, 0, 0, 1, 0, 0]
    """

    assert template_meets_constraints(
        template=t2,
        pct_notes_common=pct_notes_common,
        prev_rotation=t1,
        next_rotation=None,
    )

    assert template_meets_constraints(
        template=t3,
        pct_notes_common=pct_notes_common,
        prev_rotation=t1,
        next_rotation=None,
    )

    assert template_meets_constraints(
        template=t3,
        pct_notes_common=pct_notes_common,
        prev_rotation=t2,
        next_rotation=None,
    )

    assert template_meets_constraints(
        template=t4,
        pct_notes_common=pct_notes_common,
        prev_rotation=t5,
        next_rotation=None,
    )


def test_select_chords():
    n_chords = 50

    chords = select_chords(
        n_chords=n_chords,
    )

    assert len(chords) == n_chords


def test_get_all_rotations_of_template():

    template = [1, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0]

    rotations = get_all_rotations_of_template(template)

    assert len(rotations) == 12
    assert [1, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0] in rotations
    assert [0, 1, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0] in rotations
    assert [0, 0, 1, 0, 0, 1, 0, 0, 0, 1, 0, 0] in rotations
    assert [0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 1, 0] in rotations
    assert [0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 1] in rotations
    assert [1, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0] in rotations
    assert [0, 1, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0] in rotations
    assert [0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 1, 0] in rotations
    assert [0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 1] in rotations
    assert [1, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0] in rotations
    assert [0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0] in rotations
    assert [0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 1] in rotations


def test_get_n_common_ones():

    template_1 = [1, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0]
    template_2 = [1, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0]

    template_3 = [0, 1, 1, 1, 1, 0, 0, 1, 0, 0, 0, 0]

    ones = [1] * 12
    zeros = [0] * 12

    assert get_n_common_ones(template_1, template_2) == 3
    assert get_n_common_ones(template_1, template_3) == 2
    assert get_n_common_ones(template_1, ones) == 3
    assert get_n_common_ones(template_1, zeros) == 0
    assert get_n_common_ones(ones, ones) == 12
    assert get_n_common_ones(zeros, zeros) == 0


def test_high_enough_match():

    num = 2
    denom_1 = 2
    denom_2 = 2
    thresh = 1

    assert high_enough_match(num, denom_1, denom_2, thresh)

    num = 0
    denom_1 = 2
    denom_2 = 2
    thresh = 1

    assert not high_enough_match(num, denom_1, denom_2, thresh)


def test_get_n_max_matches_between_templates():

    template_1 = [1, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0]
    template_1_rotated = [0, 1, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0]
    template_2 = [1] * 12
    template_3 = [0] * 12
    template_4 = [1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0]
    template_5 = [0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1]

    assert get_n_max_matches_between_templates(template_1, template_1_rotated) == 3
    assert get_n_max_matches_between_templates(template_1, template_2) == 3
    assert get_n_max_matches_between_templates(template_1, template_3) == 0
    assert get_n_max_matches_between_templates(template_2, template_3) == 0
    assert get_n_max_matches_between_templates(template_1, template_4) == 2
    assert get_n_max_matches_between_templates(template_4, template_5) == 6


def test_get_possible_rotations():

    template = [0, 1, 0, 1]

    prev_rotation = [0, 1, 1, 0]
    next_rotation = [1, 0, 0, 1]
    surrounding_rotations = [prev_rotation, next_rotation]

    pct_notes_common = 1

    possible = get_possible_rotations(template, surrounding_rotations, pct_notes_common)
    assert not possible


def test_get_notes_from_template_range():
    get_notes_from_template_range([1, 0, 0, 0, 1], 60) == ["C4", "E4"]
    get_notes_from_template_range([1, 0, 0, 1, 0], 48) == ["C3", "D#3"]
