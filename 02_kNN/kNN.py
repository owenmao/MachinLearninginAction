'''
# 2015-12-30 ~ 
# k-Nearest Neighbors algorithms
# UTF-8 encoding, Line encoding use LF(UNIX)

# coding and comments by Yedarm Seong
# mybirth0407@gmail.com
'''

from numpy import *
import operator
import os

def CreateDataSet():
    group = array([[1.0, 1.1], [1.0, 1.0], [0, 0], [0, 0.1]])
    labels = ['A', 'A', 'B', 'B']

    return group, labels

'''
# in_x: 분류하기 위한 벡터
# data_set: 입력받은 행렬
# labels: 분류할 라벨이 표기된 벡터
# k: 투표할 최근접 이웃의 수
'''
def Classfiy0(in_x, data_set, labels, k):
    data_set_size = data_set.shape[0]
    diff_matrix = tile(in_x, (data_set_size, 1)) - data_set

    square_diff_matrix = diff_matrix ** 2
    square_distances = square_diff_matrix.sum(axis = 1)

    distances = square_distances ** 0.5
    sorted_distance_indicies = distances.argsort()
    class_count = {}

    for i in range(k):
        vote_i_label = labels[sorted_distance_indicies[i]]
        class_count[vote_i_label] = class_count.get(vote_i_label, 0) + 1

    sorted_class_count = sorted(class_count.items(),
                                key = operator.itemgetter(1),
                                reverse = True)
                                
    return sorted_class_count[0][0]

'''
filename: 입력받은 파일명
'''
def File2Matrix(filename):
    fr = open(filename)
    number_of_lines = len(fr.readlines())
    return_matrix = zeros((number_of_lines, 3))
    class_label_vector = []
    fr.seek(0)
    index = 0

    for line in fr.readlines():
        line =  line.strip()
        list_from_line = line.split('\t')
        return_matrix[index, : ] = list_from_line[0: 3]
        class_label_vector.append(list_from_line[-1])
        index += 1

    return return_matrix, class_label_vector

'''
data_set: 입력받은 행렬
'''
def AutoNorm(data_set):
    min_values = data_set.min(0)
    max_values = data_set.max(0)

    ranges = max_values - min_values
    norm_data_set = zeros(shape(data_set))
    m = data_set.shape[0]
    norm_data_set = data_set - tile(min_values, (m, 1))
    norm_data_set = norm_data_set / tile(ranges, (m, 1))
    
    return norm_data_set, ranges, min_values

def DatingClassTest():
    ho_ratio= 0.10
    dating_data_matrix, dating_labels = File2Matrix("datingTestSet2.txt")
    norm_martrix, ranges, min_values = AutoNorm(dating_data_matrix)
    m = norm_martrix.shape[0]
    number_test_vectors = int(m * ho_ratio)
    error_count = 0.0

    for i in range(number_test_vectors):
        classifier_result = Classfiy0(norm_martrix[i, :],
                                norm_martrix[number_test_vectors: m, :],
                                dating_labels[number_test_vectors: m], 3)

        print("the classifier came back with: %d, the real answer is %d"
            % (int(classifier_result), int(dating_labels[i])))
        
        if classifier_result != dating_labels[i]:
            error_count += 1.0

    print("the total error rate is: %f"
        % (float(error_count) / float(number_test_vectors)))

def ClassifyPerson():
    result_list = ["not at all", "in small doses", "in large doses"]
    video_games = float(input(
        "percentage of time spent playing video games? "))
    flier = float(input(
        "frequent flier miles earned per year? "))
    ice_cream = float(input(
        "liters of ice cream consumed per year? "))

    dating_data_matrix, dating_labels = File2Matrix("datingTestSet2.txt")
    norm_martrix, ranges, min_values = AutoNorm(dating_data_matrix)
    in_array = array([flier, video_games, ice_cream])

    classifier_result = Classfiy0((in_array - min_values) / ranges,
                                    norm_martrix, dating_labels, 3)

    print("You will probably like this person:",
        result_list[int(classifier_result) - 1])

'''
filename: 입력받은 파일명
'''
def Img2Vector(filename):
    return_vector = zeros((1, 1024))
    fr = open(filename)

    for i in range(32):
        line_str = fr.readline()

        for j in range(32):
            return_vector[0, (32 * i) + j] = int(line_str[j])

    return return_vector

def HandwritingClassTest():
    handwrite_labels = []
    training_file_list = os.listdir("trainingDigits")
    m = len(training_file_list)
    training_matrix = zeros((m, 1024))

    for i in range(m):
        file_name_str = training_file_list[i]
        file_str = file_name_str.split('.')[0]
        class_number_str = int(file_str.split('_')[0])
        handwrite_labels.append(class_number_str)

        training_matrix[i, :] = Img2Vector("trainingDigits/%s"
            % (file_name_str))

    test_file_list = os.listdir("testDigits")
    error_count = 0.0
    m_test = len(test_file_list)

    for i in range(m_test):
        file_name_str = test_file_list[i]
        file_str = file_name_str.split('.')[0]
        class_number_str = int(file_str.split('_')[0])
        vector_under_test = Img2Vector("testDigits/%s" % (file_name_str))

        classifier_result = Classfiy0(vector_under_test, training_matrix,
                                        handwrite_labels, 3)

        print("the classifier came back with: %d, the real answer is: %d"
            % (classifier_result, class_number_str))

        if classifier_result != class_number_str:
            error_count += 1.0

    print("\nthe total number of errors is: %d" % (error_count))
    print("\nthe total error rate is: %f" % (error_count / float(m_test)))
