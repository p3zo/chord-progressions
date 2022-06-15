import mido
from chord_progressions.chord import Chord
from chord_progressions.progression import Progression

# TODO: double-check that this conditional import avoids circular import
# TODO: double-check that there would be a circular import at runtime without this
# from typing import TYPE_CHECKING
# if TYPE_CHECKING:
#     from chord_progressions.progression import Progression


DEFAULT_BPM = 120
DEFAULT_MIDI_TICKS_PER_BEAT = 480


def get_midi_ticks_from_seconds(seconds, bpm, ticks_per_beat):
    midi_tempo = mido.bpm2tempo(bpm)
    return int(mido.second2tick(seconds, ticks_per_beat, midi_tempo))


def make_midi_chord(chord: Chord, end_tick: int):
    note_onsets = []
    note_offsets = []

    first_note = True
    for midi_num in chord.midi_nums:
        note_onsets.append(mido.Message("note_on", note=midi_num, time=0))

        if not first_note:
            end_tick = 0

        note_offsets.append(mido.Message("note_off", note=midi_num, time=end_tick))
        first_note = False

    return note_onsets + note_offsets


def make_midi_progression(
    progression: Progression,
    name="",
    ticks_per_beat=DEFAULT_MIDI_TICKS_PER_BEAT,
    bpm=DEFAULT_BPM,
):
    mid = mido.MidiFile(type=0)
    mid.ticks_per_beat = ticks_per_beat

    track = mido.MidiTrack()
    track.name = name
    mid.tracks.append(track)

    for chord in progression.chords:
        tick_duration = get_midi_ticks_from_seconds(chord.duration, bpm, ticks_per_beat)
        chord = make_midi_chord(chord, tick_duration)

        for msg in chord:
            track.append(msg)

    return mid


def to_midi(
    progression: Progression,
    name="",
    ticks_per_beat=DEFAULT_MIDI_TICKS_PER_BEAT,
    bpm=DEFAULT_BPM,
):
    mid = mido.MidiFile(type=0)
    mid.ticks_per_beat = ticks_per_beat

    track = mido.MidiTrack()
    track.name = name
    mid.tracks.append(track)

    for chord in progression.chords:
        duration_ticks = get_midi_ticks_from_seconds(
            chord.duration, bpm, ticks_per_beat
        )
        chord = make_midi_chord(chord, duration_ticks)

        for msg in chord:
            track.append(msg)

    return mid
