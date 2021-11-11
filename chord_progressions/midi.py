import os

import mido
from chord_progressions import MIDI_OUTPUT_DIR, logger
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
    run_id,
    ticks_per_beat=DEFAULT_MIDI_TICKS_PER_BEAT,
    bpm=DEFAULT_BPM,
):
    """
    chords: list of lists containing note strings
    durations: list of floats representing seconds
        The length of this list must match the length of `chords`
    bpm: int
    ticks_per_beat: int
        The length of a tick is defined in ticks per beat. This value is stored
        as ticks_per_beat in MidiFile objects and remains fixed throughout a track.
    run_id: str to be used in filepath and in midi track name
    """

    progression = mido.MidiFile(type=0)
    progression.ticks_per_beat = ticks_per_beat

    track = mido.MidiTrack()
    track.name = run_id
    progression.tracks.append(track)

    for chord, duration in zip(chords, durations):
        tick_duration = get_midi_ticks_from_seconds(duration, bpm, ticks_per_beat)

        chord = make_midi_chord(chord, 0, tick_duration)

        for msg in chord:
            track.append(msg)

    return progression


def save_midi_progression(midi_progression, run_id, output_dir):
    """
    midi_progression: MidiFile of the entire progression
    run_id: str to be used in filepath and in midi track name
    output_dir: str, path to directory
    """
    filename = f"{run_id}.mid"
    midi_progression.filename = filename

    filepath = os.path.join(output_dir, filename)
    midi_progression.save(filepath)

    logger.info(f"Midi saved to {filepath}")
