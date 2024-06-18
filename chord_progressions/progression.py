import json

from chord_progressions import DEFAULT_BPM, logger
from chord_progressions.chord import Chord
from chord_progressions.io.audio import make_audio_progression, save_audio_buffer
from chord_progressions.io.midi import get_midi_from_progression

"""
    Durations are specified in Tone.Time.Notation format.
    **NOT ALL TONE TIME NOTATIONS ARE SUPPORTED.**

    The number represents the subdivision. "t" represents a triplet. A "." adds a half.
    e.g. "4n" is a quarter note, "4t" is a quarter note triplet, and "4n." is a dotted quarter note.

    Tone.Time docs:
        https://github.com/Tonejs/Tone.js/wiki/Time

    Full list of Tone.js subdivisions:
        https://github.com/Tonejs/Tone.js/blob/dbed4d27fe66ee606a7309b03ac0ba4f5a2a4ecb/Tone/core/type/Units.ts#L47-L55s
"""
DURATIONS = ["8n", "4n", "4n.", "2n", "2n.", "1m", "2m"]

# The number of beats per duration
DURATION_BEAT_MAPPING = {
    "8n": 0.5,
    "4n": 1,
    "4n.": 1.5,
    "2n": 2,
    "2n.": 3,
    "1m": 4,
    "2m": 8,
}


def duration_to_seconds(duration, bpm):
    """Converts Tone.Time.notation to seconds"""
    beats = DURATION_BEAT_MAPPING[duration]
    seconds_per_beat = 60 / bpm
    return beats * seconds_per_beat


def get_closest(lst, K):
    """Returns the number from `lst` closest to a float `K`"""
    return min(range(len(lst)), key=lambda i: abs(lst[i] - K))


def seconds_to_duration(seconds, bpm):
    """Converts seconds to beats and quantizes to the closest supported beat notation"""
    beats_per_second = bpm / 60
    beats = seconds * beats_per_second
    ix = get_closest(list(DURATION_BEAT_MAPPING.values()), beats)
    return list(DURATION_BEAT_MAPPING.keys())[ix]


class Progression:
    """
    A sequence of Chords with metadata such as bpm.

    Parameters
    ----------
    chords: list[Chord] or list[list[int]], default []
        The chords in the progression.
    durations: list[str] or list[float], default []
        The duration of the chords, specified in Tone.Time notation or in seconds.
        Seconds will be quantized to Tone.Time units.
    bpm: float, default DEFAULT_BPM
        The beats per minute (BPM) of the progression.
    name: str, default ""
        The name of the progression.
    """

    def __init__(
        self,
        chords: list[Chord] = [],
        durations: list[str] = [],
        bpm: float = DEFAULT_BPM,
        name: str = "",
    ):
        if not isinstance(chords, list):
            raise ValueError("Chords must be a list")

        # If chords are passed as a midi_nums_list (list[list[int]]), convert them to Chords
        if isinstance(chords, list) and len(chords) > 0 and isinstance(chords[0], list):
            chords = [Chord(c) for c in chords]

        if not isinstance(durations, list):
            raise ValueError("Durations must be a list")

        if len(durations) == 0:
            durations = ["1m"] * len(chords)
        elif isinstance(durations[0], str):
            pass
        elif isinstance(durations[0], int) or isinstance(durations[0], float):
            durations = [seconds_to_duration(d, bpm) for d in durations]
        else:
            raise ValueError("Durations must be Tone.Time notation strings or seconds.")

        if not len(durations) == len(chords):
            raise ValueError("Durations must be the same length as chords.")

        self.chords = chords
        self.durations = durations
        self.bpm = bpm
        self.name = name
        self.metrics = {}  # TODO: add metrics

    def __iter__(self):
        # TODO: include progression-chord metadata
        for chord in self.chords:
            yield chord

    def __len__(self):
        return len(self.chords)

    def __repr__(self):
        return "Progression " + self.to_string()

    def __getitem__(self, ix):
        # TODO: include progression-chord metadata, e.g. its duration
        return self.chords[ix]

    def to_string(self):
        return json.dumps(self.to_json(), indent=4)

    def to_json(self):
        # TODO: include progression-level attrs like name, bpm
        result = []

        for ix, (chord, duration) in enumerate(list(zip(self.chords, self.durations))):
            result.append(
                {
                    "id": chord.id,
                    "ix": ix,
                    "duration": duration,
                    "type": chord.type,
                    "typeId": chord.typeId,
                    "notes": chord.notes,
                    "midi_nums": chord.midi_nums,
                    "metrics": chord.metrics,
                }
            )

        return result

    def get_durations_in_seconds(self):
        return [duration_to_seconds(d, self.bpm) for d in self.durations]

    def to_audio(self, outpath=None, n_overtones=4):
        dur_secs = self.get_durations_in_seconds()
        audio_buffer = make_audio_progression(self.chords, dur_secs, n_overtones)

        # TODO: create outpath from random word + datetime if not provided? add flag to opt for this?
        if outpath:
            save_audio_buffer(audio_buffer, outpath)
            logger.info(f"Audio saved to {outpath}")

    def to_midi(self, outpath=None):
        mid = get_midi_from_progression(self)
        if outpath:
            mid.filename = outpath
            mid.save(outpath)
            logger.info(f"Midi saved to {outpath}")
