import argparse
import os

from chord_progressions.extract.midi import simplify_harmony
from chord_progressions.extract.midi_harman import label_midi, write_labels
from chord_progressions.io.midi import make_midi_progression, save_midi_progression

try:
    THIS_DIR = os.path.dirname(os.path.realpath(__file__))
except:
    THIS_DIR = os.getcwd()

OUTPUT_DIR = os.path.join(THIS_DIR, "../assets/output")

if not os.path.isdir(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)

# note values, e.g. 1/4 = quarter note, 1/64 = 64th note
# TODO: parse these from args
SHORTEST_NOTE = 1 / 64
SMOOTH_BEAT = 1
QUANTIZE_BEAT = 1 / 2

SAMPLE_FILEPATH = "../assets/midi/Sakamoto_MerryChristmasMrLawrence.mid"

if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--filepath",
        type=str,
        default=SAMPLE_FILEPATH,
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
    harman_labels = label_midi(extracted)
    harman_results = write_labels(harman_labels, filepath, harman_outpath, songname)
    print(f"Wrote harman labels to {harman_outpath}")

    chords = [i["notes"] for i in harman_labels]
    durations = [i["end_time"] - i["start_time"] for i in harman_labels]
    midi_progression = make_midi_progression(chords, durations, songname)
    midi_progression_path = os.path.join(OUTPUT_DIR, f"harman-chords_{songname}.mid")
    save_midi_progression(midi_progression, midi_progression_path)
    print(f"Wrote harman chords to {midi_progression_path}")
