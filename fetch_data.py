import yfinance as yf

def get_scenarioes(stock, time_period, time_after, start, end):
    df = yf.download(stock, start = start, end = end, interval = "1m")

    open_values = df['Open'].to_numpy()

    scenarioes_list = []

    for i in range(len(time_after)):
        scenarioes = []
        for j in range(len(df) - (time_period + time_after[i])):
            relative_values = open_values[j:j+time_period+time_after[i]] / open_values[j + time_period-1]
            y = 0
            if relative_values[time_period-1] < relative_values[-1]:
                y = 1
            else:
                y = 0
            scenarioes.append([relative_values, y])
        scenarioes_list.append(scenarioes)

    return scenarioes_list

