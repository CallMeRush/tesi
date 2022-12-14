# Implementation without numpy. It has (almost) the same results (distances are 
# the same until at least the fifth decimal point), but with bigger data sizes 
# it is sigificantly slower. 

import math

def train_old(scenarios, labels = [0, 1], c = [1, 1]):
    # c values: complexity parameters; increasing the value of c[0] generates 1-labelled balls of larger size so providing higher sensitivity

    # Check if there are only scenarios labelled as the given labels
    for s in scenarios:
        if s[1] not in labels:
            print("ERROR: the scenarios are not correctly labelled.")
            return None

    classifier = []
    complete = False
    
    x = [row[0] for row in scenarios]
    y = [row[1] for row in scenarios]

    x_c = x[0]
    y_c = y[0]

    R = x[1:]
    L = y[1:]

    support = [None] * len(labels)

    while not complete:
        opposite_label = (y_c + 1) % 2

        [distances, indexes] = calculate_distances(R, x_c)

        R = order_based_on_indexes(R, indexes)
        L = order_based_on_indexes(L, indexes)

        opposite_positions = search_indexes_by_label(L, opposite_label, labels)
        support_positions = opposite_positions[0:min(c[opposite_label], len(opposite_positions))]

        support_array = support[opposite_label]
        if support_array == None:
            support_array = []

        if len(opposite_positions) < c[opposite_label]:
            complete = True

            distance_to_append = math.inf
            classifier.append([x_c, distance_to_append, y_c])

            support_array.append([math.inf] * len(x_c))
        else:
            # to floor to nearest float: // 1e-15 * 1e-15
            distance_to_append = distances[support_positions[-1]] 
            classifier.append([x_c, distance_to_append, y_c])

            support_array.append(get_elements_by_indexes(R, support_positions))

            x_c = R[support_positions[-1]]
            y_c = L[support_positions[-1]]
            
            R = R[min(support_positions[-1]+1, len(R)-1):]
            L = L[min(support_positions[-1]+1, len(L)-1):]

        support[opposite_label] = support_array

    cardinalities_per_label = [0] * len(labels)
    scenarios_per_label = [0] * len(labels)
    for i in range(len(labels)):
        cardinalities_per_label[i] = len(support[i])
        scenarios_per_label[i] = number_of_scenarios_with_given_label(scenarios, labels[i])

    return classifier, cardinalities_per_label, scenarios_per_label


def column(matrix, i):
    return [row[i] for row in matrix]


def calculate_distances(R, x_c):
    if len(R) == len(x_c) and all(isinstance(ele, list) for ele in R): # R contains the last x
        distance = 0
        for i in range(len(R)):
            distance += (x_c[i] - R[i]) ** 2
        return [math.sqrt(distance)], [0]

    distances = []
    for i in range(len(R)):
        distance = 0
        for j in range(len(R[i])):
            distance += (x_c[j] - R[i][j]) ** 2
        distances.append([math.sqrt(distance), i])

    distances.sort() # it automatically sorts by the first values of matrix
    return [row[0] for row in distances], [row[1] for row in distances]


def order_based_on_indexes(array, indexes):
    if indexes == [0]: # we have the last x
        return array

    new_array = []
    for index in indexes:
        new_array.append(array[index])
    return new_array


def search_indexes_by_label(array, label, labels):
    if len(array) == 1: # We have the last x
        if array[0] == label:
            return array
        return []

    new_array = []
    for i in range(len(array)):
        if array[i] == label:
            new_array.append(i)
    return new_array


def get_elements_by_indexes(array, indexes):
    new_array = []
    for index in indexes:
        new_array.append(array[index])
    return new_array


def number_of_scenarios_with_given_label(array, label):
    count = 0
    for element in array:
        if element[1] == label:
            count += 1
    return count

