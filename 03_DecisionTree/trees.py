'''
# 2016-01-01 ~ 
# Decision Tree
# UTF-8 encoding, Line encoding use LF(UNIX)

# coding and comments by Yedarm Seong
# mybirth0407@gmail.com
'''

from math import log
import operator

def CalcShannonEntrophy(data_set):
    num_entries = len(data_set)
    label_counts = {}

    for feature_vector in data_set:
        current_label = feature_vector[-1]

        if current_label not in label_counts.keys():
            label_counts[current_label] = 0
            label_counts[current_label] += 1
    shannon_entrophy = 0.0

    for key in label_counts:
        prob = float(label_counts[key]) / num_entries
        shannon_entrophy -= prob * log(prob, 2)

    return shannon_entrophy

def CreateDataSet():
    data_set = [[1, 1, "yes"],
                [1, 1, "yes"],
                [1, 0, "no"],
                [0, 1, "no"],
                [0, 1, "no"]]
    labels = ["no surfacing", "flippers"]

    return data_set, labels

def SplitDataSet(data_set, axis, value):
    return_data_set = []

    for feature_vector in data_set:
        if feature_vector[axis] == value:
            reduced_feature_vector = feature_vector[ :axis]
            reduced_feature_vector.extend(feature_vector[axis + 1: ])
            return_data_set.append(reduced_feature_vector)

    return return_data_set

def ChooseBestFeatureToSplit(data_set):
    num_features = len(data_set[0]) - 1
    best_entrophy = CalcShannonEntrophy(data_set)
    best_information_gain = 0.0;
    best_feature = -1

    for i in range(num_features):
        feature_list = [example[i] for example in data_set]
        unique_values = set(feature_list)
        new_entrophy = 0.0

        for value in unique_values:
            sub_data_set = SplitDataSet(data_set, i, value)
            prob = len(sub_data_set) / float(len(data_set))
            new_entrophy += (prob * CalcShannonEntrophy(sub_data_set))

        information_gain = best_entrophy - new_entrophy

        if information_gain > best_information_gain:
            best_information_gain = information_gain
            best_feature = i

    return best_feature

def MajorityCount(class_list):
    class_count = {}

    for vote in class_list:
        if vote not in class_count.keys(): class_count[vote] = 0
        class_count[vote] += 1

    sorted_class_count = sorted(class_count.items(),
                                key = operator.itemgetter(1),
                                reversed = True)

    return sorted_class_count[0][0]

def CreateTree(data_set, labels):
    class_list = [example[-1] for example in data_set]

    if class_list.count(class_list[0]) == len(class_list):
        return class_list[0]

    if len(data_set[0]) == 1:
        return MajorityCount(class_list)

    best_feature = ChooseBestFeatureToSplit(data_set)
    best_feature_label = labels[best_feature]

    my_tree = { best_feature_label: {}}
    del(labels[best_feature])
    featrue_values = [example[best_feature] for example in data_set]
    unique_values = set(featrue_values)

    for value in unique_values:
        sub_labels = labels[: ]
        my_tree[best_feature_label][value] = CreateTree(SplitDataSet(
                                data_set, best_feature, value), sub_labels)

    return my_tree

def Classify(input_tree, feat_labels, test_vector):
    first_str = list(input_tree.keys())[0]
    second_dict = input_tree[first_str]
    feat_index = feat_labels.index(first_str)

    for key in second_dict.keys():
        if test_vector[feat_index] == key:
            if type(second_dict[key]).__name__=="dict":
                class_label = Classify(
                    second_dict[key], feat_labels, test_vector)
            else:
                class_label = second_dict[key]

    return class_label

def StoreTree(input_tree, filename):
    import pickle
    fw = open(filename, 'w')
    pickle.dump(input_tree, fw)
    fw.close()

def GrabTree(filename):
    import pickle
    fr = open(filename)

    return pickle.load(fr)
