from collections import OrderedDict
from functools import wraps


def simple_keymaker(params):
    """
    A simple cache key maker for python hashable objects.
    Doesn't support kwargs.

    For complex cases can be replaced with something like pickle. See tests.
    :return tuple:
    """
    args, kwargs = params
    assert not kwargs, 'This key maker doesn\'t support kwargs'
    return args


def lru_cache(max_size=100, keymaker=simple_keymaker):
    """
    Fixme: Better use `functools.lru_cache`.

    :param int max_size: The max size of items to store in cache.
    :param callable keymaker: A function to to create a key from arguments.
    :return callable: Returns decorated function.
    """

    assert isinstance(max_size, int), '`max_size` is not an integer'
    assert max_size > 0, '`max_size` should be greater than zero'

    def deco(func):
        @wraps(func)
        def inner(*args, **kwargs):
            key = keymaker((args, kwargs))
            if key in inner.cache:
                # todo: there is `move_to_end` in py3
                value = inner.cache.pop(key)
                inner.cache[key] = value
            else:
                value = inner.cache[key] = func(*args, **kwargs)

            if len(inner.cache) > max_size:
                # todo: there is no `iteritems` in py3
                oldest = next(inner.cache.iterkeys())
                del inner.cache[oldest]
            return value

        inner.cache = OrderedDict()
        return inner
    return deco
