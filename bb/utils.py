from functools import reduce


def compose(*fns):
    """
    Creates a composition of given functions

    >>> distinct = compose(list, set)
    >>>> distinct([0, 0, 1, 1, 2, 3])
    [0, 1, 2, 3]

    Todo: py3 supports star unpacking: `init, *rest = reversed(fns)`
    :param callable fns: Functions to compose
    :return callable: Returns of composition of given functions.
    """
    funcs = reversed(fns)
    init, rest = next(funcs), tuple(funcs)

    def inner(*args, **kwargs):
        return reduce(lambda a, b: b(a), rest, init(*args, **kwargs))
    return inner
