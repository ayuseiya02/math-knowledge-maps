import sys

from MathMLToOpTree import *   
from StandardizeOpTree import *

test_filename = "tests/custom/basic1.xml" # default test file
if len(sys.argv) > 1: # but will run diff test file if one is passed as argument
    test_filename = sys.argv[1]
trees = getTreesFromFile(test_filename)

for tree in trees:
    plt.subplot(121)
    pos = nx.nx_agraph.pygraphviz_layout(tree, prog='dot')
    labels = nx.get_node_attributes(tree, 'data') 
    nx.draw(tree, pos, labels = labels, font_size = 8)
    
    std_tree = standardizeOpTree(tree)
    plt.subplot(122)
    pos = nx.nx_agraph.pygraphviz_layout(std_tree, prog='dot')
    labels = nx.get_node_attributes(std_tree, 'data') 
    nx.draw(std_tree, pos, labels = labels, font_size = 8)

    plt.show()

