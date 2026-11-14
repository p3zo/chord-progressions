# Chord Progressions

A Python library for building, inspecting, measuring and exporting chord progressions.

## Installation

Requires Python 3.12 or newer.

    $ pip install chord-progressions

## Quick start

```python
from chord_progressions import Progression

progression = Progression(
    [["C3", "E4", "G4"], ["F3", "A4", "C5"], ["G3", "B3", "D4", "F4"], ["C3", "E4", "G4", "C5"]],
    durations=["2n", "2n", "1m", "1m"],
    bpm=100,
)

[chord.type for chord in progression]
# ['major chord', 'major chord', 'dominant-seventh / german-sixth chord', 'major chord']

progression.key
# 'C major'

progression.to_midi("progression.mid")
progression.to_audio("progression.wav")
```

## Guide

- [Chords](chords.md): create chords from MIDI numbers or note names, and read their notes, type and metrics.
- [Progressions](progressions.md): sequence chords with durations and a tempo, find the key, and export MIDI,
  audio or JSON.
- [Notes and chord types](notes-and-types.md): convert between MIDI numbers, note names, pitch classes and
  frequencies, and look up chord types.
- [Measures](measures.md): score chords and whole progressions, such as tension, roughness, voice leading and
  how tension changes over time.
- [Extract](extract.md): turn MIDI or audio files into progressions.
- [Glossary](glossary.md): the names and formats used throughout the library.
