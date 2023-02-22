import os
from mathml_trees.MathMLToOpTree import *
from mathml_trees.StandardizeOpTree import *

def plotRepeats():
    print("generating trees...")
    tree_sets = []
    for i, filename in enumerate(os.listdir('articles')):
        print(str(len(os.listdir('articles')) - i) + " articles remaining")
        tree_sets.append(getTreesFromFile("articles/" + filename))
    print("trees generated")

    print("generating std trees...")
    std_tree_sets = []
    for tree_set in tree_sets:
        std_tree_set = []
        for tree in tree_set:
            std_tree_set.append(standardizeOpTree(tree))
        std_tree_sets.append(std_tree_set)
    print("std trees generated")

    repeats = []
    for i in range(len(std_tree_sets)):
        for tree in std_tree_sets[i]:
            for j in range(i + 1, len(std_tree_sets)):
                print("comparing article " + str(i) + " and " + str(j))
                for tree2 in std_tree_sets[j]:
                    if nx.utils.graphs_equal(tree, tree2):
                        repeats.append([tree, i, j])
    print(str(len(repeats)) + "repeats found!")

    article_names = os.listdir('articles')
    for repeat in repeats:
        plotTree(repeat[0], article_names[repeat[1]][:-5] + " and " + article_names[repeat[2]][:-5])

plotRepeats()