import argparse
import os

from chord_progressions.extract import simplify_harmony
from chord_progressions.extract_harman import write_harman_labels

try:
    THIS_DIR = os.path.dirname(os.path.realpath(__file__))
except:
    THIS_DIR = os.getcwd()

OUTPUT_DIR = os.path.join(THIS_DIR, "../output")

if not os.path.isdir(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)

# note values, e.g. 1/4 = quarter note, 1/64 = 64th note
# TODO: parse these from args
SHORTEST_NOTE = 1 / 64
SMOOTH_BEAT = 1
QUANTIZE_BEAT = 1 / 2


if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--filepath",
        type=str,
        help="Path to a midi file",
    )
    args = parser.parse_args()

    filepath = args.filepath

    songname = os.path.splitext(os.path.basename(filepath))[0]

    extracted = simplify_harmony(filepath, SHORTEST_NOTE, SMOOTH_BEAT, QUANTIZE_BEAT)
    chords_path = os.path.join(OUTPUT_DIR, f"chords-{songname}.mid")
    extracted.write(chords_path)
    print(f"Wrote chords to {chords_path}")

    harman_outpath = os.path.join(OUTPUT_DIR, f"harman-{songname}.csv")
    write_harman_labels(filepath, harman_outpath, songname)
