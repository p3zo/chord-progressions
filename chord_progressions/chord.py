from uuid import uuid4

from chord_progressions.type_templates import TYPE_TEMPLATES
from chord_progressions.pitch import (
    get_midi_num_from_note,
    get_note_from_midi_num,
    get_note_list,
    get_pitch_class_from_note,
)
from chord_progressions.utils import is_circular_match


def get_template_from_notes(notes):

    pitch_classes = [get_pitch_class_from_note(n) for n in notes]

    template = [0] * 12

    for ix in pitch_classes:
        template[ix] = 1

    return template


def get_template_from_template_string(template_string):
    return [int(i) for i in list(template_string)]


def get_type_from_type_num(num):
    return list(TYPE_TEMPLATES)[num]


def get_types_from_type_string(type_str):
    types = []

    for num in type_str.split("_"):
        if num == "":
            types.append("")
        else:
            types.append(get_type_from_type_num(int(num)))

    return types


def get_type_num_from_type(chord_type):
    if not chord_type:
        return None

    return list(TYPE_TEMPLATES).index(chord_type)


def get_notes_from_note_string(note_string):
    return [get_note_from_midi_num(s) for s in note_string.split("-")]


def get_chords_from_chord_string(chord_str):
    return [get_notes_from_note_string(s) for s in chord_str.split("_")]


def get_durations_from_duration_string(dur_str):
    return dur_str.split("_")


def get_chord_string_from_chords(chords):
    midi_chords = [[str(get_midi_num_from_note(n)) for n in c] for c in chords]

    return "_".join(["-".join(m) for m in midi_chords])


def chord_is_of_type(chord, chord_type):
    return is_circular_match(
        get_template_from_notes(chord),
        get_template_from_template_string(TYPE_TEMPLATES[chord_type]),
    )


def get_type_from_chord(chord):
    """
    Returns the first exact template match for the chord

    TODO:
        - find partial matches as well
        - optimize
    """
    for chord_type in list(TYPE_TEMPLATES):
        if chord_is_of_type(chord, chord_type):
            return chord_type

    print("No type template matched chord", chord)
    return ""


def get_types_from_chords(chords):
    """
    Returns the first exact template match for each chord

    TODO:
        - find partial matches as well
        - optimize
    """
    result = []

    for chord in chords:

        match = False

        for chord_type in list(TYPE_TEMPLATES):
            if is_circular_match(
                get_template_from_notes(chord),
                get_template_from_template_string(TYPE_TEMPLATES[chord_type]),
            ):
                match = True
                result.append(chord_type)

        if not match:
            print("No type template matched chord", chord)
            result.append("")

    return result


def get_possible_types_of_chord(chord):
    """Returns an array of strings with possible chord types"""
    possible_types = []

    for chord_type in list(TYPE_TEMPLATES):

        if chord_is_of_type(chord, chord_type):
            possible_types.append(chord_type)

        # TODO: look for partial matches
        # if chord_contained_in_type(chord, chord_type):
        #     possible_types.append(chord_type)

    return possible_types


# TODO: finish this
# def chord_contained_in_type(chord, chord_type):
#     return is_partial_circular_match(
#         get_template_from_notes(chord),
#         get_template_from_template_string(TYPE_TEMPLATES[chord_type]),
#     )


def get_notes_from_template(template, note_range_low, note_range_high):

    all_notes = get_note_list(note_range_low, note_range_high)

    notes = [all_notes[ix] if is_onset else 0 for ix, is_onset in enumerate(template)]

    return [n for n in notes if n]


def serialize_chord(chord, chord_type, duration, chord_metrics, locked, ix):
    return {
        "id": str(uuid4()),
        "ix": ix,
        "type": chord_type,
        "duration": duration,
        "typeId": get_type_num_from_type(chord_type),
        "notes": chord,
        "locked": str(locked),
        "metrics": chord_metrics,
    }


def serialize_chords(chords, chord_types, durations, chord_metrics, chord_locks):
    chord_dicts = []

    for ix, (chord, chord_type, duration) in enumerate(
        list(zip(chords, chord_types, durations))
    ):

        locked = list(chord_locks)[ix]

        chord_dicts.append(
            serialize_chord(chord, chord_type, duration, chord_metrics[ix], locked, ix)
        )

    return chord_dicts
