from music21 import chord, stream
from music21.analysis.discrete import KrumhanslSchmuckler

from chord_progressions.pitch import NOTE_NAMES


def get_key(midi_nums_list, quarter_lengths):
    """Returns the major or minor key that best fits a sequence of chords, e.g. "C major".

    Uses the Krumhansl-Schmuckler algorithm, which weights each pitch class by how long it sounds.
    """
    s = stream.Stream()
    for midi_nums, quarter_length in zip(midi_nums_list, quarter_lengths, strict=True):
        s.append(chord.Chord(midi_nums, quarterLength=quarter_length))

    key = KrumhanslSchmuckler().getSolution(s)

    # music21 returns an arbitrary key when no key correlates, e.g. all 12 pitch classes equally long
    if key.correlationCoefficient == 0:
        raise ValueError("No key fits a progression where every pitch class sounds equally long")

    # music21 may spell the tonic with flats, e.g. "E-"
    return f"{NOTE_NAMES[key.tonic.pitchClass]} {key.mode}"
