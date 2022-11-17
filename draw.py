import matplotlib.pyplot as plt
import math

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

