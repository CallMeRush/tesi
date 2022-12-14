import math
from numpy import linalg as LA

def use_gem_balls(classifier, x):
    n = len(x)
    d = len(x[0])
    
    y = [-1] * n

    for i in range(n):
        found = False
        j = 0
        while not found:
            if LA.norm(x[i] - classifier[j][0]) < classifier[j][1]:
                found = True
                y[i] = classifier[j][2]
            else:
                j += 1

    return y

