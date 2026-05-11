# src/greedy.py
import numpy as np
from scipy.spatial import KDTree


def compute_jump(pt_a, pt_b):
    return np.linalg.norm(pt_a - pt_b)


def greedy_sort(curves, start_pt=np.array([0.0, 0.0])):
    """
    Greedy nearest-neighbor sort using KDTree.
    
    Args:
        curves (list[dict]) : List of curves with 'start' and 'end' keys.
        start_pt (np.array) : Starting reference point.

    Returns:
        tuple: (ordered list of curves, list of reversal flags, total jump distance)
    """
    n = len(curves)

    # Build point array: points[i*2] = start, points[i*2+1] = end
    points = np.array([
        p for c in curves
        for p in [c["start"], c["end"]]
    ])

    tree = KDTree(points)
    used = set()

    # Find starting curve
    dists = np.linalg.norm(points - start_pt, axis=1)
    first_pt_id = int(np.argmin(dists))
    first_curve_id = first_pt_id // 2
    first_reversed = (first_pt_id % 2 == 1)

    ordered = [curves[first_curve_id]]
    reversals = [first_reversed]
    used.add(first_curve_id)

    last_pt = np.array(curves[first_curve_id]["start"] if first_reversed
                       else curves[first_curve_id]["end"])

    total_jump = 0.0

    # Greedy search
    while len(ordered) < n:
        # Query more neighbors until we find an unused curve
        k = 2
        while True:
            dists, ids = tree.query(last_pt, k=k)
            found = False
            for pt_id in ids:
                curve_id = pt_id // 2
                if curve_id in used:
                    continue
                # Found next curve
                reversed_flag = (pt_id % 2 == 1)
                c = curves[curve_id]
                entry = np.array(c["end"] if reversed_flag else c["start"])
                exit_pt = np.array(c["start"] if reversed_flag else c["end"])

                total_jump += compute_jump(last_pt, entry)
                ordered.append(c)
                reversals.append(reversed_flag)
                used.add(curve_id)
                last_pt = exit_pt
                found = True
                break
            if found:
                break
            k *= 2  # expand search if all neighbors are used

    return ordered, reversals, total_jump