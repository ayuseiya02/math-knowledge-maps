from lxml import etree as ET
from bs4 import BeautifulSoup
import networkx as nx
from networkx.drawing.nx_agraph import graphviz_layout
import matplotlib.pyplot as plt
import re

class Node:
    def __init__(self, value, children=None):
        self.value = value
        self.children = [] if children == None else children

REMOVE_TAGS = ["math", "semantics", "annotation", "annotation-xml"]
REMOVE_ATTRIBUTES = ["id", "xref", "type", "cd"]

def toMathMLStrings(xml_filename):
    f = open(xml_filename, "r")
    xml = f.read()
    soup = BeautifulSoup(xml)
    mathml_strings = []
    for mms in soup.find_all("math"):
        
        if mms["display"] != "block":
            continue
        
        for attr in REMOVE_ATTRIBUTES: 
            [s.attrs.pop(attr) for s in mms.find_all() if attr in s.attrs]

        mathml_strings.append([mms.prettify(), mms["alttext"]])
    return mathml_strings

skip = {'math', 'annotation', 'annotation-xml'}
bin_op = {'apply'}
term = {'ci', 'cn', 'cs', 'csymbol'}

def _eTreeToOpTree(et):
    if et.tag in skip:
        for child in et:
            return _eTreeToOpTree(child)

    elif et.tag == 'semantics':
        for child in et:
            if child.tag == 'annotation' or child.tag == 'annotation-xml':
                #print("content ml found!")
                return _eTreeToOpTree(child)
        #print("content ml not found")
        exit(-1)

    elif et.tag in term:
        #print("terminal tag [" + et.tag + "] with value [" + et.text.strip() + "] found")
        return Node(value = et.text.strip())

    elif len(list(et)) == 0:
        #print("operator tag [" + et.tag + "] found")
        return Node(value = et.tag)

    elif et.tag in bin_op:
        value = ""
        children = []
        child_num = 1
        for child in et:
            if child_num == 1:
                node = _eTreeToOpTree(child)
                value = node.value
                children.extend(node.children)
            else:
                children.append(_eTreeToOpTree(child))
            child_num += 1
        #print("binop tag [" + et.tag + "] with operator [" + value.strip() + "] found")
        return Node(value = value.strip(), children = children)

    elif et.tag == "list":
        children = []
        for child in et:
            node = _eTreeToOpTree(child)
            children.append(node)
        return Node(value = et.tag, children = children)

    else:
        #print("skipping tag [" + et.tag + "]")
        children = []
        for child in et:
            children.append(_eTreeToOpTree(child))
        return Node(value = et.tag, children = children)

def toOpTree(mathml_string):
    et = ET.fromstring(mathml_string)
    root = _eTreeToOpTree(et)
    return root

MISSING_GLYPHS = {

}

"""
119867: 'H', 119889: 'd', 119899: 'n', 119882: 'W',
119904: 's', 119886: 'a', 119901: 'p', 119876: 'Q',
119861: 'B', 119888: 'c', 119902: 'q', 119875: 'P',
119862: 'C', 119911: 'z', 119905: 't', 119880: 'U',
119864: 'E', 119894: 'i', 119895: 'j', 119898: 'm',
119909: 'x', 119874: 'O'
120588: chr(0x03C1), 120574: chr(0x03B3), 120594: chr(0x03C7),
120581: chr(0x03BA), 120582: chr(0x03BB), 120591: chr(0x03C4)
"""

def subMissingGlyph(c):
    uni = ord(c)
    if uni >= 119860 and uni <= 119885:
        new_uni = uni - (119860 - ord('A'))
        return chr(new_uni)
    elif uni >= 119886 and uni <= 119911:
        new_uni = uni - (119886 - ord('a'))
        return chr(new_uni)
    elif uni >= 120572 and uni <= 120594:
        new_uni = uni - (120572 - 0x03B1)
        return chr(new_uni)
    else:
        return chr(uni)

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

def graphTree(root):
    G = nx.DiGraph()
    _graphTree(G, root, -1)
    return G

def plotTree(tree, title=""):
    plt.title(title, usetex=True)
    pos = nx.nx_agraph.pygraphviz_layout(tree, prog='dot')
    labels = nx.get_node_attributes(tree, 'data') 
    nx.draw(tree, pos, labels = labels, font_size = 8)
    plt.show()