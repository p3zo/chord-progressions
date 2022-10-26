# Extract

Experimental functions for automatically extracting chord progressions from audio and midi.

## Extract chords from a midi file

```python
from chord_progressions.extract.midi import simplify_harmony
from chord_progressions.extract.midi_harman import label_midi

extracted = simplify_harmony('my_file.mid')
harman_labels = label_midi(extracted)
```

## Extract chords from an audio file

```python
from chord_progressions.extract.audio import extract_progression_from_audio

progression = extract_progression_from_audio('my_file.wav')
```

## Eventual interface

```python
import chord_progressions
progression = chord_progressions.Progression.from_audio('my_file.wav')
progression = chord_progressions.Progression.from_midi('my_file.mid')
```
