from lxml import etree as ET
from bs4 import BeautifulSoup
import networkx as nx
from networkx.drawing.nx_agraph import graphviz_layout
import matplotlib.pyplot as plt
import re

# unnecessary attributes to remove from mathml string
REMOVE_ATTRIBUTES = ["id", "xref", "type", "cd", "encoding"]

"""
takes in article html filename
outputs a list of [mathml string, latex alttext] for each "block" equation
    a block equation is an equation that gets its own line in the article (as opposed to an "inline" equation)
    a mathml string is just everything contained in a <math> tag (including the <math> tag)
    the latex alttext is also returned so we can use it later to render and view the equation
"""
def toMathMLStrings(html_filename):
    f = open(html_filename, "r")
    xml = f.read()
    soup = BeautifulSoup(xml)
    mathml_strings = []
    for mms in soup.find_all("math"):

        if mms["display"] != "block": # skip non-block equations
            continue
     
        for attr in REMOVE_ATTRIBUTES: # remove unnecessary attributes
            [s.attrs.pop(attr) for s in mms.find_all() if attr in s.attrs]

        mathml_strings.append([mms.prettify(), mms["alttext"]]) # prettify fixes mismatched tags and formats the HTML better

    return mathml_strings

class Node:
    def __init__(self, value, children=None):
        self.value = value
        self.children = [] if children == None else children

# tags to skip
skip = {'math', 'semantics', 'annotation', 'annotation-xml'}
# operator tags - first child is operator, remaining children are operands
op = {'apply'}
# terminal tags - tags with no children (except few instances), usually represent variables in equation
term = {'ci', 'cn', 'cs', 'csymbol'}

"""
*functions starting with an underscore are helper functions and are not meant to be called outside of this script*
the helper function to toOpTree()
eTree is xml tree object, from lxml library
opTree is operator tree, created using custom Node class
"""
def _eTreeToOpTree(et):
    if et.tag in skip:
        if et.tag == 'semantics': # when we see "semantics" tag we know this is where tree splits between presentation and content ml
            for child in et:
                if child.tag == 'annotation' or child.tag == 'annotation-xml': # the content ml subtree will have "annotation" tag as a root
                    return _eTreeToOpTree(child)
            exit(-1) # throw error if content ml not found
        else:
            return _eTreeToOpTree(et[0]) # skip tag and move on to its child

    elif et.tag in term:
        value = et.text.strip()
        # some term tags have deeper layers of tags before the text (rare but if so usually a nested presentation ml tag)
        while value == "": # keeps going down til we hit text
            if len(list(et)) == 0:
                value = "no text found"
                break
            et = et[0]
            value = et.text.strip()
        return Node(value = value)

    elif et.tag in op:
        value = ""
        children = []

        node = _eTreeToOpTree(et[0]) # first child of op tag is operator
        value = node.value # operator becomes value of node
        children.extend(node.children) # any children the operator may have becomes children of operator node

        for i in range(1, len(list(et))): # remaining children are operands and become children of operator node
            children.append(_eTreeToOpTree(et[i]))

        return Node(value = value.strip(), children = children)

    elif len(list(et)) == 0: # if tag has no children then return a Node with value = tag
        return Node(value = et.tag)

    else: # if tag not caught by this point, we create node with value = tag and move on to its children
        children = []
        for child in et:
            children.append(_eTreeToOpTree(child))
        return Node(value = et.tag, children = children)

"""
takes in mathml_string
returns root of operator tree
most of the work done in helper function above
"""
def toOpTree(mathml_string):
    et = ET.fromstring(mathml_string) # converts mathml string to tree object
    root = _eTreeToOpTree(et)
    return root


"""
some unicode characters don't render in matplotlib
this function takes an unrenderable unicode character and returns an adequate substitute that is renderable
"""
def subMissingGlyph(c):
    uni = ord(c)
    if uni >= 119860 and uni <= 119885:
        new_uni = uni - (119860 - ord('A'))
        return chr(new_uni)
    elif uni >= 119886 and uni <= 119911:
        new_uni = uni - (119886 - ord('a'))
        return chr(new_uni)
    elif uni >= 120572 and uni <= 120596:
        new_uni = uni - (120572 - 0x03B1)
        return chr(new_uni)
    elif uni >= 119834 and uni <= 119859: # mathmetical bold small
        new_uni = uni - (119834 - ord('a'))
        return chr(new_uni)
    elif uni >= 119964 and uni <= 119989: # mathmetical script capital 
        new_uni = uni - (119834 - ord('A'))
        return chr(new_uni)
    elif uni >= 119808 and uni <= 119833: # mathmetical bold capital 
        new_uni = uni - (119834 - ord('A'))
        return chr(new_uni)
    else:
        return chr(uni)

"""
helper function to graphTree()
"""
def _graphTree(G, node, parent_id):
    if node == None:
        return
    node_id = len(G.nodes())
    if len(node.value) == 1:
        node.value = subMissingGlyph(node.value)
    G.add_node(node_id, data = node.value)
    if parent_id !=-1:
        G.add_edge(parent_id, node_id)
    for child in node.children:
        _graphTree(G, child, node_id)

"""
takes in root of opTree
DFS's thru opTree to return nx graph object of it
"""
def graphTree(root):
    G = nx.DiGraph()
    _graphTree(G, root, -1)
    return G

"""
takes in nx graph of tree and title for it
plots tree in aesthetic way with title
"""
def plotTree(tree, title=""):
    plt.title(title, usetex=True)
    pos = nx.nx_agraph.pygraphviz_layout(tree, prog='dot')
    labels = nx.get_node_attributes(tree, 'data') 
    nx.draw(tree, pos, labels = labels, font_size = 8)
    plt.show()

# some latex commands won't work in matplotlib because the required package isn't installed
BAD_COMMANDS = {
    "\\cal", "\\text", "\\hbox"
}

"""
some of the latex alttext doesn't render in matplotlib
this function cleans up alttext so it renders
"""
def cleanUpLatex(s):
    s = s.replace("\n", " ")
    s = s.replace("%", " ")
    for cmd in BAD_COMMANDS:
        s = s.replace(cmd, " ")
    s = "$" + s + "$"
    return s

"""
combines all the functions above to...
take in article html file
return list of nx graph of operator tree for each block equation in file
"""
def getTreesFromFile(filename):
    trees = []
    mathml_strings = toMathMLStrings(filename)
    for i, e in enumerate(mathml_strings): # plot operator trees of all block equations in given test file
        root = toOpTree(e[0])
        G = graphTree(root)
        trees.append(G)
    return trees

"""
combines all the functions above to...
take in article html file
plot operator tree for each block equation in file with latex-rendered equation as plot title
"""
def plotTreesFromFile(filename):
    mathml_strings = toMathMLStrings(filename)
    for i, e in enumerate(mathml_strings): # plot operator trees of all block equations in given test file
        root = toOpTree(e[0])
        G = graphTree(root)
        plotTree(G, cleanUpLatex(e[1]))