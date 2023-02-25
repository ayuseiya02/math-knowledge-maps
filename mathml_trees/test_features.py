import sys

from MathMLToOpTree import *   
from StandardizeOpTree import *
from ExtractFeatures import *

trees = getTreesFromFile("tests/sample/quant-ph0001009.html")

for tree in trees:
    s_tree = standardizeOpTree(tree)

    f = extractFeatures(s_tree)
    printFeatures(f)

    plotTree(s_tree)