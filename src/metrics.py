# src/metrics.py
import time
import numpy as np


def measure(func, *args, **kwargs):
    """
    Measure execution time of a function.

    Returns:
        tuple: (result, elapsed_seconds)
    """
    start = time.perf_counter()
    result = func(*args, **kwargs)
    elapsed = time.perf_counter() - start
    return result, elapsed


def total_jump(ordered, reversals):
    """Recalculate total jump distance from ordered curves."""
    total = 0.0
    for i in range(len(ordered) - 1):
        exit_pt  = np.array(ordered[i]["start"]     if reversals[i]     else ordered[i]["end"])
        entry_pt = np.array(ordered[i+1]["end"]     if reversals[i+1]   else ordered[i+1]["start"])
        total += np.linalg.norm(exit_pt - entry_pt)
    return total