import networkx as nx

COMMON_CONSTANTS = [
    0x03C0 # pi
]

def isVar(name):
    if len(name) != 1:
        return False
    if not name.isalpha():
        return False
    if ord(name) in COMMON_CONSTANTS:
        return False
    return True

def standardizeOpTree(t):
    var_nodes = []
    used_names = set()
    for node in t.nodes():
        if t.out_degree(node) == 0:
            name = t.nodes[node]['data']
            if isVar(name):
                var_nodes.append(node)
                used_names.add(name)

    s = t.copy()
    sorted = nx.topological_sort(t)
    substitutions = {}
    idx = ord('a')
    for node in sorted:
        if node not in var_nodes:
            continue

        name = t.nodes[node]['data']
        if name in substitutions.keys():
            s.nodes[node]['data'] = substitutions[name]
        else:
            s.nodes[node]['data'] = chr(idx)
            substitutions.update({name:chr(idx)})
            idx += 1

    return s