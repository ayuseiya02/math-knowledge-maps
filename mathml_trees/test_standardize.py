import sys

from MathMLToOpTree import *   
from StandardizeOpTree import *

trees1 = getTreesFromFile("tests/custom/basic1.xml")
trees2 = getTreesFromFile("tests/custom/basic3.xml")

tree1 = trees1[0]
tree2 = trees2[0]

plt.subplot(121)
pos = nx.nx_agraph.pygraphviz_layout(tree1, prog='dot')
labels = nx.get_node_attributes(tree1, 'data') 
nx.draw(tree1, pos, labels = labels, font_size = 8)
plt.subplot(122)
pos = nx.nx_agraph.pygraphviz_layout(tree2, prog='dot')
labels = nx.get_node_attributes(tree2, 'data') 
nx.draw(tree2, pos, labels = labels, font_size = 8)
plt.suptitle("graphs equal? " + str(nx.utils.graphs_equal(tree1, tree2)))
plt.show()

std_tree1 = standardizeOpTree(tree1)
std_tree2 = standardizeOpTree(tree2)

plt.subplot(121)
pos = nx.nx_agraph.pygraphviz_layout(std_tree1, prog='dot')
labels = nx.get_node_attributes(std_tree1, 'data') 
nx.draw(std_tree1, pos, labels = labels, font_size = 8)
plt.subplot(122)
pos = nx.nx_agraph.pygraphviz_layout(std_tree2, prog='dot')
labels = nx.get_node_attributes(std_tree2, 'data') 
nx.draw(std_tree2, pos, labels = labels, font_size = 8)
plt.suptitle("graphs equal? " + str(nx.utils.graphs_equal(std_tree1, std_tree2)))
plt.show()