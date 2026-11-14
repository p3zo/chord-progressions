# Extract

Turn recordings into progressions. Both extractors are experimental, and how well they work varies a lot between
kinds of music.

## From MIDI

```python
from chord_progressions import extract_progression_from_midi

progression = extract_progression_from_midi("song.mid")
```

The result is a [`Progression`](progressions.md) with the file's tempo and named after the file. Chord durations
are rounded to the closest [supported duration](progressions.md#durations).

Before labeling chords, the notes are simplified. These parameters control that, each as a fraction of a whole
note:

| Argument        | Default | Meaning                                                            |
|-----------------|---------|--------------------------------------------------------------------|
| `shortest_note` | `1/64`  | notes shorter than this are dropped                                |
| `smooth_beat`   | `1`     | repeated notes closer together than this are joined into one       |
| `quantize_beat` | `1/2`   | note starts and ends are moved to the closest multiple of this     |

To inspect the steps, pass `simplified_path` to write the simplified notes as a MIDI file, and
`harman_labels_path` to write the chord labels as a CSV file.

The file needs a tempo; when it changes tempo, the first one is used throughout.

Method: chords are labeled with the HarmAn algorithm from [Pardo and Birmingham, 2002][harman]
([PDF][harman-pdf]).

## From audio

Requires [Essentia](https://essentia.upf.edu/installing.html) with its Python bindings, which is not installed
with this library.

```python
from chord_progressions.extract.audio import extract_progression_from_audio

progression = extract_progression_from_audio("song.wav", plot_dir="plots", marked_audio_dir="beats")
```

`plot_dir` receives a plot of the pitch-class profile over time and `marked_audio_dir` a copy of the audio with
the detected beats marked. Both directories must exist.

Method: pitch-class profiles (HPCP) from [Gómez, 2006, as implemented in Essentia][hpcp], averaged over each bar.

[harman]: https://doi.org/10.1162/014892602760137167
[harman-pdf]: https://interactiveaudiolab.github.io/assets/papers/pardo-birmingham-cmj02.pdf
[hpcp]: https://essentia.upf.edu/reference/std_HPCP.html
