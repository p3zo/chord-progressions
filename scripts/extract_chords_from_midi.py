import argparse
import os

from chord_progressions.extract.midi_harman import extract_progression_from_midi

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
    parser.add_argument(
        "--sonify",
        action="store_true",
        help="Create a .wav file with a sonification of the extracted chords",
    )
    args = parser.parse_args()

    filepath = args.filepath

    track_name = os.path.splitext(os.path.basename(filepath))[0]

    simplified_path = os.path.join(OUTPUT_DIR, f"chords-{track_name}.mid")
    harman_labels_path = os.path.join(OUTPUT_DIR, f"harman-labels_{track_name}.csv")
    progression = extract_progression_from_midi(
        filepath, simplified_path=simplified_path, harman_labels_path=harman_labels_path
    )

    midi_progression_path = os.path.join(OUTPUT_DIR, f"harman-chords_{track_name}.mid")
    progression.to_midi(outpath=midi_progression_path)

    if args.sonify:
        audio_progression_path = os.path.join(
            OUTPUT_DIR, f"harman-chords_{track_name}.wav"
        )
        progression.to_audio(outpath=audio_progression_path)
