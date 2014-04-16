import unittest

from ctree.c.nodes import *
from ctree.c.types import *
from ctree.transformations import PyBasicConversions
from ctree.frontend import get_ast

class TestUnroll(unittest.TestCase):
    def _check(self, actual, expected):
        self.assertEqual(str(actual), str(expected))

    def test_simple_unroll(self):
        actual = For(Assign(SymbolRef('x', Int()), Constant(0)),
                     Lt(SymbolRef('x'), Constant(9)),
                     PostInc(SymbolRef('x')),
                     [AddAssign(SymbolRef('z', Int()), Mul(Constant(2), SymbolRef('x')))]
                     )
        expected = For(Assign(SymbolRef('x', Int()), Constant(0)),
                       Lt(SymbolRef('x'), Constant(9)),
                       AddAssign(SymbolRef('x'), 2),
                       [
                           AddAssign(SymbolRef('z', Int()), Mul(Constant(2), SymbolRef('x'))),
                           PostInc(SymbolRef('x')),
                           AddAssign(SymbolRef('z'), Mul(Constant(2), SymbolRef('x')))
                       ])
        actual.unroll(2)
        self._check(actual, expected)

    def test_leftover_unroll(self):
        actual = For(Assign(SymbolRef('y', Int()), Constant(0)),
                     Lt(SymbolRef('y'), Constant(10)),
                     PostInc(SymbolRef('y')),
                     [
                         For(Assign(SymbolRef('x', Int()), Constant(0)),
                             Lt(SymbolRef('x'), Constant(10)),
                             PostInc(SymbolRef('x')),
                             [AddAssign(SymbolRef('z', Int()), Mul(Constant(2), SymbolRef('x')))]
                             )
                     ])
        expected = For(Assign(SymbolRef('y', Int()), Constant(0)),
                       Lt(SymbolRef('y'), Constant(10)),
                       PostInc(SymbolRef('y')),
                       [
                           For(Assign(SymbolRef('x', Int()), Constant(0)),
                               Lt(SymbolRef('x'), Constant(9)),
                               AddAssign(SymbolRef('x'), 2),
                               [
                                   AddAssign(SymbolRef('z', Int()), Mul(Constant(2), SymbolRef('x'))),
                                   PostInc(SymbolRef('x')),
                                   AddAssign(SymbolRef('z'), Mul(Constant(2), SymbolRef('x')))
                               ]),
                           For(Assign(SymbolRef('x', Int()), Constant(9)),
                               Lt(SymbolRef('x'), Constant(10)),
                               PostInc(SymbolRef('x')),
                               [AddAssign(SymbolRef('z', Int()), Mul(Constant(2), SymbolRef('x')))]
                               )
                       ])
        actual.body[0].unroll(2)
        self._check(actual, expected)


    def test_LtE_handler(self):
        actual = For(Assign(SymbolRef('x', Int()), Constant(0)),
                     LtE(SymbolRef('x'), Constant(15)),
                     PostInc(SymbolRef('x')),
                     [AddAssign(SymbolRef('z', Int()), Mul(Constant(2), SymbolRef('x')))]
                     )
        expected = For(Assign(SymbolRef('x', Int()), Constant(0)),
                       Lt(SymbolRef('x'), Constant(16)),
                       AddAssign(SymbolRef('x'), 4),
                       [
                           AddAssign(SymbolRef('z', Int()), Mul(Constant(2), SymbolRef('x'))),
                           PostInc(SymbolRef('x')),
                           AddAssign(SymbolRef('z'), Mul(Constant(2), SymbolRef('x'))),
                           PostInc(SymbolRef('x')),
                           AddAssign(SymbolRef('z'), Mul(Constant(2), SymbolRef('x'))),
                           PostInc(SymbolRef('x')),
                           AddAssign(SymbolRef('z'), Mul(Constant(2), SymbolRef('x')))
                       ])
        actual.unroll(4)
        self._check(actual, expected)

    def test_leftover_LtE(self):
        actual = For(Assign(SymbolRef('y', Int()), Constant(0)),
                     Lt(SymbolRef('y'), Constant(10)),
                     PostInc(SymbolRef('y')),
                     [
                         For(Assign(SymbolRef('x', Int()), Constant(0)),
                             LtE(SymbolRef('x'), Constant(10)),
                             PostInc(SymbolRef('x')),
                             [AddAssign(SymbolRef('z', Int()), Mul(Constant(2), SymbolRef('x')))]
                             )
                     ])
        expected = For(Assign(SymbolRef('y', Int()), Constant(0)),
                       Lt(SymbolRef('y'), Constant(10)),
                       PostInc(SymbolRef('y')),
                       [
                           For(Assign(SymbolRef('x', Int()), Constant(0)),
                               Lt(SymbolRef('x'), Constant(9)),
                               AddAssign(SymbolRef('x'), 3),
                               [
                                   AddAssign(SymbolRef('z', Int()), Mul(Constant(2), SymbolRef('x'))),
                                   PostInc(SymbolRef('x')),
                                   AddAssign(SymbolRef('z'), Mul(Constant(2), SymbolRef('x'))),
                                   PostInc(SymbolRef('x')),
                                   AddAssign(SymbolRef('z'), Mul(Constant(2), SymbolRef('x')))
                               ]),
                           For(Assign(SymbolRef('x', Int()), Constant(9)),
                               LtE(SymbolRef('x'), Constant(10)),
                               PostInc(SymbolRef('x')),
                               [AddAssign(SymbolRef('z', Int()), Mul(Constant(2), SymbolRef('x')))]
                               )
                       ])
        actual.body[0].unroll(3)
        self._check(actual, expected)
