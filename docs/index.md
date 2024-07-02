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
