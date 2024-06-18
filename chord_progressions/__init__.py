import logging
import os

__version__ = "0.36.0"  # updated by bumpversion, do not change

THIS_DIR = os.path.dirname(os.path.realpath(__file__))

OUTPUT_DIR = os.path.join(THIS_DIR, "../assets/output")

# a copy of /usr/share/dict/web2 from a macbook air (early 2014)
WORDS_FILEPATH = os.path.join(THIS_DIR, "..", "words")

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("chord-progressions")

# Config
# TODO: move to config
DEFAULT_BPM = 120
DEFAULT_MIDI_TICKS_PER_BEAT = 480
