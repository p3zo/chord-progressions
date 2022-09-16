from uuid import uuid4

from chord_progressions import logger
from chord_progressions.evaluate import evaluate_notes_list
from chord_progressions.pitch import (
    get_midi_num_from_note,
    get_note_from_midi_num,
    get_note_list,
    get_pitch_class_from_midi_num,
    get_pitch_class_from_note,
)
from chord_progressions.type_templates import TYPE_TEMPLATES
from chord_progressions.utils import is_circular_match

NoteList = list[str]
MidiNumList = list[int]


class Chord:
    """A set of unique notes with duration.

    Parameters
    ----------
    notes: list[Chord], default []
        The set of notes in the chord. Can be specified as a list of midi numbers or as a list of note names.
            e.g. Chord([60, 64, 67])
            e.g. Chord(["C4", "E4", "G4"])

    duration: int, default 1
        The duration of the chord, specified in seconds.
    """

    def __init__(self, notes: list = [], duration: int = 1, id: str = None):
        if isinstance(notes, list) and len(notes) > 0 and isinstance(notes[0], str):
            notes = [get_midi_num_from_note(n) for n in notes]

        self.init_from_midi_nums(midi_nums=notes, duration=duration, id=id)

    def init_from_midi_nums(
        self, midi_nums: MidiNumList = [], duration: int = 1, id: str = None
    ):
        if any([i < 0 or i > 128 for i in midi_nums]):
            raise ValueError("The valid range of midi numbers is 0 to 128")

        self.midi_nums = sorted(list(set(midi_nums)))

        self.duration = duration or 1

        chord_type = get_type_from_midi_nums(midi_nums)
        self.type = chord_type
        self.typeId = get_type_num_from_type(chord_type)

        notes = [get_note_from_midi_num(n) for n in midi_nums]
        self.notes = notes
        self.metrics = evaluate_notes_list(notes)
        self.template = get_template_from_notes(notes)

        if not id:
            id = str(uuid4())
        self.id = id

    def __repr__(self):
        return "Chord " + self.to_string()

    def to_string(self):
        return str(self.to_json())

    def to_json(self):
        return {
            "id": self.id,
            "midi_nums": self.midi_nums,
            "duration": self.duration,
            "type": self.type,
            "typeId": self.typeId,
            "notes": self.notes,
            "metrics": self.metrics,
        }


def get_template_from_pitch_classes(pcs):
    """e.g. [0, 4, 7] -> [1, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0]"""
    template = [0] * 12

    for ix in pcs:
        template[ix] = 1

    return template


def get_template_from_notes(notes):
    """e.g. ["C4", "E4", "G4"] -> [1, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0]"""
    pitch_classes = [get_pitch_class_from_note(n) for n in notes]

    return get_template_from_pitch_classes(pitch_classes)


def get_template_from_midi_nums(midi_nums):
    """e.g. [48, 60] -> [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]"""
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
    """e.g. "60-48_62-50" -> [[60, 48], [62, 50]]
    If any chord in `midi_nums_str` is invalid, returns an empty string for that chord"""
    midi_nums_list = []
    for m in midi_nums_str.split("_"):
        try:
            midi_nums_list.append([int(i) for i in m.split("-")])
        except:
            pass

    return midi_nums_list


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


def get_type_from_midi_nums(midi_nums):
    """
    Returns the first exact template match

    e.g. [48, 60] -> "unison"
    """
    notes = [get_note_from_midi_num(n) for n in midi_nums]
    return get_type_from_notes(notes)


def get_types_from_notes_list(notes_list):
    """
    Returns the first exact template match for each note list

    e.g. [["C4", "C3"], ["C4", "E3"]] -> ["unison", "major third"]

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
    """e.g. [1, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0] -> ["C", "E", "G"]"""
    all_notes = get_note_list(note_range_low, note_range_high)

    notes = [all_notes[ix] if is_onset else 0 for ix, is_onset in enumerate(template)]

    return [n for n in notes if n]
