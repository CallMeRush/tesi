from GEM.train_gem_balls import train
from GEM.validate_gem_balls import validate
from GEM.use_gem_balls import use_gem_balls
from fetch_data import get_scenarioes

time_period = 7
time_after = [1, 3, 10]

scenarioes_train = get_scenarioes('BTC-USD', time_period, time_after, '2022-11-01', '2022-11-07')
scenarioes_test = get_scenarioes('BTC-USD', time_period, time_after, '2022-11-08', '2022-11-09')

for i in range(len(time_after)):
    print("\n\n")

    current_train = scenarioes_train[i]
    current_test = scenarioes_test[i]    

    [classifier, card, num] = train(current_train)

    LOOFalseNegative=card[1]/num[1]
    LOOFalsePositive=card[0]/num[0]

    beta=0.05;
    [GuaranteedFalseNegativeRate,GuaranteedFalsePositiveRate]= validate(card, num,[beta,beta])

    if GuaranteedFalseNegativeRate != None:
        print("GuaranteedFalseNegativeRate: " + str(GuaranteedFalseNegativeRate))
    if GuaranteedFalsePositiveRate != None:
        print("GuaranteedFalsePositiveRate: " + str(GuaranteedFalsePositiveRate))

    y_test = use_gem_balls(classifier, [row[0] for row in current_test])

    y_true = [row[1] for row in current_test]

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

