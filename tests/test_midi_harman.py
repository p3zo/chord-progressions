import pretty_midi

from chord_progressions.extract import midi_harman
from chord_progressions.extract.midi_harman import label_midi

# C major, F major, A minor, G dominant seventh
PROGRESSION = [[60, 64, 67], [65, 69, 72], [57, 60, 64], [55, 59, 62, 65]]


def make_midi(chords, arpeggiate=False):
    midi = pretty_midi.PrettyMIDI()
    instrument = pretty_midi.Instrument(program=0)
    for start, pitches in enumerate(chords):
        for ix, pitch in enumerate(pitches):
            if arpeggiate:
                step = 1 / len(pitches)
                note = pretty_midi.Note(100, pitch, start + ix * step, start + (ix + 1) * step)
            else:
                note = pretty_midi.Note(100, pitch, start, start + 1)
            instrument.notes.append(note)
    midi.instruments.append(instrument)
    return midi


def test_consecutive_chords_of_the_same_type_are_separate_segments():
    labels = label_midi(make_midi(PROGRESSION))
    assert [(label["label"], label["notes"]) for label in labels] == [
        ("major chord", ["C4", "E4", "G4"]),
        ("major chord", ["F4", "A4", "C5"]),
        ("minor chord", ["A3", "C4", "E4"]),
        ("dominant-seventh / german-sixth chord", ["G3", "B3", "D4", "F4"]),
    ]
    assert [label["start_time"] for label in labels] == [0, 1, 2, 3]


def test_arpeggiated_chords_are_grouped_like_block_chords():
    # Neighboring chords share no notes: a shared note joins the segment before it
    progression = [[60, 64, 67], [62, 65, 69], [64, 67, 71], [65, 69, 72]]
    labels = label_midi(make_midi(progression, arpeggiate=True))
    assert [label["notes"] for label in labels] == [
        ["C4", "E4", "G4"],
        ["D4", "F4", "A4"],
        ["E4", "G4", "B4"],
        ["F4", "A4", "C5"],
    ]
    assert [label["start_time"] for label in labels] == [0, 1, 2, 3]


def test_each_minimal_segment_is_scored_once(monkeypatch):
    calls = []
    original = midi_harman.get_label_scores

    def counting_get_label_scores(pc_weights):
        calls.append(1)
        return original(pc_weights)

    monkeypatch.setattr(midi_harman, "get_label_scores", counting_get_label_scores)

    midi = make_midi(PROGRESSION * 20, arpeggiate=True)
    num_minimal_segments = len(
        midi_harman.get_minimal_segments(
            midi_harman.get_partition_points(midi_harman.parse_events(midi))
        )
    )
    label_midi(midi)

    assert len(calls) == num_minimal_segments
