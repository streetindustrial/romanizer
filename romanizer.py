#!/usr/bin/env python
"""A very simple roman numbers iterable, similar to Python's `range`."""

__version__ = '1.0'
__author__ = 'V.R.'
__all__ = ['RomanRange']


class RomanRange:
    """Iterator for roman numbers (like default 'range')."""

    _table = (
        (1000, 'M'), (900, 'CM'), (500, 'D'), (400, 'CD'), (100, 'C'),
        (90, 'XC'), (50, 'L'), (40, 'XL'), (10, 'X'), (9, 'IX'), (5, 'V'),
        (4, 'IV'), (1, 'I')
    )              #: roman ref table

    _cache = None   #: stores some pre-cached nums (it's initialized below)

    __slots__ = '_range',

    def __init__(self, *args):
        self._range = range(*args)
        for arg in args[:2]:
            if arg < 0:
                raise ValueError('Negative roman numbers... Are you kidding?')

    def __iter__(self):
        for i in self._range:
            yield self._cache.get(i, self._next(i))

    def __repr__(self):
        return 'Roman %s' % str(self._range)

    @classmethod
    def _next(cls, i):
        if i == 0:
            return 'N'  #: nulla
        s = []
        for k, v in cls._table:
            n = i // k
            if n:
                s.append(v * n)
                i -= k * n
                if i == 0:
                    return ''.join(s)
        else:
            raise ValueError('Something terribly wrong happened.')


RomanRange._cache = {i: RomanRange._next(i)
                     for i in range(1, 128)}


if __name__ == '__main__':

    # run tests if the module is called directly
    # if module is called with arguments, then it will be run as CLI

    import sys
    import unittest

    class TestRomanRange(unittest.TestCase):
        """`RomanRange` class tester."""

        def test_that_it_works_like_normal_range(self):
            r = RomanRange(1, 20, 2)
            expected = ('I', 'III', 'V', 'VII', 'IX', 'XI', 'XIII', 'XV')
            for num, ex in zip(r, expected):
                self.assertEqual(num, ex)

        def test_for_zero(self):
            self.assertEqual(list(RomanRange(0, 2)), ['N', 'I'])

        def test_for_negative(self):
            with self.assertRaises(ValueError):
                RomanRange(-5, -10)

        def test_that_it_raises_errors_from_range(self):
            with self.assertRaises(TypeError):
                RomanRange(0.25)

    if sys.argv[1:]:
        _args = [int(arg) for arg in sys.argv[1:]]
        [print(r) for r in RomanRange(*_args)]
    else:
        unittest.main()
