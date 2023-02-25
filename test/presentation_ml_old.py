import re
from lxml import etree as ET
from bs4 import BeautifulSoup
import networkx as nx
#import graphviz 
from networkx.drawing.nx_agraph import graphviz_layout
import matplotlib.pyplot as plt


saved_nodes = {}    # MathML expression trees use structure sharing, resuing frequently used nodes




"""
strip_comments:
    Purpose:    deletes broken tags & comments from math ML string.
    Input:      presentation_ml_string (str): The presentation ML string to remove comments from.
    Output:     str: The presentation ML string with comments removed.
"""
def strip_comments(presentation_ml_string):
    comment = r"<!--(.*?)-->"  # pattern for matching HTML-style comments
    space = r"<mspace[^>]*\/>"

    ret = re.sub(comment, "", presentation_ml_string)
    ret = re.sub(space, "", ret)
    print(ret)
    return ret

'''
Node: 
    Purpose: stores the value of a each node in the tree and a list of children.
    Input: value (str):              node data
           children (list of Nodes): children of current node
    Output: None
'''
class Node:
    def __init__(self, value, children=None, bounds=None):
        self.value = value
        self.children = [] if children == None else children
        self.edges = []
        self.bounds = None
    
    def add_child(self, child, edge=''):
        if child:
            self.children.append(child)
            self.edges.append(edge)



'''
to_expr_tree:
    Purpose: wrapper for converting mathml to expression tree
    Input:  mathml_string (str)     : expression to be converted
    Output: (ExpressionTreeNode*)   : pointer to root node of expression tree
'''
def to_expr_tree(mathml_string):
    mathml_string = mathml_string.encode('utf-8')
    mathml_tree = ET.fromstring(mathml_string)
    print(ET.tostring(mathml_tree,pretty_print=True))
    root = xml_to_tree(mathml_tree)
    remove_mrow_nodes(root)
    return root


'''
xml_to_tree:
    Purpose: converting mathml to expression tree
    Input:  mathml_string (str)     : expressionput it outside the  to be converted
    Output: (ExpressionTreeNode*)   : pointer to root node of expression tree
'''
pull_value = {'mi', 'mn', 'mo', 'ms', 'mtext'}
placeholders = {'NONE', 'mrow', 'menclose', 'del', 'mphantom'}
u = {'mroot':'sup'}
subscripts = {'msub':'sub', 'msup':'sup' }
d= {}
ud = {}
replace = {'msqrt':'√', 'mfrac':'/', 'mroot':'√', 'mover':'⏞', 'munder':'⏟'}


def xml_to_tree(xml):
    root = Node('',[])
    _xml_to_tree(xml,root)
    return root

def _xml_to_tree(xml, node):
    children = [child for child in xml]
    prev_child_node = node
    prev_xml = xml

    p_tag = prev_xml.tag

    temp_child = None

    if p_tag in u:
        bottom_child = children[-1]
        children = children[:-1]

        bottom_child_node = Node(bottom_child.text)
        prev_child_node.add_child(bottom_child_node, f'{p_tag}_{u[p_tag]}')

    if p_tag in subscripts:
        bottom_child = children[-1]
        children = children[:-1]

        temp_child = Node(bottom_child.text)
    
    for child in children:
        edge_label = prev_xml.tag

        child_node = Node(child.text if child.text else replace[child.tag] if child.tag in replace else 'NONE')
        
        if temp_child:
            child_node.add_child(temp_child, subscripts[p_tag])
        
        prev_child_node.add_child(child_node, edge_label)
        _xml_to_tree(child, child_node)

        if p_tag != 'mfrac':
            prev_child_node = child_node
            prev_xml = child


        

    

def remove_mrow_nodes(node, parent=None):
    if node.value in placeholders:
        if parent is not None:
            parent_index = parent.children.index(node)
            parent.children.pop(parent_index)
            parent.children[parent_index:parent_index] = node.children
        else:
            node.children.clear()
    else:
        for child in node.children:
            remove_mrow_nodes(child, node)



'''
to_string:
    Purpose: converting mathml to expression tree
    Input:  mathml_string (str)     : expression to be converted
    Output: (ExpressionTreeNode*)   : pointer to root node of expression tree
'''
def to_string(bounds):
    def stringify(bound):
        if bound == []:
            return ""
        output= bound.value
        left_children = stringify(bound.children[:len(bound.children)//2 + 1])
        right_children = stringify(bound.children[len(bound.children)//2 + 1:])
        return left_children + " " + output + " " + right_children
    bound_list = []
    for bound in bounds:
        bound_list.append(stringify(bound))
    return " | ".join(bound_list)


'''
print_tree:
    Purpose: prints expression tree in simple
    Input:  node     : expression to be printed
    Output: None     : prints 
'''
def print_tree(node, level=0):
    to_print = node.value + to_string(node.bounds) if node.bounds else node.value
    print("  " * level + to_print)
    for child in node.children:
        print("  " * level + "|__", end="")
        print_tree(child, level + 1)


'''
post_order:
    Purpose: perform post order traversal of tree
    Input:  node (ExpressionTreeNode*)      pointer to the root of expression tree
    Output: (list of strings)               a list containing the traversal order
'''   
def post_order(node):
    traversal = []
    def _post_order(node):
        for child in node.children:
            _post_order(child)
        traversal.append(node.value) if not node.bounds else traversal.append(node.value + to_string(node.bounds))
    _post_order(node)
    return traversal


'''
make_tree:
    Purpose: converts Node Tree to networkX DiGraph
    Input: node (Node):     contentML subtree node
    Output:                 networkX graph
'''
def make_tree(node):
    G = nx.DiGraph()
    def make_tree_helper(node, parent_id, edge_name):
        node_id = len(G.nodes())
        G.add_node(node_id, data = node.value if not node.bounds else node.value + to_string(node.bounds))
        if parent_id !=-1:
            G.add_edge(parent_id, node_id, name=edge_name)
        for child, edge_name in zip(node.children, node.edges):
            make_tree_helper(child, node_id, edge_name)
    make_tree_helper(node, -1, '')
    return G


'''
plot_tree:
    Purpose: converts Node Tree to DiGraph
    Input: G (nx.Digraph): graph object
    Output:  Displays Tree    
'''
def plotTree(tree):
    for node in tree.nodes():
        print(tree.nodes[node]['data'])
    pos = nx.nx_agraph.pygraphviz_layout(tree, prog='dot')
    labels = nx.get_node_attributes(tree, 'data') 

    edge_labels = dict([((n1, n2), d['name'])
                    for n1, n2, d in G.edges(data=True)])
    nx.draw_networkx_edge_labels(G , pos, edge_labels=edge_labels,
                             font_color='red', font_weight='bold')

    nx.draw(tree, pos, labels = labels, font_size = 8, with_labels=True)
    plt.show()



# Token Elements 
mi = '<math display="block"><!-- Multiple characters, default mathvariant is "normal". --><mi>sin</mi></math>'
mn = '<math display="block"><mn>twelve</mn></math>'
mo1 = '<math display="block"><mn>5</mn><mo>+</mo><mn>5</mn></math>'
mo2 = '<math display="block"><mrow><mo>[</mo> <!-- default form value: prefix --><mrow><mn>0</mn><mo>;</mo> <!-- default form value: infix --><mn>1</mn></mrow><mo>)</mo> <!-- default form value: postfix --></mrow></math>'
ms = '<math display="block"><ms>Hello World!</ms></math>'
mspace = '<math display="block"><mn>1</mn><mspace depth="40px" height="20px" width="100px"style="background: lightblue;"/><mn>2</mn></math>'
mtext = '<math display="block"><mtext>Theorem of Pythagoras</mtext></math>'
tokens = [mi,mn, mo1, mo2,ms, mspace, mtext]

# General Layout
menclose = '<math display="block"><menclose notation="circle box"><mi>x</mi><mo>+</mo><mi>y</mi></menclose></math>'
mfrac = '<math display="block"><mfrac><mrow><mi>a</mi><mo>+</mo><mn>2</mn></mrow><mrow><mn>3</mn><mo>−</mo><mi>b</mi></mrow></mfrac></math>'
# mpadded = '<math display="block"><mpadded width="400px" height="5em" depth="4em"lspace="300px" voffset="-2em"style="background: lightblue"><mi>x</mi><mo>+</mo><mi>y</mi></mpadded></math>'
msqrt = '<math display="block"><msqrt><mi>x</mi></msqrt></math>'
mphantom = '<math display="block"><mrow><mi>x</mi><mo>+</mo><mphantom><mi>y</mi><mo>+</mo></mphantom><mi>z</mi></mrow></math>'
mroot = '<math display="block"><mroot><mi>x</mi><mn>3</mn></mroot></math>'
layout = [mroot, msqrt]

# menclose, mfrac, msqrt, mphantom, 


#Script 
mmultiscripts = '''
<math display="block"><mmultiscripts>
    <mi>X</mi>      <!-- base expression -->
    <mi>d</mi>      <!-- postsubscript -->
    <mi>c</mi>      <!-- postsuperscript -->
    <mprescripts />
    <mi>b</mi>      <!-- presubscript -->
    <mi>a</mi>      <!-- presuperscript -->
  </mmultiscripts>
</math>
'''
msup = '''
<math display="block">
  <msup>
    <mi>X</mi>
    <mn>2</mn>
  </msup>
</math>
'''

msub = '''
<math display="block">
  <msub>
    <mi>X</mi>
    <mn>1</mn>
  </msub>
</math>
'''

msub2 = '''
<math display="block">
  <msub>
    <mrow>
        <mi>a</mi>
        <mo>+</mo>
        <mi>b</mi>
    </mrow>
    <mn>1</mn>
  </msub>
</math>
'''

mtable = '''<math display="block">
  <mi>X</mi>
  <mo>=</mo>
  <mtable frame="solid" rowlines="solid" align="axis 3">
    <mtr>
      <mtd><mi>A</mi></mtd>
      <mtd><mi>B</mi></mtd>
    </mtr>
    <mtr>
      <mtd><mi>C</mi></mtd>
      <mtd><mi>D</mi></mtd>
    </mtr>
    <mtr>
      <mtd><mi>E</mi></mtd>
      <mtd><mi>F</mi></mtd>
    </mtr>
  </mtable>
</math>'''

script = [mfrac, msub2, msub, msup, mmultiscripts]

expressions = script

for i, e in enumerate(expressions):
    # 0. Convert math expression to tree data structure
    print('top')
    print(strip_comments(e))
    expression_tree = to_expr_tree(strip_comments(e))
    G = make_tree(expression_tree)
    plotTree(G)













