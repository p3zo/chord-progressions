from uuid import uuid4

from chord_progressions.evaluate import evaluate_notes
from chord_progressions.pitch import get_midi_num_from_note, get_note_from_midi_num
from chord_progressions.type_templates import (
    get_template_from_notes,
    get_type_from_midi_nums,
    get_type_num_from_type,
)

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

        midi_nums = sorted(list(set(midi_nums)))
        self.midi_nums = midi_nums

        self.duration = duration or 1

        chord_type = get_type_from_midi_nums(midi_nums)
        self.type = chord_type
        self.typeId = get_type_num_from_type(chord_type)

        notes = [get_note_from_midi_num(n) for n in midi_nums]
        self.notes = notes
        self.metrics = evaluate_notes(notes)
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
