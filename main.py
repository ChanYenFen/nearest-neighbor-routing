# main.py
from src.generate import load_json, generate_random_curves, generate_grid_curves
from src.greedy   import greedy_sort
from src.two_opt  import two_opt_improve
from src.metrics  import measure


def run(curves, label):
    n = len(curves)

    (ordered_g, rev_g, jump_g), t_g = measure(greedy_sort, curves)
    (ordered_2, rev_2, jump_2), t_2 = measure(two_opt_improve, curves, ordered_g, rev_g)

    improvement = (jump_g - jump_2) / jump_g * 100

    print(f"\n{'='*45}")
    print(f"  {label}  (n={n})")
    print(f"{'='*45}")
    print(f"  {'Algorithm':<20} {'Jump':>8}  {'Time':>8}")
    print(f"  {'-'*38}")
    print(f"  {'Greedy':<20} {jump_g:>8.2f}  {t_g:>7.4f}s")
    print(f"  {'Greedy + 2-opt':<20} {jump_2:>8.2f}  {t_2:>7.4f}s")
    print(f"  {'-'*38}")
    print(f"  Improvement: {improvement:.1f}%")


if __name__ == "__main__":
    # Fixed JSON files
    run(load_json("examples/random_curves.json"), "Random Curves")
    run(load_json("examples/grid_curves.json"),   "Grid Curves")

    # Scale comparison
    print("\n\n--- Scale Comparison (Random) ---")
    for n in [10, 100, 500, 1000]:
        curves = generate_random_curves(n=n)
        run(curves, f"Random")