from chord_progressions import DEFAULT_BPM, logger
from chord_progressions.chord import Chord
from chord_progressions.io.audio import make_audio_progression, save_audio_buffer
from chord_progressions.io.midi import get_midi_from_progression
from chord_progressions.solver import select_chords
from chord_progressions.utils import get_n_random_uuids


class Progression:
    def __init__(
        self,
        chords: list[Chord] = [],
        durations: list[str] = None,
        bpm: float = DEFAULT_BPM,
        locks: list[int] = None,
        name: str = "",
    ):
        self.chords = chords

        if not durations:
            durations = ["1m"] * len(chords)
        self.durations = durations

        self.bpm = bpm
        self.name = name

        if not locks:
            locks = [0] * len(chords)
        self.locks = locks

        self.ids = get_n_random_uuids(len(chords))

        # TODO: add metrics
        self.metrics = {}

    def __iter__(self):
        for chord in self.chords:
            yield chord

    def __len__(self):
        return len(self.chords)

    def json(self):
        result = []

        for ix, (chord, chord_id, duration, locked) in enumerate(
            list(zip(self.chords, self.ids, self.durations, self.locks))
        ):
            result.append(
                {
                    "id": chord_id,
                    "ix": ix,
                    "type": chord.type,
                    "typeId": chord.typeId,
                    "notes": chord.notes,
                    "duration": duration,
                    "locked": str(locked),
                    "metrics": chord.metrics,
                }
            )

        return result

    def from_audio(self, filepath):
        return

    def as_audio(self, n_overtones=2):
        durations_seconds = [dur * (60 / self.bpm) for dur in self.durations]
        return make_audio_progression(self.chords, durations_seconds, n_overtones)

    def save_audio(self, outpath, n_overtones=2):
        audio_buffer = self.as_audio(n_overtones)
        save_audio_buffer(audio_buffer, outpath)
        logger.info(f"Audio saved to {outpath}")

    def from_midi(self):
        return

    def as_midi(self):
        return get_midi_from_progression(
            self.chords, self.durations, self.bpm, self.name
        )

    def save_midi(self, outpath):
        """Saves the progression a .mid file"""
        mid = self.as_midi()
        mid.filename = outpath
        mid.save(outpath)
        logger.info(f"Midi saved to {outpath}")

    def get_new_solution(self):
        """Given existing locked chords and constraints, returns a new chord progression of the same length
        TODO: allow solver constraints to be passed as arguments"""

        existing_chords = self.chords

        # Use the default parameters
        return select_chords(
            n_chords=len(existing_chords),
            existing_chords=existing_chords,
            pct_notes_common=0,
            note_range_low=60,
            note_range_high=108,
            locks=self.locks,
        )
