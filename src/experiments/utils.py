from matplotlib import pyplot as plt
import numpy as np
import scipy

def pad_traces(traces):
    max_len = max(len(t) for t in traces)
    padded = []
    for trace in traces:
        if len(trace) < max_len:
            padding = [trace[-1]] * (max_len - len(trace))
            trace = trace + padding
        padded.append(trace)
    return np.array(padded)  # shape: (runs, max_len)

def run_balance_experiments(strategy_fn, runs: int = 1000, **kwargs):
    traces = [strategy_fn(**kwargs) for _ in range(runs)]
    return pad_traces(traces)

def compute_mean_and_ci(data: np.ndarray):
    mean = np.mean(data, axis=0)
    sem = scipy.stats.sem(data, axis=0)
    ci = scipy.stats.t.interval(0.95, len(data)-1, loc=mean, scale=sem)
    return mean, ci

def analyze_gain_thresholds(traces: np.ndarray, starting_amount: float, thresholds=None):
    if thresholds is None:
        thresholds = list(range(5, 105, 5))  # 5% to 100%
    thresholds_float = [starting_amount * (1 + pct / 100) for pct in thresholds]
    result = {pct: 0 for pct in thresholds}

    for run in traces:
        for pct, target in zip(thresholds, thresholds_float):
            if np.any(np.array(run) >= target):
                result[pct] += 1

    return result

# === Plotting ===
def plot_balance_over_time(ax, mean, ci, label: str):
    x = np.arange(len(mean))
    ax.plot(x, mean, label=label)
    ax.fill_between(x, ci[0], ci[1], alpha=0.2)

def plot_gain_thresholds(ax, threshold_counts: dict, total_runs: int, label: str):
    thresholds = sorted(threshold_counts.keys())
    values = [100 * threshold_counts[t] / total_runs for t in thresholds]
    ax.plot(thresholds, values, marker='o', label=label)

def plot_gain_thresholds_line(ax, thresholds_dict: dict, total_runs: int):
    """
    Plots gain threshold achievements as lines for multiple strategies or configurations.

    Args:
        ax: The matplotlib axis to plot on.
        thresholds_dict: A dict of label -> threshold_counts dicts.
                         Example:
                         {
                             'strat1 $10': {5: 1000, 10: 850, 15: 700, ...},
                             'strat2 $10': {5: 1100, 10: 900, 15: 750, ...},
                             ...
                         }
        total_runs: The number of simulation runs for each.
    """
    # Determine all thresholds across all strategies
    all_thresholds = sorted(set(
        t for d in thresholds_dict.values() for t in d.keys()
    ))

    for label, threshold_counts in thresholds_dict.items():
        percentages = [100 * threshold_counts.get(t, 0) / total_runs for t in all_thresholds]
        ax.plot(all_thresholds, percentages, marker='o', label=label)

    ax.set_xlabel("Gain Threshold (%)")
    ax.set_ylabel("Runs Reaching Threshold (%)")
    ax.set_title("Percentage of Runs Reaching Gain Thresholds")
    ax.grid(True, linestyle='--', alpha=0.5)
    ax.legend()

def plot_thresholds_per_amount(thresholds_dict, strategies, start_amounts, total_runs):
    for amt in start_amounts:
        fig, ax = plt.subplots(figsize=(10, 6))
        subset = {
            strat: thresholds_dict[strat][amt]
            for strat in strategies
            if amt in thresholds_dict[strat]
        }
        plot_gain_thresholds_line(ax, subset, total_runs=total_runs)
        ax.set_title(f"Gain Threshold Reach Rate – Starting Amount ${amt}")
        ax.set_xlabel("Gain Threshold (%)")
        ax.set_ylabel("Runs Reaching Threshold (%)")
        ax.grid(True, linestyle='--', alpha=0.5)
        ax.legend()
        plt.tight_layout()
        plt.show()