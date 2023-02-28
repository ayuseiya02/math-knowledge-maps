import sys

from MathMLToOpTree import *   
from StandardizeOpTree import *
from ExtractFeatures import *

trees = getTreesFromFile("tests/sample/quant-ph0001009.html")
#trees = getTreesFromFile("tests/custom/basic3.xml")

for tree in trees:
    plotTree(tree)

    s_tree = standardizeOpTree(tree)
    plotTree(s_tree)

    f = extractFeatures(s_tree)
    printFeatures(f)

    plotTree(s_tree)