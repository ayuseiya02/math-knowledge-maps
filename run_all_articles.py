import os
from mathml_trees.MathMLToOpTree import *

def plotIsomorphs():
    tree_sets = []

    print("generating trees...")

    for i, filename in enumerate(os.listdir('articles')):
        print(str(len(os.listdir('articles')) - i) + " articles remaining")
        tree_sets.append(getTreesFromFile("articles/" + filename))

    print("trees generated")

    isomorphs = []

    for i in range(len(tree_sets)):
        for tree in tree_sets[i]:
            for j in range(len(tree_sets)):
                if i == j:
                    continue
                print("comparing article " + str(i) + " and " + str(j))
                for tree2 in tree_sets[j]:
                    if nx.is_isomorphic(tree, tree2):
                        isomorphs.append([tree, tree2])

    print(str(len(isomorphs)) + "isomorphs found!")

    for iso in isomorphs:
        plotTree(iso[0], "A")
        plotTree(iso[1], "B")