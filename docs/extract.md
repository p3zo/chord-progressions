# Extract

An API is provided to automatically extract chord progressions from audio and midi. These functions are experimental and
the quality of the results may vary greatly between types of music.

## Extract chords from a midi file

```python

from chord_progressions import extract_progression_from_midi

progression = extract_progression_from_midi('my_file.mid')
```

## Extract chords from an audio file

NOTE: this requires installing [Essentia](http://essentia.upf.edu/documentation/installing.html) with Python bindings which is not included in this library.

```python
from chord_progressions.extract import extract_progression_from_audio

progression = extract_progression_from_audio('my_file.wav')
```
