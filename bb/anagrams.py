from utils import compose


def find_anagrams_lazy(chars, choices, distinct=True):
    """
    Finds anagrams of given chars in given choices.
    This version doesn't support mixed types.

    :param basestring chars: A chars to look for
    :param choices: Sequence of anagrams
    :param bool distinct: Set True to skip duplicates
    :return: Returns a generator
    """
    lower = chars.lower()
    chars = sorted(lower)
    seen = {lower}
    for option in choices:
        opt_lower = option.lower()
        is_anagram = (
            opt_lower not in seen and  # skips duplicates and self
            sorted(opt_lower) == chars  # perfect match
        )

        if is_anagram:
            yield option
            if distinct:
                seen.add(opt_lower)


find_anagrams = compose(list, find_anagrams_lazy)
