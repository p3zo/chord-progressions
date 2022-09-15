import numpy as np
from chord_progressions import logger
from chord_progressions.chord import (
    Chord,
    get_notes_from_template,
    get_template_from_midi_nums,
    get_template_from_template_str,
)
from chord_progressions.pitch import (
    get_midi_num_from_note,
    get_note_from_midi_num,
    get_pitch_class_from_note,
)
from chord_progressions.type_templates import TYPE_TEMPLATES
from chord_progressions.utils import shift_arr_by_one

# hard-code some constraints until there is a convincing use-case to make them variable
N_NOTES_MIN = 1
N_NOTES_MAX = 12
SPACING_CUTOFF = 52  # E3
MIN_SPACING = 4  # half steps


def get_n_common_ones(template_1, template_2):
    """
    Doesn't consider rotations, e.g. get_n_common_ones([1, 0, 1, 1], [0, 1, 1, 0]) = 1
    """
    one_indices_1 = [ix for ix, i in enumerate(template_1) if i == 1]
    one_indices_2 = [ix for ix, i in enumerate(template_2) if i == 1]

    return len(set(one_indices_1) & set(one_indices_2))


def get_n_max_matches_between_templates(template_1, template_2):
    """Calculate the maximum the number of matching ones that two templates could have in any rotation."""

    matches = 0

    n = get_n_common_ones(template_1, template_2)

    if n > matches:
        matches = n

    for i in range(len(template_1) - 1):

        template_1 = shift_arr_by_one(template_1)

        # TODO: is this needed?
        # for j in range(len(template_2) - 1):
        #     template_2 = shift_arr_by_one(template_2)

        n = get_n_common_ones(template_1, template_2)

        if n > matches:
            matches = n

    return matches


def high_enough_match(num, denom_1, denom_2, thresh):
    """
    Returns True if both quotients of a number divided
    by two denominators are greater than a threshold
    """

    # TODO(bug): division by 0 is possible
    if denom_1 == 0 or denom_2 == 0:
        return False

    pct_1 = num / denom_1
    pct_2 = num / denom_2

    return pct_1 >= thresh or pct_2 >= thresh


def template_meets_constraints(
    template,
    pct_notes_common,
    preceding_rotation,
    succeeding_rotation,
):
    """
    Returns True if `template`
        - has num notes between `n_notes_min` and `n_notes_max`
        - has num consecutive notes less than `n_consecutive max`
        - has at least `pct_notes_common` with both preceding & succeeding rotations
    """
    if preceding_rotation:

        n_max = get_n_max_matches_between_templates(template, preceding_rotation)

        if not high_enough_match(
            n_max, sum(template), sum(preceding_rotation), pct_notes_common
        ):
            return False

    if succeeding_rotation:

        n_max = get_n_max_matches_between_templates(template, succeeding_rotation)

        if not high_enough_match(
            n_max, sum(template), sum(succeeding_rotation), pct_notes_common
        ):
            return False

    s = sum(template)

    return not (s < N_NOTES_MIN or s < pct_notes_common or s > N_NOTES_MAX)


def select_voicing(rotation, note_range_low, note_range_high):
    """
    Places a set of pitch classes into pitch space.

    NOTE: this does not randomize the template
    TODO: fix this?
    """

    n_notes = note_range_high - note_range_low + 1
    n_templates = int(n_notes / 12)
    remainder = n_notes % 12

    possible_pitches = rotation * n_templates + rotation[:remainder]

    spaced = False
    while not spaced:
        possible_pitch_ixs = [ix for ix, i in enumerate(possible_pitches) if i == 1]

        pitch_class_assignments = {}

        while len(possible_pitch_ixs) > 0:

            ix = np.random.randint(len(possible_pitch_ixs))

            choice = possible_pitch_ixs.pop(ix)

            slot = choice % 12

            pitch_class_assignments[slot] = choice

        selected_pitches = [0] * n_notes
        for ix in set(pitch_class_assignments.values()):
            selected_pitches[ix] = 1

        selected_notes = get_notes_from_template(
            selected_pitches, note_range_low, note_range_high
        )
        voicing = [get_midi_num_from_note(n) for n in selected_notes]

        spaced = is_voicing_spaced(voicing)

    return voicing


def get_rotations_in_common(template, rotation, pct_notes_common):
    """
    Returns a list of lists with all the rotations of `template` that share
    at least `pct_notes_common` with `rotation`.
    """
    matches = []

    n = get_n_common_ones(template, rotation)

    if high_enough_match(n, sum(template), sum(rotation), pct_notes_common):
        matches.append(template)

    for i in range(len(template) - 1):

        template = shift_arr_by_one(template)

        n = get_n_common_ones(template, rotation)

        if high_enough_match(n, sum(template), sum(rotation), pct_notes_common):
            matches.append(template)

    return matches


def get_possible_rotations(template, surrounding_rotations, pct_notes_common):
    """
    Returns a list of lists with all the rotations of `template` that share at least
    `pct_notes_common` with any `surrounding_rotations`.
    """
    if not any(surrounding_rotations):
        return get_all_rotations_of_template(template)

    possible = []
    for rotation in surrounding_rotations:
        if rotation:
            for match in get_rotations_in_common(template, rotation, pct_notes_common):
                possible.append(match)

    return possible


def get_template_str(template):
    return "".join([str(i) for i in template])


def get_all_rotations_of_template(template):

    rotation_strs = set()
    rotation_strs.add(get_template_str(template))

    prev = template

    for i in range(len(template) - 1):
        rotated = shift_arr_by_one(prev)
        rotation_strs.add(get_template_str(rotated))

        prev = rotated

    return [[int(j) for j in list(i)] for i in rotation_strs]


def choose_random_template(allowed_chord_types):

    template_type = allowed_chord_types[np.random.randint(len(allowed_chord_types))]

    template = get_template_from_template_str(TYPE_TEMPLATES[template_type])

    return template, template_type


def choose_template_with_constraints(
    allowed_chord_types,
    pct_notes_common,
    preceding_rotation,
    succeeding_rotation,
):

    allowed_types = allowed_chord_types.copy()

    template, template_type = choose_random_template(allowed_types)

    while not template_meets_constraints(
        template,
        pct_notes_common,
        preceding_rotation,
        succeeding_rotation,
    ):

        allowed_types.remove(template_type)

        if len(allowed_types) == 0:
            logger.warning("No chord types meet constraints.")
            return None, None

        template, template_type = choose_random_template(allowed_types)

    return template, template_type


def select_chords(
    n_chords=5,
    pct_notes_common=0,
    note_range_low=60,
    note_range_high=108,
    allowed_chord_types=list(TYPE_TEMPLATES),
    existing_chords=None,
    locks=None,
):
    # allow all chord types if none are specified
    if len(allowed_chord_types) == 0:
        allowed_chord_types = list(TYPE_TEMPLATES)[1:]  # exclude "unknown"

    if type(locks) != str:
        locks = "0" * n_chords
    elif len(locks) != n_chords:
        logger.error(
            "`locks` has a different length from `n_chords`. Falling back to all locks."
        )
        locks = "1" * n_chords

    logger.debug(f"Locks: {locks}")

    open_ixs = [ix for ix, i in enumerate(locks) if i == "0"]
    rotations = [[]] * n_chords
    chord_notes = [[]] * n_chords

    if existing_chords:
        logger.debug(f"Existing chords: {existing_chords}")

        for ix, midi_nums in enumerate(existing_chords):
            rotations[ix] = get_template_from_midi_nums(midi_nums)
            chord_notes[ix] = midi_nums

    print(f"Indexes to fill: {open_ixs}")
    logger.debug(f"Indexes to fill: {open_ixs}")

    for ix in open_ixs:
        preceding_rotation = rotations[ix - 1] if ix > 0 else None

        succeeding_rotation = None
        if ix < n_chords - 1:
            rotation = rotations[ix + 1]
            succeeding_rotation = rotation if rotation else None

        template, chord_type = choose_template_with_constraints(
            allowed_chord_types,
            pct_notes_common,
            preceding_rotation,
            succeeding_rotation,
        )

        surrounding_rotations = [preceding_rotation, succeeding_rotation]

        possible_rotations = get_possible_rotations(
            template, surrounding_rotations, pct_notes_common
        )

        if not possible_rotations:
            logger.warning("NO POSSIBLE ROTATIONS")

        rotation = possible_rotations[np.random.randint(len(possible_rotations))]

        voicing = select_voicing(rotation, note_range_low, note_range_high)

        chord_notes[ix] = voicing
        rotations[ix] = rotation

        logger.debug(f"Selected for ix {ix}: ( {voicing}, {chord_type} )")

    return [Chord(c) for c in chord_notes]


def is_voicing_spaced(voicing):
    """Use the harmonic series spacing to inform voicing - highs closer and lows farther apart.

    Voicing is an array of midi note numbers
    """
    notes_below_c3 = sorted([n for n in voicing if n < SPACING_CUTOFF])

    spacings_below_c3 = []
    for ix, n in enumerate(notes_below_c3):
        if ix == 0:
            continue

        spacing = n - notes_below_c3[ix - 1]

        spacings_below_c3.append(spacing)

    if all([i >= MIN_SPACING for i in spacings_below_c3]):
        return True

    return False


def shuffle_voicing(notes: list[str], note_range_low: int, note_range_high: int):
    voicing = []

    note_range = range(note_range_low, note_range_high + 1)

    pitch_classes = [get_pitch_class_from_note(n) for n in notes]

    for ix, pc in enumerate(pitch_classes):
        opts = [i for i in note_range if i % 12 == pc]

        np.random.shuffle(opts)

        # if the note range doesn't include the pitch class, just return the original note
        # TODO: return a flag to indicate this happened so the client can display a warning
        if len(opts) == 0:
            voicing.append(get_midi_num_from_note(notes[ix]))

        for ix, opt in enumerate(opts):

            # prevent the same note from being used if there are other options
            # TODO: allow notes to expand & be voiced in multiple octaves?
            # TODO: allow a note voiced in multiple octaves to be collapsed into one?
            if opt in voicing and ix < len(opts) - 1:
                continue
            else:
                voicing.append(opt)
                break

    return [get_note_from_midi_num(n) for n in sorted(voicing)]
