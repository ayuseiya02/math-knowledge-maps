import sys

from MathMLToContTree import *
from expressionFinder import *

"""
G = nx.DiGraph()
G.add_node(0, data = r'$\u1D451$')
plotTree(G)
"""


test_filename = "tests/basic1.xml"
if len(sys.argv) > 1:
    test_filename = sys.argv[1]

def cleanUpLatex(s):
    s = s.replace("\n", " ")
    s = s.replace("%", " ")
    s = "$" + s + "$"
    return s

mathml_strings = toMathMLStrings(test_filename)
for i, e in enumerate(mathml_strings):
    print(e[1])
    root = toOpTree(e[0])
    G = graphTree(root)
    plotTree(G, cleanUpLatex(e[1]))

