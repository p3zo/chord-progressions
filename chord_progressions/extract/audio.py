"""
Implementation details:

For each frame:
    1. Obtain spectrogram with STFT
    2. Detect spectral peaks
    3. Estimate HPCP [Gómez 2006]

Join frames together into segments corresponding to each beat of the track.

For each segment:
    4. Avg and normalize HPCPs
    5. Match avg'd HPCPs to Chordico's tone profiles
"""

import os

import essentia
import essentia.standard as es
import essentia.streaming as ess
import matplotlib.pyplot as plt
import numpy as np
from chord_progressions import logger
from chord_progressions.chord import Chord
from chord_progressions.progression import Progression
from pylab import imshow

SAMPLE_RATE = 44100  # Hz
FRAME_SIZE = 4096  # samples
HPCP_THRESH = 0.35

PC_MIDI_NUMS = list(range(69, 81))


def get_essentia_features(filepath):
    # TODO: preprocess audio to eliminate regions where harmonic structure is noisy
    #   e.g. source-separate guitar from the rest of the mix?

    # Initialize the essentia streaming algorithms
    loader = ess.MonoLoader(filename=filepath)

    framecutter = ess.FrameCutter(
        frameSize=FRAME_SIZE, hopSize=int(FRAME_SIZE / 2), silentFrames="noise"
    )

    windowing = ess.Windowing(type="blackmanharris62")

    spectrum = ess.Spectrum()

    spectralpeaks = ess.SpectralPeaks(
        orderBy="magnitude",
        magnitudeThreshold=0.00001,
        minFrequency=20,
        maxFrequency=3500,
        maxPeaks=60,
    )

    hpcp_extractor = ess.HPCP(
        size=12,  # the size of the output HPCP (must be a positive nonzero multiple of 12)
        referenceFrequency=440,  # the reference frequency for semitone index calculation, corresponding to A3 [Hz]
        minFrequency=20,  # the min freq that contributes to the HPCP [Hz]
        maxFrequency=3500,  # the max freq that contributes to the HPCP [Hz]
        weightType="cosine",  # type of weighting function for determining frequency contribution
        nonLinear=False,  # apply non-linear mapping to the output (boost values close to 1, decrease values close to 0)
        windowSize=1.0,  # the size, in semitones, of the window used for the weighting
        bandPreset=False,  # don't use a band preset
    )

    # Use a pool to store data
    pool = essentia.Pool()

    # Connect streaming algorithms
    loader.audio >> framecutter.signal
    loader.audio >> (pool, "audio")

    framecutter.frame >> windowing.frame >> spectrum.frame
    spectrum.spectrum >> spectralpeaks.spectrum
    spectralpeaks.magnitudes >> hpcp_extractor.magnitudes
    spectralpeaks.frequencies >> hpcp_extractor.frequencies

    # TODO: use a representation w voicings rather than just HPCPs (use pitches, not just pitch classes)
    hpcp_extractor.hpcp >> (pool, "hpcp")

    # TODO: compute [HighResolutionFeatures](https://essentia.upf.edu/reference/std_HighResolutionFeatures.html)
    # TODO: compute hpcp crest & entropy (https://essentia.upf.edu/tutorial_extractors_musicextractor.html)
    # TODO: get all sorts of other features w MusicExtractor (https://essentia.upf.edu/streaming_extractor_music.html)

    # Run the streaming network
    essentia.run(loader)

    feats = {i: pool[i] for i in pool.descriptorNames() if i != "audio"}

    return pool["audio"], feats


def plot_hpcp(hpcp, figpath):
    plt.rcParams["figure.figsize"] = (15, 6)
    imshow(hpcp.T, aspect="auto", origin="lower", interpolation="none")
    plt.yticks(
        ticks=range(12),
        labels=["A", "A#", "B", "C", "C#", "D", "D#", "E", "F", "F#", "G", "G#"],
    )
    plt.title("HPCPs in frames")
    plt.savefig(figpath)
    plt.clf()
    print(f"Saved HPCP plot to {figpath}")


def get_beats(x, marked_audio_path=None):
    # Compute beat positions and BPM
    rhythm_extractor = es.RhythmExtractor2013(method="multifeature")
    bpm, beats, beats_confidence, _, beats_intervals = rhythm_extractor(x)
    print(f"  BPM: {bpm}")

    if marked_audio_path:
        # Mark beat positions in the audio and write it to a file
        marker = es.AudioOnsetsMarker(onsets=beats, type="noise")
        marked_audio = marker(x)
        es.MonoWriter(filename=marked_audio_path)(marked_audio)

    return beats, bpm


def get_meter(signal, beats):
    """Estimate the time signature of a signal by finding the highest correlation between salient beat loudness bands"""
    loudness, loudness_band_ratio = es.BeatsLoudness(
        beats=beats,  # list of beat positions (in seconds)
        beatWindowDuration=0.1,  # seconds, dur of window in which to look for beat start (centered on beat positions)
        beatDuration=0.05,  # duration of window in which the beat will be restricted [s]
        frequencyBands=[
            20,
            150,
            400,
            3200,
            7000,
            22000,
        ],  # the list of bands to compute energy ratios, hz
        sampleRate=SAMPLE_RATE,
    )(signal)

    beatogram = es.Beatogram(size=16)(  # size: number of beats for dynamic filtering
        loudness, loudness_band_ratio
    )

    return es.Meter()(beatogram)


def extract_progression_from_audio(filepath, plot_dir=None, marked_audio_dir=None):
    """
    Params
        filepath: str, Path to an audio file
        plot_dir: str, if passed, writes intermediate plots. Useful for debugging.
        marked_audio_dir: str, writes an audio file with beat position markers. Useful for debugging.

    Returns
        progression: Progression, the extracted progression object
    """

    basename = os.path.basename(filepath)
    trackid = os.path.splitext(basename)[0]

    x, feats = get_essentia_features(filepath)

    hpcp = feats["hpcp"]
    logger.info(f"  HPCP shape: {hpcp.shape}")

    hpcp_figpath = os.path.join(plot_dir, f"{trackid}_hpcp.png")
    plot_hpcp(hpcp, hpcp_figpath)

    marked_audio_path = os.path.join(marked_audio_dir, f"{trackid}_beats.mp3")
    beats, bpm = get_beats(x, marked_audio_path)

    meter = get_meter(x, beats)
    print(f"  Estimated meter: {meter}")

    segment_start_times = beats[:: int(meter)]
    frames_per_second = SAMPLE_RATE / FRAME_SIZE
    quarter_note_beat_samples = [
        int(i * frames_per_second) for i in segment_start_times
    ]
    beat_samples = list(
        zip(quarter_note_beat_samples[:-1], quarter_note_beat_samples[1:])
    )
    beat_durations_samples = [b[1] - b[0] for b in beat_samples]
    beat_durations = [i / frames_per_second for i in beat_durations_samples]

    segment_pcs = []

    for fstart, fend in beat_samples:
        frame = hpcp[fstart:fend]
        mean = frame.mean(axis=0)
        normalized_mean = mean / mean.max() if mean.max() > 0 else mean
        pcs = np.where(normalized_mean > HPCP_THRESH)[0].tolist()
        segment_pcs.append(pcs)

    chords = [Chord([PC_MIDI_NUMS[pc] for pc in seg]) for seg in segment_pcs]
    # TODO: convert beat_durations to Tone Time values relative to bpm and add them to Progression
    progression = Progression(chords, beat_durations, bpm=bpm, name=filepath)

    return progression
