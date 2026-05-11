# src/two_opt.py
import numpy as np


def _get_entry_exit(curve, rev):
    if rev:
        return np.array(curve["end"]), np.array(curve["start"])
    else:
        return np.array(curve["start"]), np.array(curve["end"])


def two_opt_improve(curves, ordered, reversals, max_passes=10):
    """
    2-opt post-processing to reduce total jump distance.

    Args:
        curves (list[dict])   : Original curve list.
        ordered (list[dict])  : Greedy-sorted curves.
        reversals (list[bool]): Reversal flags from greedy sort.
        max_passes (int)      : Maximum improvement passes.

    Returns:
        tuple: (improved ordered list, improved reversals, total jump distance)
    """
    n = len(ordered)
    seqs = list(ordered)
    revs = list(reversals)
    improved = True
    passes = 0

    while improved and passes < max_passes:
        improved = False
        passes += 1

        for i in range(n - 1):
            for j in range(i + 2, n):
                _, exit_i   = _get_entry_exit(seqs[i],     revs[i])
                entry_i1, _ = _get_entry_exit(seqs[i + 1], revs[i + 1])
                _, exit_j   = _get_entry_exit(seqs[j],     revs[j])

                cost_before = np.linalg.norm(exit_i - entry_i1)
                if j + 1 < n:
                    entry_j1, _ = _get_entry_exit(seqs[j + 1], revs[j + 1])
                    cost_before += np.linalg.norm(exit_j - entry_j1)

                cost_after = np.linalg.norm(exit_i - exit_j)
                if j + 1 < n:
                    cost_after += np.linalg.norm(entry_i1 - entry_j1)

                if cost_after < cost_before - 1e-6:
                    seqs[i + 1:j + 1] = seqs[i + 1:j + 1][::-1]
                    revs[i + 1:j + 1] = [not r for r in revs[i + 1:j + 1][::-1]]
                    improved = True

    # Recalculate total jump
    total_jump = 0.0
    for i in range(n - 1):
        _, exit_pt  = _get_entry_exit(seqs[i],     revs[i])
        entry_pt, _ = _get_entry_exit(seqs[i + 1], revs[i + 1])
        total_jump += np.linalg.norm(exit_pt - entry_pt)

    return seqs, revs, total_jump