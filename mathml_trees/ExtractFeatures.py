import networkx as nx

def extractFeatures(t):
    root = None
    for node in t.nodes:
        if t.in_degree(node) == 0:
            root = node
            break
    
    sorted = nx.topological_sort(t)
    var_nodes = []
    for node in sorted:
        if t.out_degree(node) == 0:
            var_nodes.append(node)
    
    features = []
    for i in range(len(var_nodes)):
        for j in range(i+1, len(var_nodes)):
            path_a = nx.shortest_path(t, root, var_nodes[i])
            path_b = nx.shortest_path(t, root, var_nodes[j])
            full_path = []
            for node in reversed(path_a):
                full_path.append(node)
            last_repeat_node = None
            for node in path_b:
                if node in full_path: # want to keep last node that appears in both paths
                    last_repeat_node = node
                    full_path.remove(node)
                else:
                    if last_repeat_node != None:
                        full_path.append(last_repeat_node)
                        last_repeat_node = None
                    full_path.append(node)
            full_path.pop(0)
            full_path.pop(-1)

            operators = []
            for node in full_path:
                operators.append(t.nodes[node]['data'])

            vars = (t.nodes[var_nodes[i]]['data'], t.nodes[var_nodes[j]]['data'])
            features.append([vars, operators])

    return features

def printFeatures(features):
    for f in features:
        var_s = "(" + str(f[0][0]) + "," + str(f[0][1]) + ")"
        op_s = "["
        for op in f[1]:
            op_s += op + ", "
        op_s = op_s[:-2]
        op_s += "]"

        print(var_s + " : " + op_s)
            
