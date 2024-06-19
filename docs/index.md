# Introduction

Chord Progressions is a Python library with tools to extract and analyze chord progressions.

## Installation

    $ pip install chord-progressions

## Progressions

The core class of this library is the `Progression`. A progression is a sequence of chords, which can be specified with
a list of MIDI note numbers.

```python
from chord_progressions.progression import Progression

progression = Progression(chords=[[69, 84, 90, 99], [60, 67, 71, 87, 98]])
```

```json
[
  {
    "id": "40664268-1e68-44df-b259-2ce3bb8d4b70",
    "ix": 0,
    "type": "diminished-seventh chord",
    "duration": "1m",
    "typeId": 139,
    "notes": [
      "A4",
      "C6",
      "F#6",
      "D#7"
    ],
    "metrics": {}
  },
  {
    "id": "87bc2fbf-8299-4070-b4db-70fa29c31e9c",
    "ix": 1,
    "type": "minor-major ninth chord",
    "duration": "1m",
    "typeId": 101,
    "notes": [
      "C4",
      "G4",
      "B4",
      "D#6",
      "D7"
    ],
    "metrics": {}
  }
]
```

## Chords

The `Chord` class has the following attributes:

- `id`: a UUID
- `ix`: the index of the chord in the progression
- `type`: the name of the chord, given
  by [this list](https://web.archive.org/web/20221116234056/https://vladimir_ladma.sweb.cz/english/music/structs/mus_rot.htm)
- `typeId`: a unique ID of the chord type
- `duration`: specified in [Tone.Time.Notation](https://github.com/Tonejs/Tone.js/wiki/Time) as one
  of `["8n", "4n", "4n.", "2n", "2n.", "1m", "2m"]`
- `notes`: the MIDI note names of the notes in the chord
- `metrics`: a dictionary of attributes computed based on the notes in the chord
