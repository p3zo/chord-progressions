import mido
from chord_progressions import DEFAULT_MIDI_TICKS_PER_BEAT
from chord_progressions.chord import Chord


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


def get_midi_ticks_from_seconds(
    seconds, bpm, ticks_per_beat=DEFAULT_MIDI_TICKS_PER_BEAT
):
    midi_tempo = mido.bpm2tempo(bpm)
    return int(mido.second2tick(seconds, ticks_per_beat, midi_tempo))


def get_seconds_from_midi_ticks(ticks, bpm, ticks_per_beat=DEFAULT_MIDI_TICKS_PER_BEAT):
    midi_tempo = mido.bpm2tempo(bpm)
    return mido.tick2second(ticks, ticks_per_beat, midi_tempo)
