import unittest
import ctypes

from ctree.c.nodes import *
from ctree.c.types import Int


class TestSymbols(unittest.TestCase):
    def _check(self, actual, expected):
        self.assertEqual(actual.codegen(), expected)

    def test_symbolref(self):
        ref = SymbolRef("foo")
        self._check(ref, "foo")

    def test_init_local(self):
        ref = SymbolRef("foo", _local=True)
        self._check(ref, "__local foo")

    def test_init_const(self):
        ref = SymbolRef("foo", _const=True)
        self._check(ref, "const foo")

    def test_set_local(self):
        ref = SymbolRef("foo")
        ref.set_local()
        self._check(ref, "__local foo")

    def test_set_const(self):
        ref = SymbolRef("foo")
        ref.set_const()
        self._check(ref, "const foo")

    def test_set_global(self):
        ref = SymbolRef("foo")
        ref.set_global()
        self._check(ref, "__global foo")

    def test_unique(self):
        ref1 = SymbolRef.unique("foo", Int())
        ref2 = SymbolRef.unique("foo", Int())
        self.assertNotEqual(ref1.codegen(), ref2.codegen())

    def test_copy(self):
        ref1 = SymbolRef("foo")
        ref2 = ref1.copy()
        self._check(ref1, ref2.codegen(()))

    def test_copy_without_declare(self):
        ref1 = SymbolRef("foo", Int())
        ref2 = ref1.copy()
        self._check(ref2, "foo")

    def test_copy_with_declare(self):
        ref1 = SymbolRef("foo", Int())
        ref2 = ref1.copy(declare=True)
        self._check(ref2, "int foo")


    def test_get_ctype(self):
        ref = SymbolRef("foo", Int())
        self.assertEqual(ref.get_ctype(), ctypes.c_int)
