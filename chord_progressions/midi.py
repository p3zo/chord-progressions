import os

import mido

from chord_progressions import MIDI_OUTPUT_DIR, logger
from chord_progressions.pitch import get_midi_num_from_note

BPM = 120
MIDI_TEMPO = mido.bpm2tempo(BPM)
MIDI_TICKS_PER_BEAT = 480


def mk_midi_chord(chord, start_tick, end_tick):

    note_onsets = []
    note_offsets = []

    first_note = True
    for note in chord:

        note = get_midi_num_from_note(note)

        note_onsets.append(mido.Message("note_on", note=note, time=start_tick))

        if not first_note:
            end_tick = 0

        note_offsets.append(mido.Message("note_off", note=note, time=end_tick))
        first_note = False

    return note_onsets + note_offsets


def get_midi_ticks_from_seconds(seconds):
    return int(mido.second2tick(seconds, MIDI_TICKS_PER_BEAT, MIDI_TEMPO))


def mk_midi_progression(chords, durations, run_id):

    progression = mido.MidiFile(type=0)

    track = mido.MidiTrack()
    track.name = run_id
    progression.tracks.append(track)

    track.append(mido.MetaMessage("set_tempo", tempo=MIDI_TEMPO, time=0))

    for chord, duration in zip(chords, durations):

        tick_duration = get_midi_ticks_from_seconds(duration)

        chord = mk_midi_chord(chord, 0, tick_duration)

        for msg in chord:
            track.append(msg)

    return progression


def save_midi_progression(run_id, chords, durations):

    midi_progression = mk_midi_progression(chords, durations, run_id)

    filepath = os.path.join(MIDI_OUTPUT_DIR, f"{run_id}.mid")
    midi_progression.save(filepath)
    logger.info(f"Midi saved to {filepath}")
