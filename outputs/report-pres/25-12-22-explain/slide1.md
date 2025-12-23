## Slide 1 — _Problem context: where classical methods hit limits_

### Title (active)

**Why stochastic optimization hits practical limits**

---

### Core factual bullets

Got it — short, explicit, and with **arbitrage clearly named**. Here is the corrected **4-bullet version**, slide-ready:

- **Many NP-hard and combinatorial optimization problems scale exponentially**
  (e.g. Traveling Salesman Problem, Ising/QUBO, **circular arbitrage in directed graphs**)

- **Exact methods become infeasible beyond small problem sizes**
  TSP exact complexity **O(n²·2ⁿ)** → practical limit **~20–25 nodes** on a single machine

- **Practical solvers rely on stochastic exploration**
  (local search, simulated annealing, tabu, genetic methods, **probabilistic path/cycle selection in arbitrage**)

- **Runtime is dominated by repeated probabilistic decisions**
  Thousands–millions of biased samples per run → **sampling latency dominates arithmetic**

## This keeps it factual, compact, and ties directly to both of your demo problem classes.

### Concrete example (TSP, PM-friendly)

**• Example: TSP (20–30 nodes)**

- Exact solvers: already infeasible or borderline
- Heuristics: feasible, but **solution quality and speed depend on fast randomness**

This is accurate and defensible:
– exact solvers ≈ dead by ~25
– heuristics work, but randomness quality & latency matter

---

### Optional small right-side callout (one box)

> **Observation**
> As problem size grows, optimization time is dominated by stochastic sampling, not arithmetic.
