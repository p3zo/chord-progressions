import json

from chord_progressions import DEFAULT_BPM, logger
from chord_progressions.chord import Chord
from chord_progressions.io.audio import make_audio_progression, save_audio_buffer
from chord_progressions.io.midi import get_midi_from_progression
from chord_progressions.solver import select_chords


class Progression:
    """
    A sequence of Chords with metadata such as bpm & chord locks.

    Parameters
    ----------
    chords: list[Chord], default []
        The chords in the progression.
    locks: str, default None
        Binary string with length equal to the number of existing chords, e.g. 101011, where 1 = locked, 0 = unlocked.
        Defaults to all unlocked if not provided.
    bpm: float, default DEFAULT_BPM
        The beats per minute (BPM) of the progression.
    name: str, default ""
        The name of the progression.
    """

    def __init__(
        self,
        chords: list[Chord] = [],
        locks: str = None,
        bpm: float = DEFAULT_BPM,
        name: str = "",
    ):
        if not isinstance(chords, list):
            raise ValueError("`chords` must be a list")

        # convert a midi_nums_list to Chords
        if isinstance(chords, list) and len(chords) > 0 and isinstance(chords[0], list):
            chords = [Chord(c) for c in chords]

        self.chords = chords

        if not locks:
            locks = "0" * len(chords)
        self.locks = locks

        self.bpm = bpm
        self.name = name

        # TODO: add metrics
        self.metrics = {}

    def __iter__(self):
        for chord in self.chords:
            yield chord

    def __len__(self):
        return len(self.chords)

    def __repr__(self):
        return "Progression " + self.to_string()

    def __getitem__(self, ix):
        return self.chords[ix]

    def to_string(self):
        return json.dumps(self.to_json(), indent=4)

    def to_json(self):
        result = []

        for ix, (chord, locked) in enumerate(list(zip(self.chords, self.locks))):
            result.append(
                {
                    "id": chord.id,
                    "ix": ix,
                    "duration": chord.duration,
                    "locked": locked,
                    "type": chord.type,
                    "typeId": chord.typeId,
                    "notes": chord.notes,
                    "metrics": chord.metrics,
                }
            )

        return result

    def to_audio(self, n_overtones=2, outpath=None):
        durations = [c.duration for c in self.chords]
        durations_seconds = [dur * (60 / self.bpm) for dur in durations]
        audio_buffer = make_audio_progression(
            self.chords, durations_seconds, n_overtones
        )
        if outpath:
            save_audio_buffer(audio_buffer, outpath)
            logger.info(f"Audio saved to {outpath}")

    def to_midi(self, outpath=None):
        mid = get_midi_from_progression(self.chords, self.bpm, self.name)
        if outpath:
            mid.filename = outpath
            mid.save(outpath)
            logger.info(f"Midi saved to {outpath}")

    def get_new_solution(self):
        """Given existing locked chords and constraints, returns a new chord progression of the same length"""

        existing_chords = self.chords

        # TODO: allow solver constraints to be passed as arguments
        chords = select_chords(
            n_chords=len(existing_chords),
            existing_chords=existing_chords,
            locks=self.locks,
        )

        return Progression(chords)
