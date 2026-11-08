"""Measures of a whole progression over time.

Each function takes one pitch-class set (an iterable of ints in 0-11) and/or one
length in quarter-note beats per chord, so a long chord counts for more than a
short one. Use `DURATION_BEAT_MAPPING` from `chord_progressions.progression` to
convert Tone.js durations to beats.
"""

from functools import lru_cache

import numpy as np
from chord_progressions.evaluate import get_set_tension


def _mask(pitch_classes):
    """A pitch-class set as a 12-bit integer, C in the lowest bit; cheap to compare and transpose."""
    return sum(1 << pc for pc in set(pitch_classes))


def _transpose(mask, step):
    return ((mask << step) | (mask >> (12 - step))) & 0xFFF


@lru_cache(maxsize=4096)
def _tension(mask):
    return get_set_tension([pc for pc in range(12) if mask >> pc & 1])


def _weights(beats):
    beats = np.asarray(beats, dtype=float)
    if len(beats) == 0 or np.any(beats <= 0):
        raise ValueError("Every chord needs a positive length in beats")
    return beats / beats.sum()


def get_mean_tension(pitch_class_sets, beats):
    """Mean `get_set_tension` over time: each chord weighted by its length."""
    tensions = [_tension(_mask(pcs)) for pcs in pitch_class_sets]
    return float(_weights(beats) @ tensions)


def get_pitch_class_emphasis(pitch_class_sets, beats):
    """Share of the progression's length during which each pitch class sounds.

    Returns 12 values, C first, summing to 1.
    """
    weights = np.zeros(12)
    for pcs, length in zip(pitch_class_sets, _weights(beats), strict=True):
        for pc in set(pcs):
            weights[pc] += length
    return weights / weights.sum()


def get_contour_fit(values, beats, times, targets):
    """How closely per-chord values follow a target contour over time, from -1 to 1.

    The contour is linear between (time, target) breakpoints, with time running from
    0 at the start of the progression to 1 at its end. Each chord is compared at the
    midpoint of its span and weighted by its length; the result is the weighted
    Pearson correlation, so it measures shape, not level or scale. 1 follows the
    contour exactly, -1 inverts it, and 0 means no relation, including when either
    the values or the sampled contour are constant.

    For example, with `get_set_tension` values and breakpoints (0, 0.6, 1) to
    (0, 1, 0), it measures how well tension rises to a peak 60% of the way through
    and then releases.
    """
    weights = _weights(beats)
    lengths = np.asarray(beats, dtype=float)
    midpoints = (np.cumsum(lengths) - lengths / 2) / lengths.sum()
    target = np.interp(midpoints, times, targets)
    values = np.asarray(values, dtype=float)
    values_dev = values - weights @ values
    target_dev = target - weights @ target
    spread = np.sqrt((weights @ values_dev**2) * (weights @ target_dev**2))
    if spread == 0:
        return 0.0
    return float((weights @ (values_dev * target_dev)) / spread)


def get_metric_conflict(beats):
    """Share of chord changes that fight a 4/4 meter, from 0 to 1.

    A change off the beat counts 1. A chord of a half note or longer that starts on
    beat 2 or 4 counts 0.5, since long harmonies sound syncopated unless they begin
    on the strong beats 1 and 3 (after Lerdahl and Jackendoff's metrical preference
    for harmonic change on strong beats). Assumes the progression starts on beat 1.
    """
    _weights(beats)
    onset, conflicts = 0.0, []
    for length in beats:
        if onset % 1:
            conflicts.append(1.0)
        elif length >= 2 and onset % 2:
            conflicts.append(0.5)
        else:
            conflicts.append(0.0)
        onset += length
    return float(np.mean(conflicts))


def get_final_lengthening(beats):
    """Length of the last chord relative to the mean chord length.

    Phrases tend to end on longer notes and chords; values of 1 or more mean the
    progression ends at least as long as it goes.
    """
    lengths = np.asarray(beats, dtype=float)
    _weights(lengths)
    return float(lengths[-1] / lengths.mean())


def get_transposed_repetition(pitch_class_sets, periods=(1, 2, 3)):
    """How much of a progression restates itself at a new pitch level, from 0 to 1.

    For each period p and transposition, counts the chords that equal the chord p
    places earlier transposed by that one interval, as in a sequence; returns the
    largest share of chords explained this way. A chord equal to the chord just
    before it is stasis, not repetition, so it never counts.
    """
    sets = [_mask(pcs) for pcs in pitch_class_sets]
    n = len(sets)
    best = 0.0
    for period in periods:
        if n < 2 * period + 1:
            continue
        for step in range(12):
            hits = sum(
                sets[ix] == _transpose(sets[ix - period], step)
                and sets[ix] != sets[ix - 1]
                for ix in range(period, n)
            )
            best = max(best, hits / (n - period))
    return best


def returns_to_opening(pitch_class_sets):
    """Whether a progression of three or more chords that moves ends on its opening chord."""
    sets = [_mask(pcs) for pcs in pitch_class_sets]
    return len(sets) >= 3 and sets[-1] == sets[0] and len(set(sets)) > 1
