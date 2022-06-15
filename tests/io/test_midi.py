from chord_progressions.io.midi import to_midi


def test_to_midi():
    mid = to_midi()
    assert mid is not None
