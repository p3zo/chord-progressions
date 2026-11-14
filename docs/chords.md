# Chords

A `Chord` is a set of unique notes.

## Create a chord

Give the notes as MIDI numbers or as note names. Duplicates are dropped and the notes are sorted from low to high.

```python
from chord_progressions import Chord

Chord([60, 64, 67])
Chord(["C4", "E4", "G4"])

Chord([67, 60, 64, 60]).midi_nums
# [60, 64, 67]
```

MIDI numbers must be between 0 and 128.

## Read a chord

```python
chord = Chord([60, 64, 67])

chord.midi_nums  # [60, 64, 67]
chord.notes      # ['C4', 'E4', 'G4']
chord.type       # 'major chord'
chord.typeId     # 63
chord.template   # [1, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0]
chord.id         # a random UUID, unless one is passed: Chord([60, 64, 67], id="tonic")
```

`type` is the chord's name in [Vladimir Ladma's list of pitch-class sets][ladma]; the names and their ids are
covered in [Notes and chord types](notes-and-types.md#chord-types). `template` marks which of the 12 pitch
classes, starting at C, the chord contains.

`metrics` holds measures of the chord's notes:

```python
chord.metrics
# {'num_notes': 3, 'num_pitches': 3, 'pc_cardinality': 3,
#  'interval_class_vector': [0, 0, 1, 1, 1, 0], 'ambitus': 7, 'evenness': 5.078...}
```

| Key                     | Meaning                                                              |
|-------------------------|----------------------------------------------------------------------|
| `num_notes`             | number of notes                                                      |
| `num_pitches`           | number of distinct notes                                             |
| `pc_cardinality`        | number of distinct pitch classes                                     |
| `interval_class_vector` | count of each interval class, from minor second to tritone           |
| `ambitus`               | semitones between the lowest and highest note                        |
| `evenness`              | how evenly the pitch classes divide the octave ([Block and Douthett, 1994][douthett]) |

More measures are available as functions; see [Measures](measures.md#chord-measures).

## Export a chord

```python
chord.to_json()
# {'id': '…', 'midi_nums': [60, 64, 67], 'type': 'major chord', 'typeId': 63,
#  'notes': ['C4', 'E4', 'G4'], 'metrics': {…}}

chord.to_midi("chord.mid")   # one second of the chord at 120 bpm
chord.to_audio("chord.wav")  # one second of the chord, synthesized with 4 overtones per note
```

Without a path, `to_midi()` returns a [`mido.MidiFile`](https://mido.readthedocs.io/en/stable/files/midi.html)
and `to_audio()` returns the samples as a NumPy array at 44.1 kHz.

[ladma]: https://web.archive.org/web/20221116234056/https://vladimir_ladma.sweb.cz/english/music/structs/mus_rot.htm
[douthett]: https://doi.org/10.2307/843826
