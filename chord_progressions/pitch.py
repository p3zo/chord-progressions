A4 = 440


NOTE_NAMES = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]

MIDI_NOTES = [
    "C-1",
    "C#-1",
    "D-1",
    "D#-1",
    "E-1",
    "F-1",
    "F#-1",
    "G-1",
    "G#-1",
    "A-1",
    "A#-1",
    "B-1",
    "C0",
    "C#0",
    "D0",
    "D#0",
    "E0",
    "F0",
    "F#0",
    "G0",
    "G#0",
    # start piano range
    "A0",
    "A#0",
    "B0",
    "C1",
    "C#1",
    "D1",
    "D#1",
    "E1",
    "F1",
    "F#1",
    "G1",
    "G#1",
    "A1",
    "A#1",
    "B1",
    "C2",
    "C#2",
    "D2",
    "D#2",
    "E2",
    "F2",
    "F#2",
    "G2",
    "G#2",
    "A2",
    "A#2",
    "B2",
    "C3",
    "C#3",
    "D3",
    "D#3",
    "E3",
    "F3",
    "F#3",
    "G3",
    "G#3",
    "A3",
    "A#3",
    "B3",
    "C4",
    "C#4",
    "D4",
    "D#4",
    "E4",
    "F4",
    "F#4",
    "G4",
    "G#4",
    "A4",
    "A#4",
    "B4",
    "C5",
    "C#5",
    "D5",
    "D#5",
    "E5",
    "F5",
    "F#5",
    "G5",
    "G#5",
    "A5",
    "A#5",
    "B5",
    "C6",
    "C#6",
    "D6",
    "D#6",
    "E6",
    "F6",
    "F#6",
    "G6",
    "G#6",
    "A6",
    "A#6",
    "B6",
    "C7",
    "C#7",
    "D7",
    "D#7",
    "E7",
    "F7",
    "F#7",
    "G7",
    "G#7",
    "A7",
    "A#7",
    "B7",
    "C8",
    # end piano range
    "C#8",
    "D8",
    "D#8",
    "E8",
    "F8",
    "F#8",
    "G8",
    "G#8",
    "A8",
    "A#8",
    "B8",
    "C9",
    "C#9",
    "D9",
    "D#9",
    "E9",
    "F9",
    "F#9",
    "G9",
]

MIDI_NOTE_FREQUENCIES = [
    8.18,
    8.66,
    9.18,
    9.72,
    10.3,
    10.91,
    11.56,
    12.25,
    12.98,
    13.75,
    14.57,
    15.43,
    16.35,
    17.32,
    18.35,
    19.45,
    20.6,
    21.83,
    23.12,
    24.5,
    25.96,
    # start piano range
    27.5,
    29.14,
    30.87,
    32.7,
    34.65,
    36.71,
    38.89,
    41.2,
    43.65,
    46.25,
    49.0,
    51.91,
    55.0,
    58.27,
    61.74,
    65.41,
    69.3,
    73.42,
    77.78,
    82.41,
    87.31,
    92.5,
    98.0,
    103.83,
    110.0,
    116.54,
    123.47,
    130.81,
    138.59,
    146.83,
    155.56,
    164.81,
    174.61,
    185.0,
    196.0,
    207.65,
    220.0,
    233.08,
    246.94,
    261.63,
    277.18,
    293.66,
    311.13,
    329.63,
    349.23,
    369.99,
    392.0,
    415.3,
    440.0,
    466.16,
    493.88,
    523.25,
    554.37,
    587.33,
    622.25,
    659.26,
    698.46,
    739.99,
    783.99,
    830.61,
    880.0,
    932.33,
    987.77,
    1046.5,
    1108.73,
    1174.66,
    1244.51,
    1318.51,
    1396.91,
    1479.98,
    1567.98,
    1661.22,
    1760.0,
    1864.66,
    1975.53,
    2093.0,
    2217.46,
    2349.32,
    2489.02,
    2637.02,
    2793.83,
    2959.96,
    3135.96,
    3322.44,
    3520.0,
    3729.31,
    3951.07,
    4186.01,
    # end piano range
    4434.92,
    4698.64,
    4978.03,
    5274.04,
    5587.65,
    5919.91,
    6271.93,
    6644.88,
    7040.0,
    7458.62,
    7902.13,
    8372.02,
    8869.84,
    9397.27,
    9956.06,
    10548.08,
    11175.3,
    11839.82,
    12543.85,
]


def get_note_from_midi_num(note_num):
    try:
        return MIDI_NOTES[int(note_num)]
    except IndexError:
        raise IndexError(f"Invalid midi note number: {note_num}")


def get_midi_num_from_note(note):
    try:
        return MIDI_NOTES.index(note)
    except ValueError:
        raise ValueError(f"Invalid note name: {note}")


def get_pitch_class_from_note(note):
    """Returns the pitch class of a note, e.g. get_pitch_class_from_note(C4) -> 0"""
    midi_num = get_midi_num_from_note(note)
    return get_pitch_class_from_midi_num(midi_num)


def get_pitch_class_from_midi_num(note_num):
    """Returns the pitch class of a midi num, e.g. 48"""
    return note_num % 12


def get_note_name_from_note(note):
    """Drops the octave part of the note, e.g. A#4 -> A#"""

    midi_num = get_midi_num_from_note(note) % 12
    pitch_class = get_pitch_class_from_midi_num(midi_num)

    return NOTE_NAMES[pitch_class]


def get_notes_from_midi_nums_str(midi_nums_str):
    """e.g. "60-48" -> ["C4", "C3"]"""
    return [get_note_from_midi_num(s) for s in midi_nums_str.split("-")]


def get_notes_list_from_midi_nums_str(midi_nums_str):
    """e.g. "60-48_62-50" -> [["C4", "C3"], ["D4", "E3"]]"""
    return [get_notes_from_midi_nums_str(s) for s in midi_nums_str.split("_")]


def get_midi_nums_list_from_midi_nums_str(midi_nums_str):
    """e.g. "60-48_62-50" -> [[60, 48], [62, 50]]
    If any chord in `midi_nums_str` is invalid, returns an empty string for that chord"""
    midi_nums_list = []
    for m in midi_nums_str.split("_"):
        try:
            midi_nums_list.append([int(i) for i in m.split("-")])
        except:
            pass

    return midi_nums_list


def get_octave_from_note(note):

    note_name = get_note_name_from_note(note)

    octave = note.split(note_name)[1]

    return int(octave)


def get_freq_from_midi_num(n):
    return round(A4 * 2 ** ((n - 69) / 12), 2)


def increment_note(note):
    """Returns the note a half step above `note`"""

    note_name = get_note_name_from_note(note)

    new_name_ix = NOTE_NAMES.index(note_name) + 1 % 12
    new_note_name = NOTE_NAMES[new_name_ix % 12]

    octave = get_octave_from_note(note)

    if new_name_ix == 12:
        octave += 1

    return new_note_name + str(octave)


def create_notes_freqs_table():
    """This is a one-off function that was used to create the MIDI_NOTE_FREQUENCIES constant"""

    from collections import OrderedDict  # # noqa

    notes = OrderedDict()

    current_note = "C-1"

    for i in range(128):
        notes[current_note] = get_freq_from_midi_num(i)
        current_note = increment_note(current_note)

    return notes


def get_note_list(note_range_low=0, note_range_high=127):

    start_ix = note_range_low
    end_ix = note_range_high

    return MIDI_NOTES[start_ix : end_ix + 1]


def get_freq_from_note(note):
    """Returns the frequency of a note, e.g. `A4`"""

    ix = get_midi_num_from_note(note)

    return MIDI_NOTE_FREQUENCIES[ix]


def get_n_overtones_harmonic(freq, n):
    """Compute a list of n overtones above a given freq"""
    return [i * freq for i in range(1, n + 2)]
