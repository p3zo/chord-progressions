"""Creates plots for the output of chord extraction"""

import os

import matplotlib.pyplot as plt
import pandas as pd
from chord_progressions import logger
from progression_extraction import OUTPUT_LABEL_DIR, PLOT_DIR
from progression_extraction.label_arrangement import ALL_TEMPLATES

YSCALE = 1


def save_gantt(df):

    fig, gnt = plt.subplots()

    # TODO: add trackname to title
    gnt.set_title(arrangement_id)

    gnt.set_ylim(0, len(ALL_TEMPLATES) * YSCALE)
    gnt.set_xlim(0, df.end.max())

    gnt.grid(True)

    gnt.set_xlabel("Seconds")
    gnt.set_ylabel("Chord type")

    # TODO: truncate y axis to only chord types that appear
    # gnt.set_yticks([i for i in range(0, 192)])
    # gnt.set_yticklabels(["1", "2", "3"])

    def add_bar(x, g):
        ylab = x.type_id.unique()[0]

        xranges = []
        for row in x.iterrows():
            bar_len = row[1].end - row[1].start
            xranges.append((row[1].start, bar_len))

        yrange = (ylab - YSCALE, YSCALE)

        g.broken_barh(xranges=xranges, yrange=yrange)

    df.groupby("type_id").apply(lambda x: add_bar(x, gnt))

    plot_path = os.path.join(PLOT_DIR, f"gantt_{arrangement_id}.png")
    plt.savefig(plot_path)


if __name__ == "__main__":

    # filepath = os.path.join(OUTPUT_LABEL_DIR, "e6abf19ddfb14f3ebe1a529b2c6d0061.csv")
    # filepath = os.path.join(OUTPUT_LABEL_DIR, "f8d865f301804304b33c5341371e4ee8.csv")
    # filepath = os.path.join(OUTPUT_LABEL_DIR, "a87e365e4ee64108bcc5ba2aafcd57e0.csv")
    filepath = os.path.join(OUTPUT_LABEL_DIR, "test_2.csv")

    # TODO: assert plot dir exists

    arrangement_id = os.path.splitext(os.path.basename(filepath))[0]
    logger.info(arrangement_id)

    df = pd.read_csv(filepath, sep="\t", names=["start", "end", "type_id"])
    logger.info(f"{len(df.type_id.unique())} unique chord types")

    save_gantt(df)
