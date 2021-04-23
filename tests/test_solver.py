from chord_progressions.chord import chord_is_of_type, get_template_from_notes
from chord_progressions.solver import (
    get_all_rotations_of_template,
    get_n_common_ones,
    get_n_max_matches_between_templates,
    get_possible_rotations,
    high_enough_match,
    select_chords,
    template_meets_constraints,
)


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
        preceding_rotation=t1,
        succeeding_rotation=None,
    )

    assert template_meets_constraints(
        template=t3,
        pct_notes_common=pct_notes_common,
        preceding_rotation=t1,
        succeeding_rotation=None,
    )

    assert template_meets_constraints(
        template=t3,
        pct_notes_common=pct_notes_common,
        preceding_rotation=t2,
        succeeding_rotation=None,
    )

    assert template_meets_constraints(
        template=t4,
        pct_notes_common=pct_notes_common,
        preceding_rotation=t5,
        succeeding_rotation=None,
    )


## TODO: fix this test after bringing upstream changes into select_chords
# def test_select_chords():

#     n_segments = 50
#     pct_notes_common = 0
#     allowed_chord_types = ["major chord", "minor chord"]
#     first_chord = None
#     existing_chords = None
#     existing_types = None
#     locks = "0" * 6
#     first_chord = None
#     adding = False
#     melody_notes = None
#     melody_times = None
#     melody_chord_placements = None

#     selected_types, selected_chords, constraints_relaxed = select_chords(
#         n_segments=n_segments,
#         pct_notes_common=pct_notes_common,
#         allowed_chord_types=allowed_chord_types,
#         first_chord=first_chord,
#         existing_chords=existing_chords,
#         existing_types=existing_types,
#         locks=locks,
#         adding=adding,
#         note_range_high=108,
#         note_range_low=21,
#         melody_notes=melody_notes,
#         melody_times=melody_times,
#         melody_chord_placements=melody_chord_placements,
#     )

#     assert len(selected_chords) == n_segments
#     assert len(selected_types) == n_segments

#     for chord_type, chord in zip(selected_types, selected_chords):
#         assert chord_is_of_type(chord, chord_type)


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

    preceding_rotation = [0, 1, 1, 0]
    succeeding_rotation = [1, 0, 0, 1]
    surrounding_rotations = [preceding_rotation, succeeding_rotation]

    pct_notes_common = 1

    possible = get_possible_rotations(template, surrounding_rotations, pct_notes_common)
    assert not possible
