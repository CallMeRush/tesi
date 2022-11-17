from examples import generate_random_points
import timeit
from GEM.train_gem_balls import train_gem_balls
from GEM.old.train_gem_balls import train_old
from GEM.validate_gem_balls import validate_gem_balls
from GEM.use_gem_balls import use_gem_balls
from GEM.old.use_gem_balls import use_old

compare_accuracy = True
compare_speed = True

print("Initializing...\n")

[s_train, x_test, y_true] = generate_random_points(15, 2000, 10000)

if compare_accuracy or compare_speed:
    [classifier_old, card_old, num_old] = train_old(s_train)
    [classifier_numpy, card_numpy, num_numpy] = train_gem_balls(s_train)


if compare_accuracy:
    print("Compare accuracy:\n")

    beta = 0.005

    print("Old:")

    [GuaranteedFalseNegativeRate, GuaranteedFalsePositiveRate] = validate_gem_balls(card_old, num_old, [beta, beta])
    print("GuaranteedFalseNegativeRate: " + str(GuaranteedFalseNegativeRate))
    print("GuaranteedFalsePositiveRate: " + str(GuaranteedFalsePositiveRate))
    y_test = use_old(classifier_old, x_test)
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

    print("\nWith numpy:")

    [GuaranteedFalseNegativeRate, GuaranteedFalsePositiveRate] = validate_gem_balls(card_numpy, num_numpy, [beta, beta])
    print("GuaranteedFalseNegativeRate: " + str(GuaranteedFalseNegativeRate))
    print("GuaranteedFalsePositiveRate: " + str(GuaranteedFalsePositiveRate))
    y_test = use_gem_balls(classifier_numpy, x_test)
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

    print("\n")

if compare_speed:
    print("Compare speed:\n")
    
    time_old = timeit.timeit('train_old(s_train)', 'from GEM.old.train_gem_balls import train_old; from __main__ import s_train', number = 3)
    print("Time train old: " + str(time_old))
    time_numpy = timeit.timeit('train_gem_balls(s_train)', 'from GEM.train_gem_balls import train_gem_balls; from __main__ import s_train', number = 3)
    print("Time train numpy: " + str(time_numpy))

    print()

    time_old = timeit.timeit('use_old(classifier_old, x_test)', 'from GEM.old.use_gem_balls import use_old; from __main__ import classifier_old, x_test', number = 3)
    print("Time use old: " + str(time_old))
    time_numpy = timeit.timeit('use_gem_balls(classifier_numpy, x_test)', 'from GEM.use_gem_balls import use_gem_balls; from __main__ import classifier_numpy, x_test', number = 3)
    print("Time use numpy: " + str(time_numpy))

