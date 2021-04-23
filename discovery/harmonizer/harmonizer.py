"""
TODO: rip the stuff from here that was moved to `solver` and consolidate the rest with `generate`
"""

import argparse
import os

import mido
import numpy as np
import pandas as pd

from chord_progressions.chord import get_template_from_notes
from chord_progressions.generate import get_run_id
from chord_progressions.midi import (
    get_seconds_from_midi_ticks,
    make_midi_progression,
    save_midi_progression,
)
from chord_progressions.pitch import get_note_from_midi_num, get_pitch_class_from_note


def tick_times_to_durations(tick_times, bpm, total_ticks, ticks_per_beat):
    """
    Given list of tick times at which to place chords and a bpm, calculate the duration of each chord.
    """

    sec_times = [
        get_seconds_from_midi_ticks(t, bpm, ticks_per_beat) for t in tick_times
    ]

    print(f"Times (ticks): {tick_times}")
    print(f"Times (secs):  {sec_times}")

    durations = []

    for i in range(1, len(sec_times)):
        durations.append(sec_times[i] - sec_times[i - 1])

    total_duration = get_seconds_from_midi_ticks(total_ticks, bpm, ticks_per_beat)
    durations.append(total_duration - sec_times[-1])

    return [round(d, 2) for d in durations]


def make_note_event_df_from_track(track):
    """
    Extracts note events from a midi track and returns a DataFrame with columns:
        [event_type, midi_num, note, delta_ticks, absolute_ticks]
    """

    note_events = []

    for msg in track:
        # print(msg)

        if msg.type in ["note_on", "note_off"]:
            note_events.append(
                [msg.type, msg.note, msg.time, get_note_from_midi_num(msg.note)]
            )

    note_events = pd.DataFrame(
        note_events, columns=["event_type", "midi_num", "delta_ticks", "note"]
    )

    # translate the `time` from `delta time in ticks` to `absolute time`
    note_events["absolute_ticks"] = note_events["delta_ticks"].cumsum()

    return note_events


def make_options(melody_filepath, bpm, n_options, output_dir):

    melody_name = os.path.basename(melody_filepath).split(".mid")[0]

    mid = mido.MidiFile(melody_filepath)

    ticks_per_beat = mid.ticks_per_beat

    if mid.type != 0:
        raise ValueError(
            "Midi file must be type 0. See https://mido.readthedocs.io/en/latest/midi_files.html#file-types for details."
        )

    track = mid.tracks[0]
    print(f"Track: {track.name}")

    note_events = make_note_event_df_from_track(track)

    max_ticks = note_events["absolute_ticks"].max()

    # TODO: take `tick_times` as param
    # evenly spaced starting at 0
    tick_times = [0]
    for i in range(1, 4):
        tick_times.append(max_ticks / 4 * i)

    active_notes = [get_active_note_at_time(note_events, t) for t in tick_times]

    durations = tick_times_to_durations(tick_times, bpm, max_ticks, ticks_per_beat)

    run_id = get_run_id(melody_name)

    for option_num in range(n_options):

        option_id = f"{run_id}_{option_num}"

        chords, chord_types = generate_option(active_notes)

        print(f"\n{option_id}:")
        for t, c in zip(chord_types, chords):
            print(f"  {t}: {c}")

        # TODO: make_midi_progression needs an `offset` param for when the first chord isn't at 0
        output_midi = make_midi_progression(
            chords, durations, bpm, ticks_per_beat, option_id
        )

        save_midi_progression(output_midi, option_id, output_dir)


if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--melody_filepath",
        type=str,
        help="Path to midi file for monophonic melody.",
        required=True,
    )
    parser.add_argument(
        "--output_dir",
        type=str,
        help="Path to directory to which to save output harmonies.",
        required=True,
    )
    parser.add_argument(
        "--bpm",
        type=float,
        help="BPM of the midi clip.",
        required=True,
    )
    parser.add_argument(
        "--n_progressions",
        type=int,
        help="The number of chord progression options to generate",
        required=True,
    )
    args = parser.parse_args()

    melody_filepath = args.melody_filepath
    bpm = args.bpm
    n_options = args.n_progressions
    output_dir = args.output_dir

    make_options(melody_filepath, bpm, n_options, output_dir)
