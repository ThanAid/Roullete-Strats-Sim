from typing import List

from pyroullete.pyroullete import PyRoullete
from experiments.utils import plot_thresholds_per_amount, run_balance_experiments, compute_mean_and_ci, analyze_gain_thresholds

def strat1(starting_amount: float, init_bet: float = 0.2) -> List[float]:
    my_run = PyRoullete(credits=starting_amount)
    lose_streak = 0

    balance_trace = [starting_amount]
    while True:
        try:
            res = my_run.play(bet_info={
                "0": init_bet,  # Straight bet on 0
                "1": init_bet,  # Straight bet on 1
                "8": init_bet,  # Straight bet on 8
                "11": init_bet, # Straight bet on 11
                "16": init_bet, # Straight bet on 16
                "21": init_bet, # Straight bet on 21
                "31": init_bet, # Straight bet on 31
                "19": init_bet  # Straight bet on 19
            })
            if res.get('win'):
                lose_streak = 0
            else:
                lose_streak += 1
            
            if lose_streak == 3:
                # After 3 consecutive losses, double the bet
                init_bet *= 2
                lose_streak = 0
            
            balance_trace.append(res.get('balance'))
            # print(f"Bet: {res.get('bet_amount')} | Result: {res.get('result')} | Balance: {res.get('balance')}")

        except ValueError as e:
            # print("YOu ran out of credits")
            break
    return balance_trace

def strat2(starting_amount: float, init_bet: float = 0.2) -> List[float]:
    my_run = PyRoullete(credits=starting_amount)
    lose_streak = 0

    balance_trace = [starting_amount]
    while True:
        try:
            res = my_run.play(bet_info={
                "0": init_bet,  # Straight bet on 0
                "1": init_bet,  # Straight bet on 1
                "8": init_bet,  # Straight bet on 8
                "11": init_bet, # Straight bet on 11
                "16": init_bet, # Straight bet on 16
                "21": init_bet, # Straight bet on 21
                "31": init_bet, # Straight bet on 31
                "19": init_bet,  # Straight bet on 19
                "2": init_bet,  # Straight bet on 2
                "3": init_bet,  # Straight bet on 3
                "4": init_bet,  # Straight bet on 4
            })
            if res.get('win'):
                lose_streak = 0
            else:
                lose_streak += 1
            
            if lose_streak == 3:
                # After 3 consecutive losses, double the bet
                init_bet *= 2
                lose_streak = 0
            
            balance_trace.append(res.get('balance'))
            # print(f"Bet: {res.get('bet_amount')} | Result: {res.get('result')} | Balance: {res.get('balance')}")

        except ValueError as e:
            # print("YOu ran out of credits")
            break
    return balance_trace

def strat3(starting_amount: float, init_bet: float = 0.2) -> List[float]:
    my_run = PyRoullete(credits=starting_amount)
    lose_streak = 0

    balance_trace = [starting_amount]
    while True:
        try:
            res = my_run.play(bet_info={
                "0": init_bet,  # Straight bet on 0
                "1": init_bet  # Straight bet on 1
            })
            if res.get('win'):
                lose_streak = 0
            else:
                lose_streak += 1
            
            if lose_streak == 2:
                # After 3 consecutive losses, double the bet
                init_bet *= 2
                lose_streak = 0
            
            balance_trace.append(res.get('balance'))
            # print(f"Bet: {res.get('bet_amount')} | Result: {res.get('result')} | Balance: {res.get('balance')}")

        except ValueError as e:
            # print("YOu ran out of credits")
            break
    return balance_trace

def strat4(starting_amount: float, init_bet: float = 0.2) -> List[float]:
    my_run = PyRoullete(credits=starting_amount)
    lose_streak = 0

    balance_trace = [starting_amount]
    while True:
        try:
            res = my_run.play(bet_info={
                "0": init_bet,  # Straight bet on 0
                "1": init_bet,  # Straight bet on 1
                "8": init_bet,  # Straight bet on 8
                "11": init_bet, # Straight bet on 11
                "16": init_bet, # Straight bet on 16
                "21": init_bet, # Straight bet on 21
                "31": init_bet, # Straight bet on 31
                "19": init_bet  # Straight bet on 19
            })
            if res.get('win'):
                lose_streak = 0
            else:
                lose_streak += 1
            
            if lose_streak == 2:
                # After 2 consecutive losses, double the bet
                init_bet *= 2
                lose_streak = 0
            
            balance_trace.append(res.get('balance'))
            # print(f"Bet: {res.get('bet_amount')} | Result: {res.get('result')} | Balance: {res.get('balance')}")

        except ValueError as e:
            # print("YOu ran out of credits")
            break
    return balance_trace

def demo(starting_amount: float, init_bet: float = 0.2):
    my_run = PyRoullete(credits=starting_amount)
    balance_trace = [my_run.get_balance()]
    while True:
        try:
            res = my_run.play(bet_info={
                "0": init_bet,  # Straight bet on 0
                "1": init_bet,  # Straight bet on 1
                "8": init_bet,  # Straight bet on 8
                "11": init_bet, # Straight bet on 11
                "16": init_bet, # Straight bet on 16
                "21": init_bet, # Straight bet on 21
                "31": init_bet, # Straight bet on 31
                "19": init_bet  # Straight bet on 19
            })
            # print(f"Result: {res.get('result')} | Balance: {res.get('balance')}")
            balance_trace.append(res.get('balance'))
        except ValueError as e:
            # print("YOu ran out of credits")
            break
    return balance_trace


if __name__ == "__main__":
    # === Register your strategies here ===
    STRATEGIES = {
        "strat1": strat1,
        "strat2": strat2,
        "strat3": strat3,
        "strat4": strat4
    }

    start_amounts = [30, 50, 100, 200, 500, 1000]
    runs = 10000
    print(f"Running {runs} simulations...")

    # === Storage ===
    results = {name: {} for name in STRATEGIES}
    thresholds = {name: {} for name in STRATEGIES}

    # === Run Experiments ===
    for strat_name, strat_func in STRATEGIES.items():
        for amt in start_amounts:
            print(f"Running {strat_name} with starting_amount = {amt}")
            data = run_balance_experiments(strat_func, runs=runs, starting_amount=amt)
            results[strat_name][amt] = compute_mean_and_ci(data)
            thresholds[strat_name][amt] = analyze_gain_thresholds(data, starting_amount=amt)

    # === Plotting Results ===
    plot_thresholds_per_amount(
    thresholds_dict=thresholds,
    strategies=STRATEGIES.keys(),
    start_amounts=start_amounts,
    total_runs=runs
)