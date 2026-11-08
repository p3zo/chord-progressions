"""
Key finding with the Krumhansl-Schmuckler algorithm: the key is the major or minor key profile that
best correlates with how long each pitch class sounds.

Krumhansl, Carol L. Cognitive Foundations of Musical Pitch. New York: Oxford, 1990, ch. 4.
Profiles are the probe-tone ratings from Krumhansl & Kessler (1982), starting on the tonic.
"""

import numpy as np

from chord_progressions.pitch import NOTE_NAMES, get_pitch_class_from_midi_num

KEY_PROFILES = {
    "major": [6.35, 2.23, 3.48, 2.33, 4.38, 4.09, 2.52, 5.19, 2.39, 3.66, 2.29, 2.88],
    "minor": [6.33, 2.68, 3.52, 5.38, 2.60, 3.53, 2.54, 4.75, 3.98, 2.69, 3.34, 3.17],
}


def get_pitch_class_durations(midi_nums_list, durations):
    """Sums the duration of every sounding note by pitch class, as a length-12 array"""
    pc_durations = np.zeros(12)

    for midi_nums, duration in zip(midi_nums_list, durations, strict=True):
        for midi_num in midi_nums:
            pc_durations[get_pitch_class_from_midi_num(midi_num)] += duration

    return pc_durations


def get_key_from_pitch_class_durations(pc_durations):
    """Returns the best-correlating key, e.g. "C major" or "F# minor" """
    if np.ptp(pc_durations) == 0:
        raise ValueError(
            "Cannot find a key when every pitch class sounds equally long, or none sound at all"
        )

    correlations = {}
    for mode, profile in KEY_PROFILES.items():
        for tonic in range(12):
            key_profile = np.roll(profile, tonic)
            correlations[f"{NOTE_NAMES[tonic]} {mode}"] = np.corrcoef(key_profile, pc_durations)[0, 1]

    return max(correlations, key=correlations.get)
