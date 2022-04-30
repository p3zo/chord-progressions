"""Process polyphonic midi to make it more well-suited for chord extraction"""

import warnings
from functools import partial

import numpy as np
import pandas as pd
import pretty_midi

# note values, e.g. 1/4 = quarter note, 1/64 = 64th note
DEFAULT_SHORTEST_NOTE = 1 / 64
DEFAULT_SMOOTH_BEAT = 1
DEFAULT_QUANTIZE_BEAT = 1 / 2


def parse_notes(pmid):
    """Parses a pretty_midi object into a 2D array with (start, end, note) columns."""
    points = []

    for instrument in pmid.instruments:
        if instrument.is_drum:
            continue

        for note in instrument.notes:
            points.append((note.start, note.end, note.pitch))

    dtype = np.dtype([("start", float), ("end", float), ("note", int)])
    notes = np.array(points, dtype=dtype)

    return np.sort(notes, order="start")


def load_midi_file(filepath):
    # warnings can be verbose when midi has no metadata e.g. tempo, key, time signature
    with warnings.catch_warnings():
        warnings.filterwarnings("ignore", category=RuntimeWarning)
        try:
            midi = pretty_midi.PrettyMIDI(filepath)
        except Exception as e:
            print(f"Failed loading file {filepath}: {e}")
            return

    return midi


def round_to_target(target, x):
    """Round `x` to the closest `target`

    e.g.
        round_to_target(1.12, .5) == 1.00
        round_to_target(1.12, .25) == 1.00
        round_to_target(1.13, .25) == 1.25
    """
    y = 1 / target
    return round(x * y) / y


def quantize_times(times, beat):
    """Quantize an array of times to the closest beat.

    e.g. quantize_times([1.1, 1.2, 1.3, 1.4], 0.5) == [1., 1., 1.5, 1.5]
    """
    func = partial(round_to_target, beat)

    return list(map(func, times))


def drop_short_notes(notes, shortest_duration):
    """Removes notes that are shorter than shortest_duration"""

    short_note_ixs = []

    for ix, n in enumerate(notes):
        if n["end"] - n["start"] < shortest_duration:
            short_note_ixs.append(ix)

    return np.delete(notes, short_note_ixs)


def smooth_notes(notes, step_size):
    """Joins adjacent, repeated notes into single, longer notes"""

    df = pd.DataFrame(notes)

    steps = np.arange(df.start.min(), df.end.max() + step_size, step_size)

    for ix, s in enumerate(steps):
        if ix == 0:
            continue

        seg = df[(df["start"] >= steps[ix - 1]) & (df["end"] < s)]

        vcs = seg.note.value_counts()
        vcs1 = vcs[vcs > 1]

        for k, v in vcs1.items():
            svc = seg[seg.note == k]

            df.loc[svc.index[0], "end"] = seg.loc[svc.index[-1]]["end"]

            df.drop(index=svc.index[1:], inplace=True)

    tups = list(df.itertuples(index=False, name=None))

    dtype = np.dtype([("start", float), ("end", float), ("note", int)])

    return np.array(tups, dtype=dtype)


def mk_midi_from_notes(notes):
    midi = pretty_midi.PrettyMIDI()
    piano_program = pretty_midi.instrument_name_to_program("Acoustic Grand Piano")
    piano = pretty_midi.Instrument(program=piano_program)

    for e in notes:
        note = pretty_midi.Note(
            velocity=100, pitch=e["note"], start=e["start"], end=e["end"]
        )
        piano.notes.append(note)

    midi.instruments.append(piano)

    return midi


def simplify_harmony(
    filepath,
    shortest_note=DEFAULT_SHORTEST_NOTE,
    smooth_beat=DEFAULT_SMOOTH_BEAT,
    quantize_beat=DEFAULT_QUANTIZE_BEAT,
):
    """Simplify midi to its essential harmonic content"""

    midi = load_midi_file(filepath)

    notes = parse_notes(midi)

    tempos = midi.get_tempo_changes()

    # TODO: handle tempo changes
    if len(tempos[0]) == 0:
        raise ValueError("No tempos")
    if len(tempos[0]) > 1:
        #     raise ValueError("Can't handle tempo changes")
        print(
            "Warning: MIDI file has tempo changes but a constant BPM is assumed when processing"
        )

    # TODO: calculate note durations based on time signature
    bpm = tempos[1][0]
    whole_note_dur = 60 / bpm * 4  # seconds

    # convert durations to seconds
    shortest_dur = whole_note_dur * shortest_note
    smooth_dur = whole_note_dur * smooth_beat
    quantize_dur = whole_note_dur * quantize_beat

    notes_cleaned = drop_short_notes(notes, shortest_dur)
    notes_smoothed = smooth_notes(notes_cleaned, smooth_dur)
    notes_cleaned_2 = drop_short_notes(notes_smoothed, shortest_dur * 4)

    # TODO: split on long rests (parameterized duration)
    # TODO: lengthen notes to fill in shorter rests

    # Quantize both the start and end times of each note
    notes_cleaned_2["start"] = quantize_times(notes_cleaned_2["start"], quantize_dur)
    notes_cleaned_2["end"] = quantize_times(notes_cleaned_2["end"], quantize_dur)

    # If start and end were quantized to the same time, move the end time back
    for note in notes_cleaned_2:
        if note["start"] == note["end"]:
            note["end"] += quantize_dur

    return mk_midi_from_notes(notes_cleaned_2)
