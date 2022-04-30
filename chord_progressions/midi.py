import os

import mido
from chord_progressions import logger
from chord_progressions.pitch import get_midi_num_from_note

DEFAULT_BPM = 120
DEFAULT_MIDI_TICKS_PER_BEAT = 480


def make_midi_chord(chord, start_tick, end_tick):

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


def get_midi_ticks_from_seconds(seconds, bpm, ticks_per_beat):
    midi_tempo = mido.bpm2tempo(bpm)
    return int(mido.second2tick(seconds, ticks_per_beat, midi_tempo))


def get_seconds_from_midi_ticks(ticks, bpm, ticks_per_beat):
    midi_tempo = mido.bpm2tempo(bpm)
    return mido.tick2second(ticks, ticks_per_beat, midi_tempo)


def make_midi_progression(
    chords,
    durations,
    progression_name="",
    ticks_per_beat=DEFAULT_MIDI_TICKS_PER_BEAT,
    bpm=DEFAULT_BPM,
):
    """
    chords: list of lists containing note strings

    durations: list of floats representing seconds
        The length of this list must match the length of `chords`
        The length of a tick is defined in ticks per beat. This value is stored
        as ticks_per_beat in MidiFile objects and remains fixed throughout a track.

    progression_name: str to be in midi track name

    (optional) ticks_per_beat: int

    (optional) bpm: int
    """

    progression = mido.MidiFile(type=0)
    progression.ticks_per_beat = ticks_per_beat

    track = mido.MidiTrack()
    track.name = progression_name
    progression.tracks.append(track)

    for chord, duration in zip(chords, durations):
        tick_duration = get_midi_ticks_from_seconds(duration, bpm, ticks_per_beat)

        chord = make_midi_chord(chord, 0, tick_duration)

        for msg in chord:
            track.append(msg)

    return progression


def save_midi_progression(midi_progression, outpath):
    """
    midi_progression: MidiFile of the entire progression
    outpath: str to be used in filepath
    """
    midi_progression.filename = outpath
    midi_progression.save(outpath)
    logger.info(f"Midi saved to {outpath}")
