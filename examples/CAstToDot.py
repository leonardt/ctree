"""
Illustrates the DOT-printing functionality by constructing
a small AST and printing its DOT representation.

Usage:
  $ python AstToDot.py > graph.dot

The resulting file can be viewed with a visualizer like Graphiz.
"""

from ctree.nodes.c import *

def main():
  stmt0 = Assign(SymbolRef('foo'), Constant(123.4))
  stmt1 = FunctionDecl(Float(), SymbolRef("bar"), [Int(), Long()], [String("baz")])
  tree = File([stmt0, stmt1])
  print (tree.visualize())

if __name__ == '__main__':
  main()
