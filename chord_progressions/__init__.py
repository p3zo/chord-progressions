import logging
import os

__version__ = "0.37.0"  # updated by bumpversion, do not change

THIS_DIR = os.path.dirname(os.path.realpath(__file__))

OUTPUT_DIR = os.path.join(THIS_DIR, "../assets/output")

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("chord-progressions")

# Config
# TODO: move to config
DEFAULT_BPM = 120
DEFAULT_MIDI_TICKS_PER_BEAT = 480

from chord_progressions.chord import Chord
from chord_progressions.extract import (
    extract_progression_from_midi,
)
from chord_progressions.pitch import (
    get_midi_num_from_note,
    get_note_from_midi_num,
    get_note_list,
    get_pitch_class_from_note,
    get_midi_nums_list_from_midi_nums_str,
    get_notes_list_from_midi_nums_str,
)
from chord_progressions.progression import Progression, DURATIONS
from chord_progressions.type_templates import (
    TYPE_TEMPLATES,
    get_template_from_template_str,
    get_template_from_notes,
    get_type_from_notes,
    get_type_num_from_type,
)

# Use __all__ to let type checkers know what is part of the public API
__all__ = [
    Chord,
    extract_progression_from_midi,
    get_midi_num_from_note,
    get_note_from_midi_num,
    get_note_list,
    get_pitch_class_from_note,
    get_midi_nums_list_from_midi_nums_str,
    get_notes_list_from_midi_nums_str,
    Progression,
    DURATIONS,
    TYPE_TEMPLATES,
    get_template_from_template_str,
    get_template_from_notes,
    get_type_from_notes,
    get_type_num_from_type,
]
