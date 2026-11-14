# Loaded on first use, so that importing the package does not load pandas and networkx
# (about 60 MB) for code that never extracts progressions.
def __getattr__(name):
    if name == "extract_progression_from_midi":
        from chord_progressions.extract.midi_harman import extract_progression_from_midi

        return extract_progression_from_midi
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
