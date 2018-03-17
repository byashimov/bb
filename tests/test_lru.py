import pickle
from itertools import starmap

import mock
from unittest2 import TestCase

from bb.lru import lru_cache


class LruTestCase(TestCase):
    def test_lru_cache(self):
        mock_call = mock.Mock()

        @lru_cache(max_size=4)
        def foo(char):
            mock_call(char)
            return char.upper()

        cases = (
            ('a', 'A', ['A']),
            ('b', 'B', ['A', 'B']),
            ('c', 'C', ['A', 'B', 'C']),
            ('d', 'D', ['A', 'B', 'C', 'D']),
            ('e', 'E', ['B', 'C', 'D', 'E']),
            ('d', 'D', ['B', 'C', 'E', 'D']),
            ('f', 'F', ['C', 'E', 'D', 'F']),
        )

        for arg, result, cache in cases:
            with self.subTest(arg=arg, result=result, cache=cache):
                self.assertEqual(foo(arg), result)
                self.assertEqual(foo.cache.values(), cache)

        # Proves no extra calls
        calls = map(mock.call, ('a', 'b', 'c', 'd', 'e', 'f'))
        mock_call.assert_has_calls(calls, any_order=False)

    def test_args(self):
        mock_call = mock.Mock()

        @lru_cache(max_size=4)
        def foo(*chars):
            mock_call(*chars)
            return '-'.join(chars).upper()

        cases = (
            (('a', 'b'), 'A-B', ['A-B']),
            (('c', 'd'), 'C-D', ['A-B', 'C-D']),
            (('a', 'b'), 'A-B', ['C-D', 'A-B']),
        )

        for args, result, cache in cases:
            with self.subTest(args=args, result=result, cache=cache):
                self.assertEqual(foo(*args), result)
                self.assertEqual(foo.cache.values(), cache)

        # Proves no extra calls
        calls = starmap(mock.call, (('a', 'b'), ('c', 'd')))
        mock_call.assert_has_calls(calls, any_order=False)

    def test_kwargs_fails(self):
        @lru_cache()
        def foo(*args, **kwargs):
            pass

        with self.assertRaises(AssertionError) as e:
            foo(bar=1)

        self.assertEqual(
            'This key maker doesn\'t support kwargs',
            e.exception.message
        )

    def test_max_size_bad_values(self):
        cases = (
            (.1, '`max_size` is not an integer'),
            (None, '`max_size` is not an integer'),
            ('100', '`max_size` is not an integer'),
            (0, '`max_size` should be greater than zero'),
            (-1, '`max_size` should be greater than zero'),
        )

        for max_size, msg in cases:
            with self.subTest(max_size=max_size, msg=msg):
                with self.assertRaises(AssertionError) as e:
                    lru_cache(max_size)
                self.assertEqual(msg, e.exception.message)

    def test_custom_key_maker_with_kwargs(self):
        mock_call = mock.Mock()

        @lru_cache(keymaker=pickle.dumps)
        def foo(bar, baz=None):
            mock_call(bar, baz=baz)
            return '{}:{}'.format(bar, baz)

        for call in range(2):
            with self.subTest(call=call):
                self.assertEqual(foo(0, baz=1), '0:1')

        mock_call.assert_called_once_with(0, baz=1)
