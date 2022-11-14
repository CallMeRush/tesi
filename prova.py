from GEM.train_gem_balls import train
from GEM.validate_gem_balls import validate
from GEM.use_gem_balls import use_gem_balls
from fetch_data import get_scenarioes

time_period = 25
time_after = [1, 2, 3, 5, 7, 10, 15, 25, 40, 60, 90]

scenarioes_train = get_scenarioes('BTC-USD', time_period, time_after, '2022-10-17', '2022-10-23')
scenarioes_test = get_scenarioes('BTC-USD', time_period, time_after, '2022-10-24', '2022-10-25')
#scenarioes_test = get_scenarioes('BTC-USD', time_period, time_after, '2022-11-08', '2022-11-09')

min1 = 10
min2 = 10
min_period1 = 0
min_period2 = 0
min_after1 = 0
min_after2 = 0

while time_period < 50:
    for i in range(len(time_after)):
        print("\n")
        print("Period: " + str(time_period) + " After: " + str(time_after[i]))

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
        for j in range(len(y_test)):
            if y_true[j] == 1:
                true += 1
            if y_true[j] == 0:
                false += 1
            if y_true[j] == 1 and y_test[j] == 0:
                FalseNegativeRateOnNewData += 1
            if y_true[j] == 0 and y_test[j] == 1:
                FalsePositiveRateOnNewData += 1

        FalsePositiveRateOnNewData /= false
        FalseNegativeRateOnNewData /= true
        print("FalsePositiveRateOnNewData: " + str(FalsePositiveRateOnNewData))
        print("FalseNegativeRateOnNewData: " + str(FalseNegativeRateOnNewData))

        min1 = min(FalsePositiveRateOnNewData, min1)
        if min1 == FalsePositiveRateOnNewData:
            min_period1 = time_period
            min_after1 = time_after[i]
        min2 = min(FalseNegativeRateOnNewData, min2)
        if min2 == FalseNegativeRateOnNewData:
            min_period2 = time_period
            min_after2 = time_after[i]
    
    time_period += 5

print(str(min1) + " " + str(min_period1) + " " + str(min_after1))
print(str(min2) + " " + str(min_period2) + " " + str(min_after2))
