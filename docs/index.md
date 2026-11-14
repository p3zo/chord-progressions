# Introduction

`Chord Progressions` is a Python library of utility functions for working with chord progressions.

## Installation

    $ pip install chord-progressions

## Usage

The simplest way to create a `Progression` is with a list of chords specified in MIDI note numbers.

```python
from chord_progressions import Progression

progression = Progression(chords=[[69, 84, 90, 99], [60, 67, 71, 87, 98]])
```

```json
[
    {
        "id": "ea1b9a6a-e309-4e6a-bad8-04643e652015",
        "ix": 0,
        "duration": "1m",
        "type": "diminished-seventh chord",
        "typeId": 139,
        "notes": [
            "A4",
            "C6",
            "F#6",
            "D#7"
        ],
        "midi_nums": [
            69,
            84,
            90,
            99
        ],
        "metrics": {
            "num_notes": 4,
            "num_pitches": 4,
            "pc_cardinality": 4,
            "interval_class_vector": [
                0,
                0,
                4,
                0,
                0,
                2
            ],
            "ambitus": 30,
            "evenness": 9.65685424949238
        }
    },
    {
        "id": "f36d4b52-9f8f-4b72-8693-34b60f23a564",
        "ix": 1,
        "duration": "1m",
        "type": "minor-major ninth chord",
        "typeId": 101,
        "notes": [
            "C4",
            "G4",
            "B4",
            "D#6",
            "D7"
        ],
        "midi_nums": [
            60,
            67,
            71,
            87,
            98
        ],
        "metrics": {
            "num_notes": 5,
            "num_pitches": 5,
            "pc_cardinality": 5,
            "interval_class_vector": [
                2,
                1,
                2,
                3,
                2,
                0
            ],
            "ambitus": 38,
            "evenness": 13.923559033019178
        }
    }
]
```

Each `Chord` in a `Progression` has the following attributes:

- `id`: a UUID
- `ix`: the index of the chord in the progression
- `type`: the name of the chord, given
  by [this list](https://web.archive.org/web/20221116234056/https://vladimir_ladma.sweb.cz/english/music/structs/mus_rot.htm)
- `typeId`: a unique ID of the chord type
- `duration`: specified in [Tone.Time.Notation](https://github.com/Tonejs/Tone.js/wiki/Time) as one
  of `["8n", "4n", "4n.", "2n", "2n.", "1m", "2m"]`
- `notes`: the MIDI note names of the notes in the chord
- `metrics`: a dictionary of attributes computed based on the notes in the chord

## Key

`Progression.key` estimates the major or minor key of a progression with the Krumhansl-Schmuckler
algorithm (Krumhansl, _Cognitive Foundations of Musical Pitch_, 1990), weighting each note by the
duration of its chord.

```python
Progression(chords=[[48, 64, 67], [53, 65, 69], [55, 59, 65], [48, 64, 67, 72]]).key
# 'C major'
```

## Progression measures

`chord_progressions.progression_measures` measures a whole progression over time. Each function
takes one pitch-class set and/or one length in quarter-note beats per chord, so long chords count
for more than short ones; `DURATION_BEAT_MAPPING` converts Tone.js durations to beats.

- `get_mean_tension`: mean Huron dyadic tension over time.
- `get_pitch_class_emphasis`: the share of time each pitch class sounds.
- `get_contour_fit`: how closely per-chord values, such as tension, follow a target contour over
  time, as a weighted correlation from -1 to 1. Given one row per progression, it measures many
  progressions in one call.
- `get_metric_conflict`: the share of chord changes that fight a 4/4 meter.
- `get_final_lengthening`: the last chord's length relative to the mean.
- `get_transposed_repetition`: how much of the progression restates itself at a new pitch level, as
  in a sequence.
- `returns_to_opening`: whether the progression ends on its opening chord.

```python
from chord_progressions.progression_measures import get_contour_fit, get_metric_conflict

tensions = [-0.6, -0.2, 0.4, -0.6]
beats = [4, 4, 4, 4]
get_contour_fit(tensions, beats, times=(0, 0.6, 1), targets=(0, 1, 0))  # rise, then release
# 0.98...
get_metric_conflict([1.5, 2.5, 4])  # the second chord starts off the beat
# 0.333...
```
