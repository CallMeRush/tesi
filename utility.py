from GEM.train_gem_balls import train_gem_balls
from GEM.validate_gem_balls import validate_gem_balls
from GEM.use_gem_balls import use_gem_balls
import math
from numpy import random
import matplotlib.pyplot as plt


def test(s_train, x_test, y_true, beta = 0.05):
    [classifier, card, num] = train_gem_balls(s_train)
    
    LOOFalseNegative=card[1]/num[1]
    LOOFalsePositive=card[0]/num[0]

    [GuaranteedFalseNegativeRate, GuaranteedFalsePositiveRate] = validate_gem_balls(card, num, [beta, beta])
    
    print("GuaranteedFalseNegativeRate: " + str(GuaranteedFalseNegativeRate))
    print("GuaranteedFalsePositiveRate: " + str(GuaranteedFalsePositiveRate))

    y_test = use_gem_balls(classifier, x_test)

    x_train = [row[0] for row in s_train]

    FalseNegativeRateOnNewData = 0
    FalsePositiveRateOnNewData = 0
    true = 0
    false = 0
    for i in range(len(y_test)):
        if y_true[i] == 1:
            true += 1
        if y_true[i] == 0:
            false += 1
        if y_true[i] == 1 and y_test[i] == 0:
            #print("true 1 dato 0: " + str(x_test[i]))
            FalseNegativeRateOnNewData += 1
        if y_true[i] == 0 and y_test[i] == 1:
            #print("true 0 dato 1: " + str(x_test[i]))
            FalsePositiveRateOnNewData += 1

    FalsePositiveRateOnNewData /= false
    FalseNegativeRateOnNewData /= true
    print("FalsePositiveRateOnNewData: " + str(FalsePositiveRateOnNewData))
    print("FalseNegativeRateOnNewData: " + str(FalseNegativeRateOnNewData))

    return classifier


def draw(classifier, x_train, x_test):
    fig, ax = plt.subplots()

    circles = []
    order = 0
    for elem in reversed(classifier):
        color = 'w'
        if elem[-1] == 0:
            color = 'r'
        else:
            color = 'y'

        radius = elem[1]
        if radius == math.inf:
            radius = 2

        circle = plt.Circle(elem[0], radius, color = color, ec = 'black')
        ax.add_patch(circle)

        order += 1

    ax.set_aspect('equal', adjustable='datalim')

    color = 'black'
    for elem in x_train:
        plt.plot(elem[0], elem[1], "x", color = color)

    color = 'white'
    for elem in x_test:
        plt.plot(elem[0], elem[1], "+", color = color)

    plt.show()


