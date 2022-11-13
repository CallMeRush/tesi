from scipy.stats import beta

def validate(card, num_scenarioes, beta_values):
    
    # Validate input
    for i in range(len(card)):
        if card[i] < 0 or card[i] > num_scenarioes[i] + 1:
            print("ERROR: wrong input.")
            return None, None

    errors = []
    for i in range(len(card)):
        if card[i] == 0:
            errors.append(0)
        elif card[i] == num_scenarioes[i] + 1:
            errors.append(1)
        else:
            errors.append(beta.ppf(1 - beta_values[i] / num_scenarioes[i], card[i], num_scenarioes[i] - card[i] + 1))

    return errors

