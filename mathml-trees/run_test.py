import sys

from TreeConverter import *
from TreeReducer import *
from TreePlotter import *

test_filename = "tests/basic1.xml"
if len(sys.argv) > 1:
    test_filename = sys.argv[1]

trees = convertToTrees(test_filename)

for tree in trees:
    presentation_tree = toPresentationTree(tree)
    plotTree(presentation_tree)
    
    content_tree = toContentTree(tree)
    plotTree(content_tree)

    operator_tree = toOperatorTree(tree)
    plotTree(operator_tree)