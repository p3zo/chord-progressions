import mido
import numpy as np
import pretty_midi
import pytest
from scipy.io import wavfile

from chord_progressions import Chord, Progression
from chord_progressions.extract.midi import parse_notes, smooth_notes
from chord_progressions.extract.midi_harman import label_midi
from chord_progressions.io.audio import SAMPLE_RATE, mk_chord_buffer, save_audio_buffer
from chord_progressions.io.midi import get_midi_from_progression, load_midi_file


def test_midi_round_trip_preserves_pitches_and_durations(tmp_path):
    progression = Progression(
        [[60, 64, 67], [62, 65, 69]], durations=["2n", "4n"], bpm=120
    )
    path = tmp_path / "progression.mid"
    get_midi_from_progression(progression).save(path)
    notes = parse_notes(load_midi_file(str(path)))

    assert notes["note"].tolist() == [60, 64, 67, 62, 65, 69]
    assert notes["start"].tolist() == pytest.approx([0, 0, 0, 1, 1, 1])
    assert notes["end"].tolist() == pytest.approx([1, 1, 1, 1.5, 1.5, 1.5])


def test_chord_and_progression_exports_return_or_save_the_same_result(tmp_path):
    chord = Chord([60, 64, 67])
    path = tmp_path / "chord.mid"
    chord.to_midi(str(path))
    for midi in (chord.to_midi(), mido.MidiFile(str(path))):
        notes = [m.note for m in midi.tracks[0] if m.type == "note_on"]
        assert notes == [60, 64, 67]

    progression = Progression(
        [[60, 64, 67], [62, 65, 69]], durations=["2n", "4n"], bpm=120
    )
    assert isinstance(progression.to_midi(), mido.MidiFile)
    # Half a note and a quarter note at 120 bpm: 1.5 seconds.
    assert len(progression.to_audio()) == int(1.5 * SAMPLE_RATE)


def test_repeated_notes_are_smoothed_without_changing_other_pitches():
    notes = np.array(
        [(0, 0.1, 60), (0.1, 0.2, 60), (0, 0.2, 64)],
        dtype=[("start", float), ("end", float), ("note", int)],
    )
    result = smooth_notes(notes, 0.5)
    assert result["note"].tolist() == [60, 64]
    assert result["start"].tolist() == [0, 0]
    assert result["end"].tolist() == pytest.approx([0.2, 0.2])


def test_harmonic_labels_preserve_segment_boundaries():
    midi = pretty_midi.PrettyMIDI()
    instrument = pretty_midi.Instrument(program=0)
    for start, pitches in [(0, [60, 64, 67]), (1, [62, 65, 69]), (2, [67, 71, 74])]:
        for pitch in pitches:
            instrument.notes.append(pretty_midi.Note(100, pitch, start, start + 1))
    midi.instruments.append(instrument)

    labels = label_midi(midi)
    assert [label["label"] for label in labels] == [
        "major chord", "minor chord", "major chord"
    ]
    assert [label["start_time"] for label in labels] == [0, 1, 2]
    assert [label["end_time"] for label in labels] == [1, 2, 3]


def test_audio_round_trip_preserves_samples(tmp_path):
    samples = mk_chord_buffer(["C4", "E4", "G4"], 0.01, 2)
    assert samples.dtype == np.float32
    assert len(samples) == int(SAMPLE_RATE * 0.01)
    assert np.isfinite(samples).all()
    assert np.max(np.abs(samples)) > 0

    path = tmp_path / "chord.wav"
    save_audio_buffer(samples, path)
    sample_rate, restored = wavfile.read(path)
    assert sample_rate == SAMPLE_RATE
    np.testing.assert_array_equal(restored, samples)
