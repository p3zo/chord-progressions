"""Generate a chord progression"""

import argparse
import copy
import csv
import os

import numpy as np

from chord_progressions import META_OUTPUT_DIR, logger
from chord_progressions.audio import save_audio_progression
from chord_progressions.midi import save_midi_progression
from chord_progressions.solver import select_notes_list
from chord_progressions.utils import round_to_base, get_run_id

DEFAULT_ALLOWED_CHORD_TYPES = [
    "minor third",
    "major third",
    "perfect fourth",
    "minor chord",
    "dorian / minor pentachord",
    "diminished chord",
    "augmented chord",
    "major-seventh chord",
    "minor-seventh chord",
    "major-ninth chord",
    "minor-ninth chord",
    "indian-japan pentatonic",
    "half-diminished seventh chord",
    "diminished-seventh chord",
    "dominant-ninth,major-minor|prometheus pentamirror",
    "minor-second quartal tetrachord",
]


def get_chord_durations(n_segments, duration_min, duration_max, duration_interval):

    if duration_min == duration_max:
        durations = [duration_min] * n_segments

    else:
        durations = np.random.uniform(duration_min, duration_max, n_segments)
        durations = [round_to_base(d, duration_interval) for d in durations]

    return durations


def generate_progression(
    n_segments,
    pct_notes_common,
    note_range_low,
    note_range_high,
    duration_min,
    duration_max,
    duration_interval,
    n_overtones,
    allowed_chord_types,
    first_chord,
):

    existing_chords = None
    existing_types = None
    locks = "0" * n_segments
    first_chord = None
    adding = False

    chord_types, chords = select_notes_list(
        n_segments=n_segments,
        pct_notes_common=pct_notes_common,
        note_range_low=note_range_low,
        note_range_high=note_range_high,
        existing_chords=existing_chords,
        existing_types=existing_types,
        locks=locks,
        first_chord=first_chord,
        adding=adding,
        allowed_chord_types=allowed_chord_types,
    )

    durations = get_chord_durations(
        n_segments, duration_min, duration_max, duration_interval
    )

    run_id = get_run_id()

    save_audio_progression(run_id, chords, durations, n_overtones)

    save_midi_progression(run_id, chords, durations)

    # metadata
    meta_filepath = os.path.join(META_OUTPUT_DIR, f"{run_id}.csv")

    with open(meta_filepath, "w") as fh:

        writer = csv.writer(fh, delimiter="\t")

        writer.writerows(
            [
                ["n_segments", n_segments],
                ["n_overtones", n_overtones],
                ["duration_min", duration_min],
                ["duration_max", duration_max],
                ["duration_interval", duration_interval],
                ["chord_types", chord_types],
                ["chords", chords],
                ["durations", durations],
            ]
        )

    logger.info(f"Progression metadata saved to to {meta_filepath}")


def validate_args(args):

    if args.n_segments < 1:
        raise ValueError("`n_segments` must be > 0")

    if args.n_overtones < 0:
        raise ValueError("`n_overtones` must be >= 0")

    if args.duration_min > args.duration_max:
        raise ValueError("`duration_min` must be <= `duration_max`")

    if args.duration_min <= 0:
        raise ValueError("`duration_min` must be > 0")

    if args.duration_min > 20:
        raise ValueError("`duration_max` must be <= 20")

    if args.duration_interval <= 0:
        raise ValueError("`duration_interval` must be > 0")

    if args.note_range_low > args.note_range_high:
        raise ValueError("`note_range_low` must be <= `note_range_high`")


if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--n_segments", type=int, default=4, help="Number of chords to generate."
    )
    # TODO: add a param for `n_unique_chords`
    # TODO: add params for lowest_note and highest_note
    parser.add_argument(
        "--pct_notes_common",
        type=float,
        default=0,
        help="Minimum percent of notes to keep in common between adjacent chords.",
    )
    # TODO: add bpm arg and make duration in beats rather than seconds
    parser.add_argument(
        "--duration_min",
        type=float,
        default=3,
        help="Minimum chord duration in seconds",
    )
    parser.add_argument(
        "--duration_max",
        type=float,
        default=3,
        help="Maximum chord duration in seconds",
    )
    parser.add_argument(
        "--duration_interval",
        type=float,
        default=0.5,
        help="Interval by which chord durations are allowed to vary in seconds",
    )
    parser.add_argument(
        "--n_overtones",
        type=int,
        default=2,
        help="Number of harmonic overtones used when generating audio buffers.",
    )
    parser.add_argument(
        "--first_chord",
        type=list,
        default=None,
        help="Specify the first chord of the progression",
    )
    parser.add_argument(
        "--note_range_low",
        type=int,
        default=36,
        help="Midi note number for lowest allowed note",
    )
    parser.add_argument(
        "--note_range_high",
        type=int,
        default=84,
        help="Midi note number for highest allowed note",
    )
    args = parser.parse_args()

    args = copy.deepcopy(args)

    validate_args(args)

    note_range_low = args.note_range_low
    note_range_high = args.note_range_high

    print(f"note_range_low {note_range_low}, note_range_high {note_range_high}")

    generate_progression(
        n_segments=args.n_segments,
        note_range_low=note_range_low,
        note_range_high=note_range_high,
        pct_notes_common=args.pct_notes_common,
        duration_min=args.duration_min,
        duration_max=args.duration_max,
        duration_interval=args.duration_interval,
        n_overtones=args.n_overtones,
        allowed_chord_types=DEFAULT_ALLOWED_CHORD_TYPES,
        first_chord=args.first_chord,
    )
