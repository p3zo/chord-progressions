from uuid import uuid4

from chord_progressions import logger
from chord_progressions.pitch import (
    get_note_from_midi_num,
    get_note_list,
    get_pitch_class_from_midi_num,
    get_pitch_class_from_note,
)
from chord_progressions.type_templates import TYPE_TEMPLATES
from chord_progressions.utils import is_circular_match


def get_template_from_pitch_classes(pcs):
    template = [0] * 12

    for ix in pcs:
        template[ix] = 1

    return template


def get_template_from_notes(notes):
    """e.g. ["C4", "C3"] -> [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]"""
    pitch_classes = [get_pitch_class_from_note(n) for n in notes]

    return get_template_from_pitch_classes(pitch_classes)


def get_template_from_midi_nums(midi_nums):
    """e.g. ["48", "60"] -> [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]"""
    pitch_classes = [get_pitch_class_from_midi_num(n) for n in midi_nums]

    return get_template_from_pitch_classes(pitch_classes)


def get_template_from_template_str(template_str):
    """e.g. "101010101010" -> [1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0]"""
    return [int(i) for i in list(template_str)]


def get_type_from_type_num(num):
    """Takes the id of a chord type and returns its name"""
    return list(TYPE_TEMPLATES)[num]


def get_types_from_type_num_str(type_num_str):
    """Takes a type_num_str and returns a list of type names"""
    types = []

    for num in type_num_str.split("_"):
        if num == "":
            types.append("")
        else:
            types.append(get_type_from_type_num(int(num)))

    return types


def get_type_num_from_type(chord_type):
    """Takes the name of a chord type and returns its id"""
    if not chord_type:
        return None

    return list(TYPE_TEMPLATES).index(chord_type)


def get_notes_from_midi_nums_str(midi_nums_str):
    """e.g. "60-48" -> ["C4", "C3"]"""
    return [get_note_from_midi_num(s) for s in midi_nums_str.split("-")]


def get_notes_list_from_midi_nums_str(midi_nums_str):
    """e.g. "60-48_62-50" -> [["C4", "C3"], ["D4", "E3"]]"""
    return [get_notes_from_midi_nums_str(s) for s in midi_nums_str.split("_")]


def get_midi_nums_list_from_midi_nums_str(midi_nums_str):
    """e.g. "60-48_62-50" -> [[60, 48], [62, 50]]"""
    return [m.split("-") for m in midi_nums_str.split("_")]


def get_durations_from_duration_str(dur_str):
    """
    Takes a duration string and returns an array of durations

    e.g. "1m_1m_1m" -> ["1m", "1m", "1m"]
    """
    return dur_str.split("_")


def notes_match_chord_type(notes, chord_type):
    """Returns true if any rotation of `notes` fit `chord_type`"""
    return is_circular_match(
        get_template_from_notes(notes),
        get_template_from_template_str(TYPE_TEMPLATES[chord_type]),
    )


def get_type_from_notes(notes):
    """
    Returns the first exact template match

    e.g. ["C4", "C3"] -> "unison"

    TODO:
        - find partial matches as well
        - optimize
    """
    for chord_type in list(TYPE_TEMPLATES):
        if notes_match_chord_type(notes, chord_type):
            return chord_type

    logger.debug(f"No type template matched chord: {notes}")
    return ""


def get_types_from_notes_list(notes_list):
    """
    Returns the first exact template match for each note list

    TODO:
        - find partial matches as well
        - optimize
    """
    result = []

    for notes in notes_list:

        match = False

        for chord_type in list(TYPE_TEMPLATES):
            if is_circular_match(
                get_template_from_notes(notes),
                get_template_from_template_str(TYPE_TEMPLATES[chord_type]),
            ):
                match = True
                result.append(chord_type)

        if not match:
            logger.debug(f"No type template matched chord: {notes}")
            result.append("")

    return result


def get_notes_from_template(template, note_range_low, note_range_high):

    all_notes = get_note_list(note_range_low, note_range_high)

    notes = [all_notes[ix] if is_onset else 0 for ix, is_onset in enumerate(template)]

    return [n for n in notes if n]


def serialize_chord(notes, chord_type, duration, chord_metrics, locked, ix):
    return {
        "id": str(uuid4()),
        "ix": ix,
        "type": chord_type,
        "duration": duration,
        "typeId": get_type_num_from_type(chord_type),
        "notes": notes,
        "locked": str(locked),
        "metrics": chord_metrics,
    }


def serialize_chords(notes_list, chord_types, durations, chord_metrics, chord_locks):
    chord_dicts = []

    for ix, (chord, chord_type, duration) in enumerate(
        list(zip(notes_list, chord_types, durations))
    ):

        locked = list(chord_locks)[ix]

        chord_dicts.append(
            serialize_chord(chord, chord_type, duration, chord_metrics[ix], locked, ix)
        )

    return chord_dicts
