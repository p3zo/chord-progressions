"""
    Defines the metrics computed for every progression.

    TODO:
        - A common heuristic is that an interval is consonant when the ratio between the frequencies is simple.
        - Resonance
        - Brilliance: "for maximum brilliance let the lower tones [be somehow equally spaced out as] their overtones"
            - Vincent Persechetti, Twentieth-Century Harmony
        - something like https://en.xen.wiki/w/Harmonic_Entropy
"""

import itertools

import numpy as np
from chord_progressions.pitch import (
    get_freq_from_note,
    get_midi_num_from_note,
    get_n_overtones_harmonic,
    get_pitch_class_from_note,
)
from chord_progressions.type_templates import get_template_from_notes


def get_interval_class_vector(notes):
    """
    Returns a vector of interval classes.
        0: minor second / major seventh (1 or 11 semitones)
        1: major second / minor seventh (2 or 10 semitones)
        2: minor third / major sixth (3 or 9 semitones)
        3: major third / minor sixth (4 or 8 semitones)
        4: perfect fourth / perfect fifth (5 or 7 semitones)
        5: tritone (6 semitones)
    """
    template = get_template_from_notes(notes)
    pitch_classes = [ix for ix, i in enumerate(template) if i == 1]

    return get_interval_class_vector_from_pitch_classes(pitch_classes)


def get_interval_class_vector_from_pitch_classes(pitch_classes):
    """Interval-class vector of a pitch-class set, e.g. [0, 4, 7] -> [0, 0, 1, 1, 1, 0]"""
    vec = [0] * 6

    pairs = itertools.combinations(sorted(set(pitch_classes)), 2)
    intervals = [b - a for a, b in pairs]
    modded = [12 - i if i > 6 else i for i in intervals]

    for i in range(6):
        vec[i] = modded.count(i + 1)

    return vec


def get_evenness(interval_class_vector):
    """
    A rough measure of acoustic consonance. Highly consonant chords divide the octave nearly evenly.
    Note that acoustic consonance implies near-evenness, but not the reverse.
    For background on the equation see https://www.researchgate.net/profile/Jack_Douthett/publication/249881698_Vector_Products_and_Intervallic_Weighting/links/575061d708ae1c34b39aaa1b.pdf
    """
    weight_vector = [0] * 6

    for i in range(6):

        k = i + 1

        weight_vector[i] += 2 * np.sin(k * np.pi / 12)

    weight = np.dot(weight_vector, interval_class_vector)

    return weight


def get_relative_evenness(evenness, cardinality):
    """
    Calculate the evenness of a pitch class set relative to its possible range.
    A relative value is useful because highly-even dyads will have a lower evenness than highly uneven hexachords.
    The result is a value between 0 and 1.
    """
    # TODO: replace this table with a formula
    MIN_MAX_EVENNESS_BY_CARDINALITY = [
        [0.0, 0.0],
        [0.5176380902050415, 2.0],
        [2.035276180410083, 5.196152422706632],
        [6.1815405503520555, 9.65685424949238],
        [9.631030293135233, 15.287884542627612],
        [16.226784405860382, 22.392304845413264],
        [24.822538518585535, 30.479392768077915],
        [35.350144283888824, 40.03987070039298],
        [47.609800856760984, 50.77067709905754],
        [61.28367099200624, 62.7660329018012],
        [75.9575411272515, 75.9575411272515],
        [91.14904935270181, 91.14904935270181],
    ]

    emin, emax = MIN_MAX_EVENNESS_BY_CARDINALITY[cardinality - 1]
    return (evenness - emin) / (emax - emin)


def get_overtone_agreement(notes):

    freqs = [get_freq_from_note(n) for n in notes]

    all_partials = []

    n_overtones = 10
    for f in freqs:
        all_partials.extend(get_n_overtones_harmonic(f, n_overtones))

    sorted_partials = sorted(all_partials)

    sum_of_differences = 0

    for i in range(1, len(sorted_partials)):
        diff = sorted_partials[i] - sorted_partials[i - 1]
        sum_of_differences += diff

    return sum_of_differences


# Huron (1994), "Interval-class content in equally tempered pitch-class sets:
# common scales exhibit optimum tonal consonance", consonance of interval classes 1-6.
HURON_CONSONANCE = np.array([-1.428, -0.582, 0.594, 0.386, 1.240, -0.453])

# Parncutt (1988) root-support weights: interval above a candidate root -> support.
ROOT_SUPPORT = {0: 10, 7: 5, 4: 3, 10: 2, 2: 1}

# Sethares (1993) parametrization of the Plomp-Levelt dissonance curve.
_PL_DSTAR, _PL_S1, _PL_S2, _PL_B1, _PL_B2 = 0.24, 0.0207, 18.96, 3.51, 5.75
_N_PARTIALS = 6
_PARTIAL_AMPLITUDES = 0.88 ** np.arange(_N_PARTIALS)


def get_set_tension(pitch_classes):
    """Mean dyadic dissonance of a pitch-class set (Huron), roughly -1.24 to 1.43.

    A single pitch class has no dyads; it is scored like the most consonant dyad,
    the perfect fifth, since a lone harmonic tone is at least that smooth.
    """
    vector = np.array(get_interval_class_vector_from_pitch_classes(pitch_classes))
    n_dyads = vector.sum()
    if n_dyads == 0:
        return float(-HURON_CONSONANCE.max())
    return float(-(vector @ HURON_CONSONANCE) / n_dyads)


def get_fourier_coefficients(pitch_classes):
    """DFT of a pitch-class set's indicator vector, coefficients 1-6, divided by cardinality.

    Magnitudes measure resemblance to the perfectly even sets (Quinn 2006; Amiot 2016):
    f5 diatonicity, f4 octatonicity, f3 hexatonicity, f6 whole-tone-ness.
    The phase of f5 locates a set on the circle of fifths.
    """
    pitch_classes = np.array(sorted(set(pitch_classes)))
    k = np.arange(1, 7)[:, None]
    return np.exp(-2j * np.pi * k * pitch_classes / 12).sum(axis=1) / len(pitch_classes)


def get_voice_leading_distance(midi_nums_1, midi_nums_2):
    """Smallest total semitone motion between two voicings (Tymoczko 2006).

    Voices may split or merge (doubling) but never cross, which on sorted notes is
    dynamic time warping with an absolute-difference cost.
    """
    a, b = sorted(midi_nums_1), sorted(midi_nums_2)
    # Plain lists and one rolling row: callers use this inside search loops.
    previous = [0.0] + [float("inf")] * len(b)
    for note in a:
        row = [float("inf")]
        for j, other in enumerate(b):
            row.append(abs(note - other) + min(previous[j], previous[j + 1], row[j]))
        previous = row
    return float(previous[-1])


def get_pitch_class_voice_leading_distance(pitch_classes_1, pitch_classes_2):
    """Smallest total motion between pitch-class sets, in semitones around the octave.

    Tries every cyclic alignment of the two sorted sets, so octave equivalence holds.
    """
    a, b = sorted(set(pitch_classes_1)), sorted(set(pitch_classes_2))
    best = float("inf")
    for shift in range(len(b)):
        rotated = b[shift:] + [pc + 12 for pc in b[:shift]]
        for offset in (-12, 0, 12):
            best = min(
                best, get_voice_leading_distance(a, [pc + offset for pc in rotated])
            )
    return best


def get_roughness(midi_nums):
    """Total Plomp-Levelt sensory roughness of a voicing with six harmonic partials."""
    if len(midi_nums) == 0:
        return 0.0
    f0 = 440.0 * 2 ** ((np.asarray(midi_nums, dtype=float) - 69) / 12)
    freqs = (f0[:, None] * np.arange(1, _N_PARTIALS + 1)).ravel()
    amps = np.tile(_PARTIAL_AMPLITUDES, len(f0))
    order = np.argsort(freqs)
    freqs, amps = freqs[order], amps[order]
    low, high = np.triu_indices(len(freqs), k=1)
    s = _PL_DSTAR / (_PL_S1 * freqs[low] + _PL_S2)
    diff = freqs[high] - freqs[low]
    curve = np.exp(-_PL_B1 * s * diff) - np.exp(-_PL_B2 * s * diff)
    return float((amps[low] * amps[high] * curve).sum())


def get_root_salience(pitch_classes):
    """Parncutt root-support score of every pitch class in the set."""
    pitch_classes = set(pitch_classes)
    return {
        root: sum(
            w
            for interval, w in ROOT_SUPPORT.items()
            if (root + interval) % 12 in pitch_classes
        )
        for root in pitch_classes
    }


def evaluate_notes(notes):
    """list of notes, e.g. ["C4", "E4", "G4"]"""

    metrics = {}

    try:

        interval_class_vector = get_interval_class_vector(notes)

        evenness = get_evenness(interval_class_vector)

        pc_cardinality = len(set([get_pitch_class_from_note(n) for n in notes]))
        assert pc_cardinality <= 12, "Pitch class cardinality > 12"

        metrics["num_notes"] = len(notes)
        metrics["num_pitches"] = len(set(notes))
        metrics["pc_cardinality"] = pc_cardinality
        metrics["interval_class_vector"] = interval_class_vector
        metrics["ambitus"] = get_ambitus(notes)
        metrics["evenness"] = evenness
        # metrics["relative_evenness"] = get_relative_evenness(evenness, pc_cardinality)
        # metrics["overtone_agreement"] = get_overtone_agreement(notes)

    except:
        pass

    return metrics


def get_macroharmony(progression):
    """The total collection of notes"""

    collection = set()

    for notes in progression:
        for note in notes:
            collection.add(note)

    return collection


def get_ambitus(macroharmony):
    """Ambitus <int>: the number of semitones between the lowest and highest note"""
    ambitus = 0

    midi_notes = [get_midi_num_from_note(n) for n in macroharmony]
    if midi_notes:
        ambitus = max(midi_notes) - min(midi_notes)

    return ambitus


def evaluate_progression(progression):
    metrics = {}

    # try:
    #     macroharmony = get_macroharmony(notes_list)
    #     metrics["ambitus"] = get_ambitus(macroharmony)
    #     metrics["density"] = len(macroharmony) / len(notes_list)
    # except:
    #     pass

    return metrics


def get_n_overtones_for_notes(notes, n):
    """Calculates `n` overtone frequencies for each note in `notes`"""

    freqs = [get_freq_from_note(n) for n in notes]
    o_freqs = [get_n_overtones_harmonic(f, n) for f in freqs]

    return o_freqs
