from chord_progressions.chord import Chord
from chord_progressions.progression import Progression


def test_instantiate_progression():
    chords = [Chord(["C2", "A4", "G6"]), Chord(["C-1", "A4", "G9"])]
    p = Progression(chords=chords)
    assert len(p) == len(chords)


def test_get_new_solution():
    chords = [Chord(["C2", "A4", "G6"]), Chord(["C-1", "A4", "G9"])]
    p = Progression(chords=chords)
    p2 = p.get_new_solution()

    assert p.chords[0].id != p2.chords[0].id
    assert p.chords[1].id != p2.chords[1].id
