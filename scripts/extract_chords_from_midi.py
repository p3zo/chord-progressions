"""Reads a midi file, extracts chord progressions, writes a new midi file"""

import argparse
import os

from chord_progressions.extract.midi_harman import extract_progression_from_midi


if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--filepath",
        type=str,
        help="Path to a midi file",
    )
    parser.add_argument(
        "--outdir",
        type=str,
        help="Directory in which to write the results",
        default=".",
    )
    parser.add_argument(
        "--shortest_note",
        type=float,
        help="Notes shorter than this duration will be filtered out. Use note values, e.g. 1/64 = 64th note.",
        default=1 / 64,
    )
    parser.add_argument(
        "--smooth_beat",
        type=float,
        help="",
        default=1,
    )
    parser.add_argument(
        "--quantize_beat",
        type=float,
        help="Note duration to quantize to.",
        default=1 / 2,
    )
    parser.add_argument(
        "--sonify",
        action="store_true",
        help="Create a .wav file with a sonification of the extracted chords",
    )
    args = parser.parse_args()

    outdir = args.outdir
    if not os.path.isdir(outdir):
        os.makedirs(outdir)

    inpath = args.filepath

    track_name = os.path.splitext(os.path.basename(inpath))[0]

    simplified_path = os.path.join(outdir, f"chords-{track_name}.mid")
    harman_labels_path = os.path.join(outdir, f"harman-labels_{track_name}.csv")
    progression = extract_progression_from_midi(
        inpath,
        shortest_note=args.shortest_note,
        smooth_beat=args.smooth_beat,
        quantize_beat=args.quantize_beat,
        simplified_path=simplified_path,
        harman_labels_path=harman_labels_path,
    )

    midi_progression_path = os.path.join(outdir, f"harman-chords_{track_name}.mid")
    progression.to_midi(outpath=midi_progression_path)

    if args.sonify:
        audio_progression_path = os.path.join(outdir, f"harman-chords_{track_name}.wav")
        progression.to_audio(outpath=audio_progression_path)
