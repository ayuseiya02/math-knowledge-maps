from TreeConverter import *

import matplotlib.pyplot as plt
#import pydot
#from networkx.drawing.nx_pydot import graphviz_layout

plt.rcParams["font.family"] = "/System/Library/Fonts/Supplemental/STIXGeneralBol.otf"

def plotTree(tree):
    pos = nx.nx_agraph.pygraphviz_layout(tree, prog='dot')
    labels = nx.get_node_attributes(tree, 'data') 
    nx.draw(tree, pos, labels = labels, font_size = 8)
    plt.show()