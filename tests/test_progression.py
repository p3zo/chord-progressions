from chord_progressions.progression import Progression


def test_instantiate_progression():
    chords = [["C2", "A4", "G6"], ["C-1", "A4", "G9"]]
    p = Progression(chords=chords)
    assert len(p) == len(chords)
