import numpy as np
import json

def generate_random_curves(n=100, seed=42):
    """
    Randomly distributed line segments.
    Each curve is defined by a start and end point.
    Order is intentionally shuffled to simulate worst-case input.
    """
    rng = np.random.default_rng(seed)
    
    curves = []
    for i in range(n):
        curves.append({
            "id": i,
            "start": rng.uniform(0, 100, 2).round(2).tolist(),
            "end":   rng.uniform(0, 100, 2).round(2).tolist()
        })
    
    # Shuffle to simulate unordered input
    indices = rng.permutation(n).tolist()
    curves = [curves[i] for i in indices]
    
    return curves

def generate_grid_curves(n=100, seed=42):
    """
    Grid-based scan lines simulating CNC or laser manufacturing toolpaths.
    Small positional noise added to simulate real-world imprecision.
    """
    rng = np.random.default_rng(seed)
    rows, cols = 10, 10
    
    curves = []
    for i in range(rows):
        for j in range(cols):
            x = j * 10 + rng.uniform(-0.5, 0.5)
            y_start = i * 10
            y_end   = i * 10 + 8
            curves.append({
                "id": i * cols + j,
                "start": [round(x, 2), round(y_start, 2)],
                "end":   [round(x, 2), round(y_end,   2)]
            })
    
    # Shuffle
    indices = rng.permutation(n).tolist()
    curves = [curves[i] for i in indices]
    
    return curves


def save_json(curves, filepath):
    with open(filepath, "w") as f:
        json.dump({"curves": curves}, f, indent=2)


def load_json(filepath):
    with open(filepath, "r") as f:
        return json.load(f)["curves"]