import networkx as nx

JUNK_TAGS = {"math", "semantics", "annotation", "annotation-xml"}

def cleanUpTree(tree): # remove junk tags
    clean_tree = tree.copy()

    node_list = list(clean_tree.nodes())
    reversed_node_list = node_list[::-1]

    for node in reversed_node_list:
        if clean_tree.nodes[node]['data'] in JUNK_TAGS:
            clean_tree.remove_node(node)

    return clean_tree

def toPresentationTree(tree):
    skip_nodes = set()

    for node in tree.nodes():
        if tree.nodes[node]['data'] == "semantics":
            children = tree.successors(node)

            skip = False
            for child in children:
                if skip:
                    skip_nodes.add(child)
                    skip_nodes = set.union(skip_nodes, nx.descendants(tree, child))
                else:
                    skip = True

    keep_nodes = [node for node in tree.nodes() if node not in skip_nodes]

    presentation_tree = (tree.subgraph(keep_nodes)).copy()

    return cleanUpTree(presentation_tree)

def toContentTree(tree):
    skip_nodes = set()

    for node in tree.nodes():
        if tree.nodes[node]['data'] == "semantics":
            children = tree.successors(node)

            skip = True
            for child in children:
                if skip:
                    skip_nodes.add(child)
                    skip_nodes = set.union(skip_nodes, nx.descendants(tree, child))
                    skip = False

    keep_nodes = [node for node in tree.nodes() if node not in skip_nodes]

    content_tree = (tree.subgraph(keep_nodes)).copy()

    return cleanUpTree(content_tree)

CONTENT_TERMS = {"ci", "cn", "cs", "csymbol"}

def toOperatorTree(tree):
    content_tree = toContentTree(tree)


    # remove content terminals ("ci", "cn", "cs", "csymbol")
    reduced_tree = content_tree.copy()

    for node in content_tree.nodes():
        if content_tree.nodes[node]['data'] in CONTENT_TERMS:
            children = content_tree.successors(node)

            for child in children:
                reduced_tree.nodes[node]['data'] = content_tree.nodes[child]['data']
                reduced_tree.remove_node(child)
    

    # remove "apply"s
    operator_tree = reduced_tree.copy()

    node_list = list(operator_tree.nodes())
    reversed_node_list = node_list[::-1]

    for node in reversed_node_list:
        if operator_tree.nodes[node]['data'] == "apply":
            children = operator_tree.successors(node)

            
            for child in children:
                if operator_tree.nodes[child]['data'] != "apply":
                    parents = operator_tree.predecessors(node)
                    for parent in parents:
                        operator_tree.add_edge(parent, child)
                    
                    children2 = operator_tree.successors(node)
                    for child2 in children2:
                        if child2 != child:
                            operator_tree.add_edge(child, child2)

                    break

    node_list2 = list(operator_tree.nodes())
    reversed_node_list2 = node_list2[::-1]

    for node in reversed_node_list2:
        if operator_tree.nodes[node]['data'] == "apply":
            operator_tree.remove_node(node)

    return cleanUpTree(operator_tree)
