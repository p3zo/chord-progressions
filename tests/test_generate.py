from chord_progressions.solver import (
    get_all_rotations_of_template,
    get_n_common_ones,
    get_n_max_matches_between_templates,
    high_enough_match,
)


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
