import logging
import os

__version__ = "0.32.0"  # updated by bumpversion, do not change

THIS_DIR = os.path.dirname(os.path.realpath(__file__))

OUTPUT_DIR = os.path.join(THIS_DIR, "../assets/output")
WAV_OUTPUT_DIR = os.path.join(OUTPUT_DIR, "wav")
MIDI_OUTPUT_DIR = os.path.join(OUTPUT_DIR, "midi")
META_OUTPUT_DIR = os.path.join(OUTPUT_DIR, "meta")

# a copy of /usr/share/dict/web2 from a macbook air (early 2014)
WORDS_FILEPATH = os.path.join(THIS_DIR, "..", "words")

for outdir in [WAV_OUTPUT_DIR, MIDI_OUTPUT_DIR, META_OUTPUT_DIR]:
    if not os.path.isdir(outdir):
        os.makedirs(outdir)

# if not os.path.exists(WORDS_FILEPATH):
#     raise EnvironmentError("Words file does not exist")

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("chord-progressions")

# Config
# TODO: move to config
DEFAULT_BPM = 120
DEFAULT_MIDI_TICKS_PER_BEAT = 480
