# see http://cgm.cs.mcgill.ca/~godfried/publications/banff.pdf
EUCLIDEAN_TUPLES = [
    (1, 1),
    (2, 1),
    (3, 1),
    (3, 2),
    # (4, 1),
    (4, 3),
    (5, 2),
    (5, 3),
    (6, 5),
    # (7, 3),
    (7, 4),
    (7, 5),
    # (8, 3),
    (8, 5),
    (8, 7),
    # (9, 4),
    (9, 5),
    # (11, 4),
    # (11, 5),
    # (12, 4),
    # (12, 5),
    # (12, 7),
    # (16, 5),
    # (16, 7),
    # (16, 9),
    # (24, 11),
    # (24, 13),
]


def get_euclidean_sequence(n, k):
    """
    Constructs a binary sequence of `n` bits with `k` 1s, such that the 1s are as evenly distributed as possible.

    e.g. get_euclidean_sequence(13, 5) = '1001010010100'
         get_euclidean_sequence(8, 3)  = '10010010'

    See https://pdfs.semanticscholar.org/c652/d0a32895afc5d50b6527447824c31a553659.pdf for more details.
    """

    assert k >= 0 and isinstance(k, int), "k should be an integer >= 0"
    assert n >= k and isinstance(n, int), "n should be an integer >= k"

    pattern = []
    counts = []
    remainders = []
    divisor = n - k
    remainders.append(k)
    level = 0

    while True:

        counts.append(divisor // remainders[level])
        remainders.append(divisor % remainders[level])
        divisor = remainders[level]
        level = level + 1

        if remainders[level] <= 1:
            break

    counts.append(divisor)

    def build(level):

        if level == -1:
            pattern.append(0)

        elif level == -2:
            pattern.append(1)

        else:
            for i in range(0, counts[level]):
                build(level - 1)

            if remainders[level] != 0:
                build(level - 2)

    build(level)

    i = pattern.index(1)
    pattern = pattern[i:] + pattern[0:i]

    return pattern
