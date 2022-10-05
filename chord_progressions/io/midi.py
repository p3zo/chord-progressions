import warnings

import mido
import pretty_midi
from chord_progressions import DEFAULT_BPM, DEFAULT_MIDI_TICKS_PER_BEAT
from chord_progressions.midi import get_midi_ticks_from_seconds, make_midi_chord


def load_midi_file(filepath):
    # warnings can be verbose when midi has no metadata e.g. tempo, key, time signature
    with warnings.catch_warnings():
        warnings.filterwarnings("ignore", category=RuntimeWarning)
        try:
            midi = pretty_midi.PrettyMIDI(filepath)
        except Exception as e:
            print(f"Failed loading file {filepath}: {e}")
            return

    return midi


def get_midi_from_progression(
    chords,
    durations_seconds,
    bpm=DEFAULT_BPM,
    name="",
    ticks_per_beat=DEFAULT_MIDI_TICKS_PER_BEAT,
):
    mid = mido.MidiFile(type=0)
    mid.ticks_per_beat = ticks_per_beat

    track = mido.MidiTrack()
    track.name = name
    mid.tracks.append(track)

    # write a set tempo message with the bpm in microseconds per beat
    midi_tempo = mido.bpm2tempo(bpm)
    track.append(mido.MetaMessage(type="set_tempo", tempo=midi_tempo))

    # write the chord progression
    for chord, duration in zip(chords, durations_seconds):
        tick_duration = get_midi_ticks_from_seconds(duration, bpm, ticks_per_beat)
        chord = make_midi_chord(chord, tick_duration)

        for msg in chord:
            track.append(msg)

    return mid
