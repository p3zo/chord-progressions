# Extract

Extract chord progressions from audio or midi.

## Extract chords from a midi file

```python
from chord_progressions.extract.midi import simplify_harmony
from chord_progressions.extract.midi_harman import label_midi

extracted = simplify_harmony('my_file.mid')
harman_labels = label_midi(extracted)
```

[//]: # (TODO: `label_midi_file&#40;&#41;` that takes the filepath directly and returns a progression obj)

## Extract chords from an audio file

```python
from chord_progressions.extract.audio import extract_chords_from_audio
chords, durations, bpm = chords = extract_chords_from_audio('my_file.wav')
```

[//]: # (TODO: `label_audio_file&#40;&#41;` that returns a progression)
