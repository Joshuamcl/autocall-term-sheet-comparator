def find_autocall_year(levels, barrier):
    for year, level in enumerate(levels[:4], start=1):
        if level >= barrier:
            return year
    return None

def evaluate_autocall(levels, nominal, coupon_rate, autocall_barrier, protection_barrier):
    maturity = 5
    autocall_year = find_autocall_year(levels, autocall_barrier)

    if autocall_year is not None:
        outcome = "autocall"
        duration = autocall_year
        redemption = nominal * (1 + coupon_rate * duration)
    else:
        duration = maturity
        final_level = levels[-1]

        if final_level >= 100:
            outcome = "protected"
            redemption = nominal * (1 + coupon_rate * maturity)
        elif final_level >= protection_barrier:
            outcome = "protected"
            redemption = nominal
        else:
            outcome = "capital_loss"
            redemption = nominal * final_level / 100

    total_return = redemption / nominal - 1
    annualized_return = (redemption / nominal) ** (1 / duration) - 1

    return {
        "autocall_year": autocall_year,
        "duration": duration,
        "redemption": redemption,
        "total_return": total_return,
        "annualized_return": annualized_return,
        "outcome": outcome
    }