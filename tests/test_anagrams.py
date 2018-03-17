# coding: utf-8

from __future__ import unicode_literals

from unittest2 import TestCase

from bb.anagrams import find_anagrams


class FindAnagramsTestCase(TestCase):
    def test_bytes(self):
        chars = b'foo'
        choices = (b'foo', b'bar', b'ofo', b'baz', b'oof')
        expected = [b'ofo', b'oof']
        self.assertEqual(find_anagrams(chars, choices), expected)

    def test_unicode(self):
        chars = 'фуу'
        choices = ('фуу', 'бар', 'уфу', 'баз', 'ууф')
        expected = ['уфу', 'ууф']
        self.assertEqual(find_anagrams(chars, choices), expected)

    def test_case_sensivity(self):
        chars = 'Foo'
        choices = ('foo', 'bar', 'ofO')
        expected = ['ofO']
        self.assertEqual(find_anagrams(chars, choices), expected)

    def test_distinct(self):
        chars = 'Foo'
        choices = ('foo', 'bar', 'ofO', 'ofo', 'Ofo')
        cases = (
            (True, ['ofO']),
            (False, ['ofO', 'ofo', 'Ofo'])
        )

        for distinct, expected in cases:
            with self.subTest(distinct=distinct, expected=expected):
                result = find_anagrams(chars, choices, distinct)
                self.assertEqual(result, expected)
