import matplotlib.pyplot as plt

decision_node = dict(boxstyle = "sawtooth", fc = "0.8")
leaf_node = dict(boxstyle = "round4", fc = "0.8")
arrow_args = dict(arrowstyle = "<-")

def PlotNode(node_txt, center_plot, parent_plot, node_type):
    CreatePlot.ax1.annotate(node_txt, xy = parent_plot,
                            xycoords = "axes fraction", xytext = center_plot,
                            textcoords = "axes fraction",
                            va = "center", ha = "center",
                            bbox = node_type, arrowprops = arrow_args)

def CreatePlot():
    fig = plt.figure(1, facecolor="white")
    fig.clf()
    CreatePlot.ax1 = plt.subplot(111, frameon=False)
    PlotNode("a decision node", (0.5, 0.1), (0.1, 0.5), decision_node)
    PlotNode("a leaf node", (0.8, 0.1), (0.3, 0.8), leaf_node)
    plt.show()

def GetNumLeafs(my_tree):
    num_leafs = 0
    first_str = list(my_tree.keys())[0]
    second_dict = my_tree[first_str]

    for key in second_dict.keys():
        if type(second_dict[key]).__name__ == "dict":
            num_leafs += GetNumLeafs(second_dict[key])
        else:
            num_leafs += 1

    return num_leafs

def GetTreeDepth(my_tree):
    max_depth = 0
    first_str = list(my_tree.keys())[0]
    second_dict = my_tree[first_str]

    for key in second_dict.keys():
        if type(second_dict[key]).__name__ == "dict":
            this_depth = 1 + GetTreeDepth(second_dict[key])
        else:
            this_depth = 1

        if this_depth > max_depth:
            max_depth = this_depth

    return max_depth

def RetrieveTree(i):
    list_of_trees = [{ "no surfacing": { 0: "no", 1: { "flippers":
                    { 0: "no", 1: "yes"}}}},
                    { "no surfacing": { 0: "no", 1: { "flippers":
                    { 0: { "head": { 0: "no", 1: "yes"}}, 1: "no"}}}}]

    return list_of_trees[i]

def PlotMidText(cntr_pt, parent_pt, txt_string):
    x_mid = ((parent_pt[0] - cntr_pt[0]) / 2.0) + cntr_pt[0]
    y_mid = ((parent_pt[1] - cntr_pt[1]) / 2.0) + cntr_pt[1]
    CreatePlot.ax1.text(x_mid, y_mid, txt_string)

def PlotTree(my_tree, parent_pt, node_txt):
    num_leafs = GetNumLeafs(my_tree);
    GetTreeDepth(my_tree)
    first_str = list(my_tree.keys())[0];
    cntr_pt = (PlotTree.x_off +
               (1.0 + float(num_leafs)) / (2.0 / PlotTree.total_width),
               PlotTree.y_off)
    PlotMidText(cntr_pt, parent_pt, node_txt)
    PlotNode(first_str, cntr_pt, parent_pt, decision_node)
    second_dict = my_tree[first_str]
    PlotTree.y_off -= (1.0 / PlotTree.total_depth)

    for key in second_dict.keys():
        if type(second_dict[key]).__name__ == "dict":
            PlotTree(second_dict[key], cntr_pt, str(key))
        else:
            PlotTree.x_off += (1.0 / PlotTree.total_width)
            PlotNode(second_dict[key], (PlotTree.x_off, PlotTree.y_off),
                     cntr_pt, leaf_node)
            PlotMidText((PlotTree.x_off, PlotTree.y_off), cntr_pt, str(key))
    PlotTree.y_off += (1.0 / PlotTree.total_depth)

def CreatePlot(in_tree):
    fig = plt.figure(1, facecolor="white")
    fig.clf()
    
    axprops = dict(xticks=[], yticks=[])
    CreatePlot.ax1 = plt.subplot(111, frameon=False, **axprops)
    PlotTree.total_width = float(GetNumLeafs(in_tree))
    PlotTree.total_depth = float(GetTreeDepth(in_tree))
    PlotTree.x_off = -(0.5 / PlotTree.total_width)
    PlotTree.y_off = 1.0
    PlotTree(in_tree, (0.5, 1.0), '')
    plt.show()
