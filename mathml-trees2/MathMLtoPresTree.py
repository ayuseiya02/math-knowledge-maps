from lxml import etree as ET    # used to parse xml as tree structure
import networkx as nx
import matplotlib.pyplot as plt

'''
ExpressionTreeNode: 
    Purpose: stores the value of a each node in the tree and a list of children.
    Input: value (str):                            node data
           children (list of ExpressionTreeNodes): children of current node
    Output: None
'''
class ExpressionTreeNode:
    def __init__(self, value, children=[]):
        self.value = value
        self.children = children or []




'''
to_expr_tree:
    Purpose: wrapper for converting mathml to expression tree
    Input:  mathml_string (str)     : expression to be converted
    Output: (ExpressionTreeNode*)   : pointer to root node of expression tree
'''
def to_expr_tree(mathml_string):
    mathml_string = mathml_string.encode('utf-8')
    mathml_tree = ET.fromstring(mathml_string)
    root = _to_expr_tree(mathml_tree)
    remove_empty_nodes(root,None)
    return root



'''
_to_expr_tree:
    Purpose: convert xml etree to expression tree
    Input:  etree_node (etree*)     : pointer to root of xml tree
    Output: (ExpressionTreeNode*)   : pointer to root of expression tree
'''
def _to_expr_tree(etree_node):
    math_tag = {'mfrac': '/', 'msub': '_', 'msup': '^', 'msubsup': '_^'}
    blank_tag = {'mn', 'mo', 'msub', 'semantics', 'mover', 'mpadded', 'mtext', 'mrow', 'mi'}
    if etree_node.tag in math_tag:                                            # etree tag is a math operator 
        value =  math_tag[etree_node.tag]
        children = [_to_expr_tree(child) for child in etree_node]
        return ExpressionTreeNode(value, children)
        
    elif etree_node.tag in blank_tag:                                         # etree tag has no meaning
        value = etree_node.text or etree_node.attrib.get('value', '')
        children = [_to_expr_tree(child) for child in etree_node]
        return ExpressionTreeNode(value, children)

    elif etree_node.tag == 'math':                                            # etree tag is wrapper for tree
        return _to_expr_tree(etree_node[0])

    else:                                                                     # etree tag is unseen
        raise ValueError('Invalid MathML element: {}'.format(etree_node.tag))




'''
remove_empty_nodes:
    Purpose: iterator for xml etree is restrictive making it diffuclt to remove empty nodes during
             expression tree creation. This a traversal is needed to find and remove these nodes.
    Input:  node (ExpressionTreeNode*):     pointer to subtree to remove empty nodes from
            parent (ExpressionTreeNode*):   pointer to parent of subtree
    Output: (ExpressionTreeNode*):          pointer to root of expression tree
'''
def remove_empty_nodes(node, parent):
    if not node.children:
        return
    if node.value == '' and parent is not None:
        parent.children += node.children
        parent.children.remove(node)
        del node
        for child in parent.children:
            remove_empty_nodes(child, parent)
    else:
        for child in node.children:
            remove_empty_nodes(child, node)




'''
post_order:
    Purpose: perform post order traversal of tree
    Input:  node (ExpressionTreeNode*)      pointer to the root of expression tree
    Output: (list of strings)               a list containing the traversal order
'''   
def post_order(node):
    traversal = []
    def _post_order(node):
        if node is None:
            return
        for child in node.children:
            _post_order(child)
        data = node.value if node.value != '' else 'root'
        traversal.append(data)
    _post_order(node)
    return traversal

mathml_string_1 = '<math><semantics><mrow><mrow><mi>V</mi><msub><mi>M</mi><mi>s</mi></msub><mi>ω</mi></mrow><mo>≳</mo><mrow><mi>γ</mi><msub><mi>k</mi><mi>B</mi></msub><mi>T</mi></mrow></mrow></semantics></math>'
mathml_string_2 = '<math><semantics><mrow><mrow><mrow><mover><mi>F</mi><mo>˙</mo></mover><mi>γ</mi></mrow><mo>/</mo><msub><mi>M</mi><mi>s</mi></msub></mrow><mo>=</mo><mrow><mo>-</mo><mrow><mi>α</mi><msup><mrow><mo>(</mo><msub><mover><mi>𝒎</mi><mo>˙</mo></mover><mi>R</mi></msub><mo>)</mo></mrow><mn>2</mn></msup></mrow></mrow></mrow></semantics></math>' 
mathml_string_3 = '<math><semantics><mrow><mrow><mi>cos</mi><mo>⁡</mo><msub><mi>θ</mi><mn>2</mn></msub></mrow><mo>=</mo><mrow><mo>-</mo><mrow><mrow><mi>ω</mi><mo>/</mo><mi>γ</mi></mrow><msub><mi>M</mi><mi>s</mi></msub><mi>D</mi></mrow></mrow></mrow></semantics></math> '





"""
expressions = [mathml_string_1]
for e in expressions:
    # 0. Convert math expression to tree data structure
    expression_tree = to_expr_tree(e)
    # 1. Perform Post order traversal 
    traversal = post_order(expression_tree)
    print(traversal)
"""