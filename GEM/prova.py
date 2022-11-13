from numpy import random
from scipy.stats import kstest, norm 
from train_gem_balls import train
from validate_gem_balls import validate
from use_gem_balls import use_gem_balls

n_train = 200
n_test = 10000

x_train = random.rand(n_train, 7)
for i in range(len(x_train)):
    for j in range(len(x_train[0])):
        x_train[i][j] -= 0.5

y_train = []
for i in range(len(x_train)):
    """a = kstest(x_train[i], norm.cdf).pvalue
    if a < 0.005:
        y_train.append(0)
    else:
        y_train.append(1)"""
    if sum(x_train[i]) > 0:
        y_train.append(1)
    else:
        y_train.append(0)

scenarios = []
for i in range(len(x_train)):
    scenarios.append([x_train[i], y_train[i]])

[classifier, card, num] = train(scenarios)

LOOFalseNegative=card[1]/num[1]
LOOFalsePositive=card[0]/num[0]

beta=0.05;
[GuaranteedFalseNegativeRate,GuaranteedFalsePositiveRate]= validate(card, num,[beta,beta])

print("GuaranteedFalseNegativeRate: " + str(GuaranteedFalseNegativeRate))
print("GuaranteedFalsePositiveRate: " + str(GuaranteedFalsePositiveRate))

x_test = random.rand(n_test, 7)
for i in range(len(x_test)):
    for j in range(len(x_test[0])):
        x_test[i][j] -= 0.5

y_test = use_gem_balls(classifier, x_test)

y_true = []
for i in range(len(x_test)):
    if sum(x_test[i]) > 0:
        y_true.append(1)
    else:
        y_true.append(0)

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
        FalseNegativeRateOnNewData += 1
    if y_true[i] == 0 and y_test[i] == 1:
        FalsePositiveRateOnNewData += 1

FalsePositiveRateOnNewData /= false
FalseNegativeRateOnNewData /= true
print("FalsePositiveRateOnNewData: " + str(FalsePositiveRateOnNewData))
print("FalseNegativeRateOnNewData: " + str(FalseNegativeRateOnNewData))

