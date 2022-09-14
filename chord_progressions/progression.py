import json

from chord_progressions import DEFAULT_BPM, logger
from chord_progressions.chord import Chord
from chord_progressions.io.audio import make_audio_progression, save_audio_buffer
from chord_progressions.io.midi import get_midi_from_progression
from chord_progressions.solver import select_chords


class Progression:
    """
    A sequence of chords with metadata such as chord durations, bpm, chord locks.

    Parameters
    ----------
    chords: list[Chord], default []
        The chords in the progression.
    durations: list[int], default None
        The duration of each chord in the progression, specified in beats. Defaults to 1 beat per chord if not provided.
            TODO: allow duration to be specified as Tone.barsBeatsSixteenths notation
            See https://github.com/Tonejs/Tone.js/wiki/Time#transport-time
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
        durations: list[int] = None,
        locks: str = None,
        bpm: float = DEFAULT_BPM,
        name: str = "",
    ):
        self.chords = chords

        if not durations:
            durations = [1] * len(chords)
        self.durations = durations

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

    def to_string(self):
        return json.dumps(self.to_json(), indent=4)

    def to_json(self):
        result = []

        for ix, (chord, duration, locked) in enumerate(
            list(zip(self.chords, self.durations, self.locks))
        ):
            result.append(
                {
                    "id": chord.id,
                    "ix": ix,
                    "duration": duration,
                    "locked": locked,
                    "type": chord.type,
                    "typeId": chord.typeId,
                    "notes": chord.notes,
                    "metrics": chord.metrics,
                }
            )

        return result

    def to_audio(self, n_overtones=2, outpath=None):
        durations_seconds = [dur * (60 / self.bpm) for dur in self.durations]
        audio_buffer = make_audio_progression(
            self.chords, durations_seconds, n_overtones
        )
        if outpath:
            save_audio_buffer(audio_buffer, outpath)
            logger.info(f"Audio saved to {outpath}")

    def to_midi(self, outpath=None):
        mid = get_midi_from_progression(
            self.chords, self.durations, self.bpm, self.name
        )
        if outpath:
            mid.filename = outpath
            mid.save(outpath)
            logger.info(f"Midi saved to {outpath}")

    def get_new_solution(self):
        """Given existing locked chords and constraints, returns a new chord progression of the same length
        TODO: allow solver constraints to be passed as arguments"""

        existing_chords = self.chords

        # Use the default parameters
        chords = select_chords(
            n_chords=len(existing_chords),
            existing_chords=existing_chords,
            pct_notes_common=0,
            note_range_low=60,
            note_range_high=108,
            locks=self.locks,
        )

        return Progression(chords, self.durations)
