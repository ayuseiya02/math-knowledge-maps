import sys

from MathMLToContTree import *

"""
G = nx.DiGraph()
G.add_node(0, data = r'$\u1D451$')
plotTree(G)
"""


test_filename = "tests/basic1.xml" # default test file
if len(sys.argv) > 1: # but will run diff test file if one is passed as argument
    test_filename = sys.argv[1]

"""
some of the latex alttext doesn't render in matplotlib
this function cleans up alttext so it renders
"""
def cleanUpLatex(s):
    s = s.replace("\n", " ")
    s = s.replace("%", " ")
    s = "$" + s + "$"
    return s

mathml_strings = toMathMLStrings(test_filename)
for i, e in enumerate(mathml_strings): # plot operator trees of all block equations in given test file
    print(e[0])
    root = toOpTree(e[0])
    G = graphTree(root)
    plotTree(G, cleanUpLatex(e[1]))

