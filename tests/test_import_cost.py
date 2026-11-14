import subprocess
import sys

HEAVY = ["matplotlib", "music21", "networkx", "pandas", "scipy"]


def loaded_after(statement):
    """The heavy libraries a fresh interpreter has loaded after running statement."""
    check = (
        f"import sys; {statement}; print(*[m for m in {HEAVY!r} if m in sys.modules])"
    )
    return subprocess.run(
        [sys.executable, "-c", check], capture_output=True, text=True, check=True
    ).stdout.split()


def test_core_modules_do_not_load_libraries_they_only_need_for_files_and_keys():
    core = (
        "import chord_progressions; from chord_progressions import progression_measures"
    )
    assert loaded_after(core) == []


def test_lazy_names_still_load_on_use():
    assert "pandas" in loaded_after(
        "from chord_progressions import extract_progression_from_midi"
    )
    assert "pandas" in loaded_after("from chord_progressions import *")
    assert "music21" in loaded_after(
        "from chord_progressions import Progression; Progression([[60, 64, 67]]).key"
    )
