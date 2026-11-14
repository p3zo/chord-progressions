# Measures

Functions that score chords, pairs of chords and whole progressions. Each links to the paper that defines the
method.

Most take pitch-class sets: lists of integers from 0 (C) to 11 (B), such as `[0, 4, 7]` for a C major triad.
Those that depend on register take MIDI numbers instead.

## Chord measures

In `chord_progressions.evaluate`.

```python
from chord_progressions.evaluate import (
    get_evenness,
    get_fourier_coefficients,
    get_interval_class_vector_from_pitch_classes,
    get_root_salience,
    get_roughness,
    get_set_tension,
)
```

| Function                                       | Input             | Returns                                             | Method |
|------------------------------------------------|-------------------|-----------------------------------------------------|--------|
| `get_interval_class_vector_from_pitch_classes` | pitch classes     | count of each interval class, minor second to tritone; `get_interval_class_vector` takes note names | |
| `get_set_tension`                              | pitch classes     | mean dissonance of the set's intervals, from about -1.24 (consonant) to 1.43 | [Huron, 1994][huron] |
| `get_roughness`                                | MIDI numbers      | sensory roughness of the voicing, from 0 up          | [Plomp and Levelt, 1965][plomp]; parameters from [Sethares, 1993][sethares] |
| `get_root_salience`                            | pitch classes     | how strongly each pitch class sounds like the root   | [Parncutt, 1988][parncutt] |
| `get_fourier_coefficients`                     | pitch classes     | coefficients 1 to 6 of the set's discrete Fourier transform, as complex numbers | [Quinn, 2006][quinn]; [Amiot, 2016][amiot] |
| `get_evenness`                                 | interval-class vector | how evenly the set divides the octave           | [Block and Douthett, 1994][douthett] |

```python
get_interval_class_vector_from_pitch_classes([0, 4, 7])  # [0, 0, 1, 1, 1, 0]
get_set_tension([0, 4, 7])       # -0.74
get_set_tension([0, 1, 2])       # 1.146
get_roughness([48, 52, 55])      # 1.377...
get_root_salience([0, 4, 7])     # {0: 18, 4: 10, 7: 10}
abs(get_fourier_coefficients([0, 2, 4, 5, 7, 9, 11])[4])  # 0.533..., the fifth coefficient
get_evenness([0, 0, 1, 1, 1, 0])  # 5.078...
```

## Voice leading

```python
from chord_progressions.evaluate import (
    get_pitch_class_voice_leading_distance,
    get_voice_leading_distance,
)

get_voice_leading_distance([60, 64, 67], [60, 65, 69])         # 3.0 semitones
get_pitch_class_voice_leading_distance([0, 4, 7], [5, 9, 0])  # 3.0 semitones
```

`get_voice_leading_distance` takes two voicings in MIDI numbers and returns the smallest total motion in
semitones, letting voices split or merge but not cross. `get_pitch_class_voice_leading_distance` does the same
for pitch-class sets, ignoring octaves. Method: [Tymoczko, 2006][tymoczko].

## Progression measures

In `chord_progressions.progression_measures`. Each function takes one pitch-class set and/or one length in
beats per chord, so longer chords count for more. A beat is a quarter note; convert durations with
`DURATION_BEAT_MAPPING` (see [Durations](progressions.md#durations)).

```python
from chord_progressions.progression_measures import (
    get_contour_fit,
    get_final_lengthening,
    get_mean_tension,
    get_metric_conflict,
    get_pitch_class_emphasis,
    get_transposed_repetition,
    returns_to_opening,
)

C, F, G7 = [0, 4, 7], [5, 9, 0], [7, 11, 2, 5]
chords = [C, F, G7, C]
beats = [2, 2, 4, 4]
```

| Function                    | Returns                                                                | Method |
|-----------------------------|------------------------------------------------------------------------|--------|
| `get_mean_tension`          | `get_set_tension` averaged over time                                   | [Huron, 1994][huron] |
| `get_pitch_class_emphasis`  | 12 values, C first and summing to 1: the share of time each pitch class sounds | |
| `get_contour_fit`           | how closely per-chord values follow a target shape over time, from -1 (inverted) to 1 (exact) | |
| `get_metric_conflict`       | share of chord changes that fight a 4/4 meter, from 0 to 1             | [Lerdahl and Jackendoff, 1983][gttm] |
| `get_final_lengthening`     | length of the last chord relative to the mean chord length             | |
| `get_transposed_repetition` | share of chords that restate an earlier chord at a new pitch level, as in a sequence, from 0 to 1 | |
| `returns_to_opening`        | whether a progression of three or more chords ends on its opening chord | |

```python
get_mean_tension(chords, beats)              # -0.592...
get_pitch_class_emphasis([C, G7], [3, 1])    # array([0.231, 0., 0.077, …])
get_metric_conflict([4, 4, 4, 4])            # 0.0
get_metric_conflict([1.5, 2.5, 4])           # 0.333..., the second chord starts off the beat
get_final_lengthening(beats)                 # 1.333..., the last chord is a third longer than average
get_transposed_repetition([[0, 4, 7], [2, 6, 9], [4, 8, 11]])  # 1.0, C D E major
returns_to_opening(chords)                   # True
```

### Contour fit

`get_contour_fit(values, beats, times, targets)` compares one value per chord, such as its tension, with a
target shape. The shape is drawn through `(time, target)` points, with time running from 0 at the start of the
progression to 1 at its end. Only the shape matters, not the level or scale of the values; constant values score
0.

```python
tensions = [get_set_tension(chord) for chord in chords]

# Rise to a peak 60% of the way through, then release.
get_contour_fit(tensions, [4, 4, 4, 4], times=(0, 0.6, 1), targets=(0, 1, 0))
# 0.843...
```

To score many progressions with the same number of chords, give `values`, `beats` or both one row per
progression. This returns one fit per row and is much faster than one call each. A single row is compared with
every row of the other argument.

```python
get_contour_fit(tensions, [[4, 4, 4, 4], [2, 2, 8, 4], [8, 4, 2, 2]], times=(0, 0.6, 1), targets=(0, 1, 0))
# array([ 0.843...,  0.976..., -0.076...])
```

[huron]: https://doi.org/10.2307/40285624
[plomp]: https://doi.org/10.1121/1.1909741
[sethares]: https://doi.org/10.1121/1.408175
[parncutt]: https://doi.org/10.2307/40285416
[quinn]: https://doi.org/10.1353/pnm.2006.0010
[amiot]: https://doi.org/10.1007/978-3-319-45581-5
[douthett]: https://doi.org/10.2307/843826
[tymoczko]: https://doi.org/10.1126/science.1126287
[gttm]: https://doi.org/10.7551/mitpress/12513.001.0001
