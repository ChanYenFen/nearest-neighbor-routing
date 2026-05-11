# Nearest Neighbor Routing

Toolpath sequencing for 2D curve sets using Greedy Nearest-Neighbor and 2-opt optimization.

OOriginally developed to reduce non-cutting travel distance in 
high-precision fabrication workflows, where toolpath sequencing 
directly impacts cycle time and operational efficiency.

The underlying problem — ordering an unstructured set of segments 
to minimize total traversal cost — is a recurring pattern across 
manufacturing domains.

---

## Problem

Given an unordered set of line segments, find a traversal order that minimizes total jump distance —
the cumulative non-cutting travel between consecutive segments.

Each segment can be traversed in either direction, so the solver also determines optimal orientation per segment.

This problem appears in:
- CNC and laser cutting toolpath sequencing
- PCB drilling order optimization
- SMT pick-and-place routing
- Embroidery and robotic fabrication path planning
In production environments, a poorly sequenced toolpath directly increases cycle time,
machine wear, and energy consumption — without any change to the design itself.

---

## Approach

Two algorithms are compared against the same input data:

**1. Greedy Nearest-Neighbor** `O(n log n)`  
At each step, select the closest unvisited endpoint using a KD-Tree index.
Fast and practical for large inputs, but locally optimal decisions can lead to globally suboptimal paths.

**2. Greedy + 2-opt** `O(n log n) + O(n²)`  
Apply 2-opt post-processing to the greedy result: iteratively reverse sub-sequences when doing so
reduces total jump distance. Accepts improvements until no further gain is found.

---

## Results

Tested on two synthetic datasets, each with n=100 segments:

**Random distribution** — segments placed uniformly at random across a 100×100 unit space:

| Algorithm      |  Jump Distance |    Time |
|----------------|---------------:|--------:|
| Greedy         |         646.34 | 0.0103s |
| Greedy + 2-opt |         470.57 | 0.6573s |
| **Improvement**|      **27.2%** |         |

**Grid distribution** — vertical scan lines with minor positional noise, simulating laser or CNC raster passes:

| Algorithm      |  Jump Distance |    Time |
|----------------|---------------:|--------:|
| Greedy         |         273.23 | 0.0045s |
| Greedy + 2-opt |         273.23 | 0.0930s |
| **Improvement**|       **0.0%** |         |

The grid result is expected: greedy performs near-optimally on structured inputs,
leaving no room for 2-opt to improve. This reflects real-world behavior where
algorithm selection should be input-aware.

---

## Scaling Behavior

Random distribution across increasing input sizes:

| n    |  Greedy Jump | Greedy Time | 2-opt Jump | 2-opt Time | Improvement |
|------|-------------:|------------:|-----------:|-----------:|------------:|
| 10   |       123.23 |     0.0010s |     123.23 |    0.0006s |        0.0% |
| 100  |       646.34 |     0.0063s |     470.57 |    0.4252s |       27.2% |
| 500  |      1426.19 |     0.0352s |    1124.60 |   19.7278s |       21.1% |
| 1000 |      2020.30 |     0.0663s |    1525.88 |   81.1446s |       24.5% |

2-opt delivers consistent 20–27% improvement on random inputs,
but the O(n²) overhead becomes a bottleneck beyond n=500.
For larger inputs, spatial partitioning or neighbor-limited 2-opt
would be the natural next step.

---

## Project Structure

nearest-neighbor-routing/
│
├── src/
│   ├── generate.py      # Synthetic dataset generation
│   ├── greedy.py        # Greedy nearest-neighbor with KD-Tree
│   ├── two_opt.py       # 2-opt post-processing
│   └── metrics.py       # Distance calculation and timing
│
├── examples/
│   ├── random_curves.json
│   └── grid_curves.json
│
├── main.py              # Benchmark runner
└── requirements.txt

---

## Requirements

numpy
scipy

---

## Notes

Segment orientation is handled explicitly: each segment can be reversed to minimize
the entry distance from the previous exit point. This doubles the effective search
space but is essential for correct results in practice.

Part of a broader computational geometry toolkit developed for manufacturing pipeline automation.