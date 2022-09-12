"""EXPERIMENTAL. Dependencies not included in project"""

import glob
import os

from chord_progressions.extract.audio import extract_progression_from_audio

try:
    THIS_DIR = os.path.dirname(os.path.realpath(__file__))
except:
    THIS_DIR = os.getcwd()

OST = "undertale"
AUDIO_DIR = os.path.join(THIS_DIR, f"../assets/audio/{OST}")
MP3_DIR_44100 = os.path.join(AUDIO_DIR, "mp3-44100")
OUTPUT_DIR = os.path.join(THIS_DIR, f"../assets/output/{OST}")
OUTPUT_MIDI_DIR = os.path.join(OUTPUT_DIR, "midi")

for outpath in [OUTPUT_MIDI_DIR]:
    if not os.path.exists(outpath):
        os.makedirs(outpath)


# Parameters
INPUT_AUDIO_DIR = MP3_DIR_44100
INPUT_AUDIO_FORMAT = ".mp3"

# TODO: adapt the below config from other script
# OST = "elliott"
# THIS_DIR = os.path.dirname(os.path.realpath(__file__))
# AUDIO_DIR = os.path.join(THIS_DIR, f"../../assets/audio/{OST}")
MARKED_AUDIO_DIR = os.path.join(AUDIO_DIR, "mp3-44100-marked")
# ACCOMPANIMENT_DIR = os.path.join(AUDIO_DIR, "split_accompaniment")

# OUTPUT_DIR = os.path.join(THIS_DIR, f"../../assets/output/{OST}")
OUTPUT_PLOT_DIR = os.path.join(OUTPUT_DIR, "plots")
# TRACKS_PATH = os.path.join(OUTPUT_DIR, "tracks.csv")

for outpath in [MARKED_AUDIO_DIR, OUTPUT_PLOT_DIR]:
    if not os.path.exists(outpath):
        os.makedirs(outpath)


if __name__ == "__main__":
    for filepath in glob.glob(f"{INPUT_AUDIO_DIR}/*{INPUT_AUDIO_FORMAT}"):
        print(f"Extracting chords from audio file: {filepath}")
        basename = os.path.basename(filepath)
        trackid = os.path.splitext(basename)[0]

        progression = extract_progression_from_audio(
            filepath, OUTPUT_PLOT_DIR, MARKED_AUDIO_DIR
        )

        midi_progression_path = os.path.join(OUTPUT_MIDI_DIR, f"{trackid}.mid")
        progression.save_midi(midi_progression_path)

        # TODO: plot transition matrix (https://github.com/seffka/ACE2017/blob/master/plots/plot_transition_matrix.py)
