saved_nodes = {}    # MathML expression trees use structure sharing, resuing frequently used nodes

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
        self.bounds = None



'''
to_expr_tree:
    Purpose: wrapper for converting mathml to expression tree
    Input:  mathml_string (str)     : expression to be converted
    Output: (ExpressionTreeNode*)   : pointer to root node of expression tree
'''
def to_expr_tree(mathml_string):
    mathml_string = mathml_string.encode('utf-8')
    mathml_tree = ET.fromstring(mathml_string)
    root = xml_to_tree(mathml_tree)
    return root



'''
xml_to_tree:
    Purpose: converting mathml to expression tree
    Input:  mathml_string (str)     : expression to be converted
    Output: (ExpressionTreeNode*)   : pointer to root node of expression tree
'''

bin_op = {'apply'}
term = {'ci', 'cn', 'csymbol', 'cs'}

def xml_to_tree(xml):
    if xml.tag == 'semantics':
        for child in xml:
            if child.tag == 'annotation' or child.tag == 'annotation-xml':
                print("content ml found!")
                return xml_to_tree(child)
        print("content ml not found")
        return(-1)

    elif xml.tag in term:
        print("terminal tag [" + xml.tag + "] with value [" + xml.text + "] found")
        return Node(value = xml.text)

    elif xml.tag in bin_op:
        value = ""
        children = []
        child_num = 1
        for child in xml:
            if child_num == 1:
                value = child.tag
                print("binop tag [" + xml.tag + "] with value [" + value + "] found")
            else:
                children.append(xml_to_tree(child))
            child_num += 1
        return Node(value = value, children = children)

    else:
        print("skipping tag [" + xml.tag + "]")
        for child in xml:
            return xml_to_tree(child)

"""
    if xml.tag in ignore:
        print("-----------")
        for child in xml:
            print(child.tag)
            return xml_to_tree(child)

    elif xml.tag in pull_value: 
        return Node(value = xml.text, children = [xml_to_tree(child) for child in xml]) # standard node

    elif xml.tag == 'bind':
        children =  [xml_to_tree(child) for child in xml]
        operator = children[0]                         # first child = binding operator
        operator.bounds = children[1:-1]               # middle child = list ofÂ bvar elements denoting bound variables
        operator.children = [children[-1]]             # final child =  Content MathML expression
        return operator

    elif xml.tag == 'share':                           # pull node id
        return saved_nodes[xml.attrib['href']]
"""
    







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


def makeTree(G, node, parent_id):
    node_id = len(G.nodes())
    G.add_node(node_id, data = node.value)
    if parent_id !=-1:
        G.add_edge(parent_id, node_id)
    for child in node.children:
        makeTree(G, child, node_id)


def plotTree(tree):
    pos = nx.nx_agraph.pygraphviz_layout(tree, prog='dot')
    labels = nx.get_node_attributes(tree, 'data') 
    nx.draw(tree, pos, labels = labels, font_size = 8)
    plt.show()

"""
for i, e in enumerate(expressions):
    # 0. Convert math expression to tree data structure
    expression_tree = to_expr_tree(e)
    print("TEST CASE: " + str(i))
    print (BeautifulSoup(e).prettify(), '\n')
    G = nx.DiGraph()
    makeTree(G, expression_tree, -1)
    plotTree(G)

     

    #print_tree(expression_tree)
    # 1. Perform Post order traversal 
    traversal = post_order(expression_tree)
    print(traversal)
    print()
    print()
    i+=1
"""