import numpy as np
from chord_progressions import logger
from chord_progressions.pitch import get_freq_from_note, get_n_overtones_harmonic
from scipy.io import wavfile

SAMPLE_RATE = 44100


def mk_sin(freq, duration, amp):
    s = [
        amp * np.sin(n * 2 * np.pi * freq / SAMPLE_RATE)
        for n in range(int(duration * SAMPLE_RATE))
    ]
    return np.array(s).reshape(-1, 1)


def mk_freq_buffer(freq, duration, n_overtones):
    freqs = get_n_overtones_harmonic(freq, n_overtones)

    # make each overtone progressively quieter
    sins = [mk_sin(f, duration, 1 / 2**i) for i, f in enumerate(freqs)]

    # TODO: normalize such that all notes have the same amplitude
    # regardless of the number of frequencies
    normed_sins = [s / len(sins) for s in sins]

    # combine the overtones to make a note
    return sum(normed_sins)


def mk_note_buffer(note, duration, n_overtones):

    freq = get_freq_from_note(note)

    return mk_freq_buffer(freq, duration, n_overtones)


def combine_buffers(buffers):
    stacked = np.hstack(buffers)

    normed = stacked / len(buffers)

    return np.sum(normed, axis=1).astype("float32")


def mk_chord_buffer(chord, duration, n_overtones):
    logger.info(f"Generating {duration} second buffer for chord: {chord}")

    note_buffers = [mk_note_buffer(note, duration, n_overtones) for note in chord]

    return combine_buffers(note_buffers)


def mk_arpeggiated_chord_buffer(chord, duration, seqs, n_overtones):

    logger.info(f"Generating {duration} second arpeggiated buffer for chord: {chord}")

    selected_seqs = [seqs[np.random.randint(len(seqs))] for i in range(len(chord))]

    bufs = []

    for note, seq in zip(chord, selected_seqs):
        logger.info(f"  {note} got rhythm {''.join(map(str, seq))}")

        pos_dur = duration / len(seq)

        seq_bufs = []

        for pos in seq:

            if pos == 1:
                seq_bufs.append(mk_note_buffer(note, pos_dur, n_overtones))

            else:
                seq_bufs.append(mk_sin(0, pos_dur, 0))

        bufs.append(np.concatenate(seq_bufs))

    # TODO: would these 0s be better placed somewhere in the middle of the bufs?
    max_buf_len = max([b.shape[0] for b in bufs])

    # TODO: can be simplified
    for ix, buf in enumerate(bufs):
        padding = np.zeros((max_buf_len - len(buf), 1))
        bufs[ix] = np.concatenate([buf, padding])

    return np.sum(bufs, axis=0)


def save_sample_chord_audio(chord, chord_type):
    buf = mk_chord_buffer(chord, duration=1, n_overtones=1)
    filename = chord_type.replace("/", "_").replace(" ", "")
    outpath = f"sample_chords/{filename}.wav"
    save_audio_buffer(buf, outpath)


def make_audio_progression(chords, durations, n_overtones):
    buffers = [
        mk_chord_buffer(c.notes, d, n_overtones) for c, d in zip(chords, durations)
    ]

    return np.concatenate(buffers)


def save_audio_buffer(buf, outpath):
    wavfile.write(outpath, SAMPLE_RATE, buf)
