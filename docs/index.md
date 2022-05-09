# Introduction

Chord Progressions is a Python library with tools to help extract, analyze, and generate chord progressions.

This library defines a chord as a set of two or more notes, and a chord progression as an ordered sequence of chords
with specified durations. Various theories of music have more specific definitions of these concepts. This library
imposes few constraints in order to be useful for many musical contexts.

## Installation

    $ pip install chord-progressions

## Progressions

The core class of this library is the `Progression`.

Below is an example of a progression with two chords.

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
    "locked": "0",
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
    "locked": "0",
    "metrics": {}
  }
]
```
