import math
import numpy as np
from numpy import linalg as LA

def train_gem_balls(scenarios, labels = [0, 1], c = [1, 1]):
    # c values: complexity parameters; increasing the value of c[0] generates 1-labelled balls of larger size so providing higher sensitivity

    # Check if there are only scenarios labelled as the given labels
    for s in scenarios:
        if s[1] not in labels:
            print("ERROR: the scenarios are not correctly labelled.")
            return None

    classifier = []
    complete = False

    x = np.array(column(scenarios, 0))
    y = np.array(column(scenarios, 1))

    x_c = x[0, :]
    y_c = y[0]

    R = x[1:, :]
    L = y[1:]

    support = [None] * len(labels)

    while not complete:
        opposite_label = (y_c + 1) % 2

        [distances, indexes] = calculate_distances(R, x_c)
        
        R = R[indexes]
        L = L[indexes]

        opposite_positions = np.where(L == opposite_label)[0]
        support_positions = opposite_positions[0:min(c[opposite_label], len(opposite_positions))]

        support_array = support[opposite_label]
        if support_array == None:
            support_array = []

        if len(opposite_positions) < c[opposite_label]:
            classifier.append([x_c, math.inf, y_c])
            support_array.append([math.inf] * len(x_c))

            complete = True
        else:
            classifier.append([x_c, distances[support_positions[-1]], y_c])
            support_array.append(R[support_positions])

            x_c = R[support_positions[-1]]
            y_c = L[support_positions[-1]]
            
            R = R[min(support_positions[-1]+1, len(R)-1):]
            L = L[min(support_positions[-1]+1, len(L)-1):]

        support[opposite_label] = support_array

    cardinalities_per_label = [0] * len(labels)
    scenarios_per_label = [0] * len(labels)
    for i in range(len(labels)):
        cardinalities_per_label[i] = len(support[i])
        scenarios_per_label[i] = len(np.where(y == labels[i])[0])

    return classifier, cardinalities_per_label, scenarios_per_label


def column(matrix, i):
    return [row[i] for row in matrix]


def calculate_distances(R, x_c):
    distances = [[]] * len(R)
    for i in range(len(R)):
        distances[i] = [LA.norm(x_c - R[i]), i]

    distances.sort() # it automatically sorts by the first values of matrix
    return column(distances, 0), column(distances, 1)


"""def order_based_on_indexes(array, indexes):
    if indexes == [0]: # we have the last x
        return array

    new_array = []
    for index in indexes:
        new_array.append(array[index])
    return new_array"""


"""def search_indexes_by_label(array, label):
    if len(array) == 1: # We have the last x
        if array[0] == label:
            return array
        return []

    new_array = []
    for i in range(len(array)):
        if array[i] == label:
            new_array.append(i)
    return new_array"""


"""def get_elements_by_indexes(array, indexes):
    new_array = []
    for index in indexes:
        new_array.append(array[index])
    return new_array"""


"""def number_of_scenarios_with_given_label(array, label):
    count = 0
    for element in array:
        if element[1] == label:
            count += 1
    return count"""

