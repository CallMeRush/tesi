from utility import test, draw
from numpy import random

def simple_hand_example():
    s_train = [
            [[0, 0], 1],
            [[2, 2], 0],
            [[3, 3], 1],
            [[4, 4], 1]]

    x_test = [[1, 1], [2, 2], [5, 5]]

    y_true = [1, 0, 1]

    return s_train, x_test, y_true


def generate_random_points(size, n_train, n_test, same_train_test = False):
    x_train = random.rand(n_train, size)
    for i in range(len(x_train)):
        for j in range(len(x_train[0])):
            x_train[i][j] -= 0.5

    y_train = []
    for i in range(len(x_train)):
        if sum(x_train[i]) > 0:
            y_train.append(1)
        else:
            y_train.append(0)

    scenarioes = []
    for i in range(len(x_train)):
        scenarioes.append([x_train[i], y_train[i]])

    x_test = random.rand(n_test, size)
    for i in range(len(x_test)):
        for j in range(len(x_test[0])):
            x_test[i][j] -= 0.5
    
    if same_train_test:
        x_test = x_train

    y_true = []
    for i in range(len(x_test)):
        if sum(x_test[i]) > 0:
            y_true.append(1)
        else:
            y_true.append(0)

    return scenarioes, x_test, y_true


if __name__ == "__main__":
    #[s_train, x_test, y_true] = simple_hand_example()
    [s_train, x_test, y_true] = generate_random_points(2, 20, 100)

    classifier = test(s_train, x_test, y_true, beta = 0.005)

    draw(classifier, [row[0] for row in s_train], x_test)

