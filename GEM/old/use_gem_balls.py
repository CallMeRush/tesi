import math

def use_old(classifier, x):
    n = len(x)
    d = len(x[0])
    
    y = [-1] * n

    for i in range(n):
        found = False
        j = 0
        while not found:
            if norm(x[i], classifier[j][0]) < classifier[j][1]:
                found = True
                y[i] = classifier[j][2]
            else:
                j += 1

    return y


def norm(p1, p2):
    result = 0
    for i in range(len(p1)):
        result += (p1[i] - p2[i]) ** 2
    return math.sqrt(result)

