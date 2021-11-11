import datetime as dt
import numpy as np

from chord_progressions import WORDS_FILEPATH


def round_to_base(x, base):
    """Rounds a number `x` to the closest `base`"""
    return base * round(x / base)


def shift_arr_by_one(arr):
    """
    Shifts an array to the right by 1 element
    e.g. shift_arr([1, 2, 3]) -> [3, 1, 2]
    """
    return arr[-1:] + arr[:-1]


def is_circular_match(list_1, list_2):
    """Does any rotation of the elements in `list_1` match `list_2`?"""

    str_1 = " ".join(map(str, list_1))
    str_2 = " ".join(map(str, list_2))

    if len(str_1) != len(str_2):
        return False

    str_2_expanded = str_2 + " " + str_2
    return str_1 in str_2_expanded


# def is_partial_circular_match(list_1, list_2):
#     """Is any rotation of the elements in `list_1` contained within `list_2`?"""

#     # LEFT OFF:
#     # is ["F1", "A#0", "F#0"] a subset of an Indian-Japan Pentatonic?
#     # how about ["F0", "F#0", "A#0", "C#1"] and ["", "", "", "C#1"]

#     # may be able to adadpt the `slots` logic from `select_voicing()` here

#     one_indices_1 = [ix for ix, i in enumerate(list_1) if i == 1]
#     one_indices_2 = [ix for ix, i in enumerate(list_2) if i == 1]

#     # enforce that a note in each slot gets selected
#     choices = {}

#     while len(choices) < sum(rotation):

#         choice = np.random.choice(one_indices)

#         slot = choice % 12

#         if slot not in choices:
#             choices[slot] = choice


def get_random_word():

    with open(WORDS_FILEPATH) as words_file:
        words = words_file.read().split()

    return words[np.random.randint(len(words))]


def get_run_id(name=None):

    today = dt.datetime.today()
    hour = today.hour * 60 * 60
    minute = today.minute * 60
    second = today.second
    datetime_id = today.strftime("%y%j") + str(hour + minute + second)

    word_id = get_random_word()

    if name:
        return f"{name}_{word_id}_{datetime_id}"

    return f"{word_id}_{datetime_id}"
