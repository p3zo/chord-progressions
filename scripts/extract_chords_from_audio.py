import glob
import os

from chord_progressions.extract.audio import extract_progression_from_audio
from chord_progressions.midi import make_midi_progression, save_midi_progression

try:
    THIS_DIR = os.path.dirname(os.path.realpath(__file__))
except:
    THIS_DIR = os.getcwd()

OST = "elliott"
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


if __name__ == "__main__":
    for filepath in glob.glob(f"{INPUT_AUDIO_DIR}/*{INPUT_AUDIO_FORMAT}"):

        basename = os.path.basename(filepath)
        trackid = os.path.splitext(basename)[0]

        progression, start_seconds = extract_progression_from_audio(filepath)

        midi_progression = progression.to_midi(name=trackid, bpm=bpm)

        midi_progression = make_midi_progression(
            chords, durations, progression_name=trackid, bpm=bpm
        )

        outpath = os.path.join(OUTPUT_MIDI_DIR, f"{trackid}.mid")
        save_midi_progression(midi_progression, outpath)

        # TODO: plot transition matrix (https://github.com/seffka/ACE2017/blob/master/plots/plot_transition_matrix.py)
