from uuid import uuid4

from chord_progressions import logger
from chord_progressions.evaluate import evaluate_notes
from chord_progressions.io.audio import mk_chord_buffer, save_audio_buffer
from chord_progressions.io.midi import get_midi_from_chord
from chord_progressions.pitch import get_midi_num_from_note, get_note_from_midi_num
from chord_progressions.type_templates import (
    get_template_from_notes,
    get_type_from_midi_nums,
    get_type_num_from_type,
)

NoteList = list[str]
MidiNumList = list[int]


class Chord:
    """A set of unique notes.

    Parameters
    ----------
    notes: list[Chord], default []
        The set of notes in the chord. Can be specified as a list of midi numbers or as a list of note names.
            e.g. Chord([60, 64, 67])
            e.g. Chord(["C4", "E4", "G4"])
    """

    def __init__(self, notes: list = [], id: str = None):
        if isinstance(notes, list) and len(notes) > 0 and isinstance(notes[0], str):
            notes = [get_midi_num_from_note(n) for n in notes]

        self.init_from_midi_nums(midi_nums=notes, id=id)

    def init_from_midi_nums(self, midi_nums: MidiNumList = [], id: str = None):
        if any([i < 0 or i > 128 for i in midi_nums]):
            raise ValueError("The valid range of midi numbers is 0 to 128")

        midi_nums = sorted(list(set(midi_nums)))
        self.midi_nums = [int(i) for i in midi_nums]

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
            "type": self.type,
            "typeId": self.typeId,
            "notes": self.notes,
            "metrics": self.metrics,
        }

    def to_audio(self, outpath=None, n_overtones=4):
        audio_buffer = mk_chord_buffer(self.notes, 1, n_overtones)

        # TODO: create outpath from random word + datetime if not provided? add flag to opt for this?
        if outpath:
            save_audio_buffer(audio_buffer, outpath)
            logger.info(f"Audio saved to {outpath}")

    def to_midi(self, outpath=None):
        mid = get_midi_from_chord(self.chords, 1, 120, "-".join(self.notes))
        if outpath:
            mid.filename = outpath
            mid.save(outpath)
            logger.info(f"Midi saved to {outpath}")
