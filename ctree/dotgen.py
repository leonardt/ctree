import ast
try:
  from pydot import *
except ImportError:
  print("pydot not available.")

from ctree.visitors import NodeVisitor

class DotGenerator(NodeVisitor):
  """
  Generates a representation of the AST in the DOT graph language.
  See http://en.wikipedia.org/wiki/DOT_(graph_description_language)

  We can use pydot to do this, instead of using plain string concatenation.
  """

  def __init__(self):
    super()
    self.graph = Dot(graph_type='digraph')

  def generate_from(self, node):
    self.visit(node)
    self.graph.write_png('example2_graph.png')

  def label_SymbolRef(self, node):
    return "name: %s" % node.name

  def label_Constant(self, node):
    return "value: %s" % node.value

  def label_String(self, node):
    return "value: %s" % node.value

  def label(self, node):
    """
    A string to provide useful information for visualization, debugging, etc.
    This routine will attempt to call a label_XXX routine for class XXX, if
    such a routine exists (much like the visit_XXX routines).
    """
    s = r"%s\n" % type(node).__name__
    labeller = getattr(self, "label_" + type(node).__name__, None)
    if labeller:
      s += labeller(node)
    return s

  def generic_visit(self, node):
    # label this node
    graph_node = Node(self.label(node))
    self.graph.add_node(graph_node)

    # s = 'n%s [label="%s"];\n' % (id(node), self.label(node))

    # edge to parent
    # if hasattr(node, 'parent') and node.parent != None:
      #s += 'n%s -> n%s [label="parent",style=dotted];\n' % (id(node), id(node.parent))

    # edges to children
    # s += 'n%s [label="%s"];\n' % (id(node), self.label(node))
    for fieldname, child in ast.iter_fields(node):
      if type(child) is list:
        for i, grandchild in enumerate(child):
          # s += 'n%d -> n%d [label="%s[%d]"];\n' % \
          #      (id(node), id(grandchild), fieldname, i)
          # s += self.visit(grandchild)
          grandchild = self.visit(grandchild)
          self.graph.add_edge(Edge(graph_node, grandchild, label="%s[%d]" % (fieldname, i)))
          self.graph.add_edge(Edge(grandchild, graph_node, label="parent", style="dotted"))
      elif isinstance(child, ast.AST):
        # s += 'n%d -> n%d [label="%s"];\n' % (id(node), id(child), fieldname)
        # s += self.visit(child)
        child = self.visit(child)
        self.graph.add_edge(Edge(graph_node, child, label=fieldname))
        self.graph.add_edge(Edge(child, graph_node, label="parent", style="dotted"))
    return graph_node

def to_dot(node):
  assert isinstance(node, ast.AST), \
    "to_dot expected an instance of ast.AST, got %s." % type(node).__name__
  return DotGenerator().generate_from(node)
