# Progressions

A `Progression` is a sequence of chords, each with a duration, played at a tempo.

## Create a progression

Pass `Chord` objects, or lists of MIDI numbers or note names that become chords.

```python
from chord_progressions import Chord, Progression

progression = Progression(
    [[48, 64, 67], [53, 69, 72], [55, 59, 62, 65], [48, 64, 67, 72]],
    durations=["2n", "2n", "1m", "1m"],
    bpm=100,
    name="I IV V7 I",
)

Progression([Chord(["C4", "E4", "G4"]), Chord(["D4", "F4", "A4"])])
```

| Argument    | Default | Meaning                                                    |
|-------------|---------|------------------------------------------------------------|
| `chords`    | `[]`    | the chords                                                 |
| `durations` | a whole bar (`"1m"`) per chord | one duration per chord, see below   |
| `bpm`       | `120`   | tempo in beats per minute; a beat is a quarter note        |
| `name`      | `""`    | a name for the progression                                 |

## Durations

Durations use [Tone.js time notation](https://github.com/Tonejs/Tone.js/wiki/Time). These are supported:

| Duration | Length           | Beats |
|----------|------------------|-------|
| `"8n"`   | eighth note      | 0.5   |
| `"4n"`   | quarter note     | 1     |
| `"4n."`  | dotted quarter   | 1.5   |
| `"2n"`   | half note        | 2     |
| `"2n."`  | dotted half      | 3     |
| `"1m"`   | one 4/4 bar      | 4     |
| `"2m"`   | two 4/4 bars     | 8     |

They are available as `DURATIONS`, and their lengths in beats as `DURATION_BEAT_MAPPING`.

Durations can also be given in seconds; each is rounded to the closest supported duration at the progression's
tempo.

```python
Progression([[60, 64, 67], [62, 65, 69]], durations=[1.2, 0.6], bpm=100).durations
# ['2n', '4n']
```

To convert yourself:

```python
from chord_progressions.progression import (
    DURATION_BEAT_MAPPING,
    duration_to_seconds,
    seconds_to_duration,
)

duration_to_seconds("2n", bpm=100)  # 1.2
seconds_to_duration(1.2, bpm=100)   # '2n'
```

## Read a progression

A progression behaves like a list of its chords.

```python
len(progression)                    # 4
progression[0].notes                # ['C3', 'E4', 'G4']
[chord.type for chord in progression]
progression.durations               # ['2n', '2n', '1m', '1m']
progression.bpm                     # 100
progression.get_durations_in_seconds()
# [1.2, 1.2, 2.4, 2.4]
```

## Key

`key` estimates the major or minor key that best fits the progression, with longer chords counting for more.

```python
progression.key
# 'C major'
```

It raises a `ValueError` when no key fits, as when every pitch class sounds for the same length of time.

Method: Krumhansl–Schmuckler key finding, from [Krumhansl, _Cognitive Foundations of Musical Pitch_][krumhansl],
as implemented by [music21](https://www.music21.org/).

## Export a progression

```python
progression.to_midi("progression.mid")   # one track at the progression's tempo
progression.to_audio("progression.wav")  # synthesized with 4 overtones per note; n_overtones=… to change
progression.to_json()
# [{'id': '…', 'ix': 0, 'duration': '2n', 'type': 'major chord', 'typeId': 63,
#   'notes': ['C3', 'E4', 'G4'], 'midi_nums': [48, 64, 67], 'metrics': {…}},
#  …]
```

Without a path, `to_midi()` returns a [`mido.MidiFile`](https://mido.readthedocs.io/en/stable/files/midi.html)
and `to_audio()` returns the samples as a NumPy array at 44.1 kHz. `to_json()` returns one entry per chord,
with its position (`ix`) and duration.

[krumhansl]: https://doi.org/10.1093/acprof:oso/9780195148367.001.0001
