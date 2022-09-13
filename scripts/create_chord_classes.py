"""
    Ad-hoc script to analyze chords on dimensions such as `evenness` and `cardinality`.

    The goal is to cluster chords into 3 - 7 "chord classes" that will serve Chordico's
    MTG-like chord card world.
"""

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

# from chord_progressions.audio import save_sample_chord_audio
from chord_progressions.chord import get_template_from_template_str
from chord_progressions.db import load_type_templates
from chord_progressions.evaluate import evaluate_notes
from chord_progressions.solver import select_voicing

sns.set(style="whitegrid")


def plot_chords_by_evenness(chords):
    by_evenness = sorted(chords, key=lambda k: k["metrics"]["evenness"])

    x = range(len(chords))
    evennesses = [c["metrics"]["evenness"] for c in by_evenness]
    tick_label = [c["chord_type"] for c in by_evenness]

    plt.figure(figsize=(20, 25))
    plt.barh(x, width=evennesses, tick_label=tick_label)
    plt.savefig("evennesses.png", dpi=300)

    plt.clf()


if __name__ == "__main__":

    note_range_low = 60
    note_range_high = 72

    chords = []

    type_templates = load_type_templates()

    for i in range(50):
        print(i)
        for chord_type, template_str in type_templates.items():

            template = get_template_from_template_str(template_str)

            voicing = select_voicing(template, note_range_low, note_range_high)

            metrics = evaluate_notes(voicing)

            chords.append(
                {
                    "chord_type": chord_type,
                    "voicing": voicing,
                    "cardinality": len(voicing),
                    "evenness": metrics["evenness"],
                    "relative_evenness": metrics["relative_evenness"],
                    "interval_class_vector": metrics["interval_class_vector"],
                }
            )

    df = pd.DataFrame(chords)
    df.sort_values(by="evenness", inplace=True)

    min_evenness_by_cardinality = df.groupby("cardinality").evenness.min()
    max_evenness_by_cardinality = df.groupby("cardinality").evenness.max()

    df["relative_evenness"] = 1 - (
        (df.evenness - df.evenness.min()) / (df.evenness.max() - df.evenness.min())
    )

    ax = sns.boxplot(x="cardinality", y="relative_evenness", data=df)
    plt.savefig("evenness_by_cardinality.png")
    plt.clf()

    # df.apply(lambda x: save_sample_chord_audio(x.voicing, x.chord_type), axis=1)
