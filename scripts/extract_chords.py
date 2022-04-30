import argparse
import os

from chord_progressions.extract import simplify_harmony
from chord_progressions.extract_harman import label_file, write_labels

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

filepath = '../data/sample/Sakamoto_MerryChristmasMrLawrence.mid'

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

    harman_outpath = os.path.join(OUTPUT_DIR, f"harman-labels_{songname}.csv")
    harman_labels = label_file(filepath)
    write_labels(harman_labels, filepath, harman_outpath, songname)
    print(f"Wrote harman labels to {harman_outpath}")

    # TODO: make a midi progression from harman labels
