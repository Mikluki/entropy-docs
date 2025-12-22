# Portfolio Optimization with Physical P-Bit Hardware: A Demonstration of Physical Randomness for Combinatorial Optimization

## Abstract

This demonstration showcases the application of physically fabricated probabilistic bits (p-bits) based on Nb-nanowires for solving practical combinatorial optimization problems. Specifically, we address the portfolio optimization problem --- a challenging task in financial engineering that requires selecting a subset of assets from a larger universe to maximize returns while controlling risk. This work serves several key purposes:

1. **Validation of Physical Randomness**: We demonstrate that our fabricated Nb-nanowire devices function as true p-bits with genuine physical randomness, a significant achievement in unconventional computing hardware.

2. **Practical Application to Optimization**: We show that these physical p-bits can effectively solve real-world constrained optimization problems when integrated with a feedback-based control algorithm.

3. **Performance Benchmarking**: We compare our p-bit-based approach against classical optimization methods like simulated annealing, demonstrating the potential advantages of physically-embodied randomness for combinatorial optimization.

## The Optimization Problem

### Complex Solution Landscapes and Local Minima

The optimization problems we target are characterized by extremely complex solution landscapes littered with numerous local minima. In these scenarios, the primary challenge is not finding the global optimum --- which may be computationally intractable --- but rather finding a sufficiently good solution quickly and reliably.

Portfolio optimization belongs to a broader class of such challenging combinatorial problems that includes:

- Energy grid optimization
- Traveling salesman problem
- Nurse/staff scheduling problems
- Vehicle routing

These problems share a common trait: as problem size increases, the solution space grows exponentially, and traditional algorithms often become trapped in suboptimal solutions. Physical randomness offers a potential advantage by enabling more effective exploration of this complex landscape, potentially escaping local minima more efficiently than pseudo-random approaches.

### Portfolio Optimization as QUBO

The portfolio optimization problem is formulated as a Quadratic Unconstrained Binary Optimization (QUBO) problem. We aim to select a subset of stocks from a universe of potential assets, subject to budget constraints, to maximize expected returns while minimizing risk.

Mathematically, this is expressed as:

$$\min_{\mathbf{x}} \mathbf{x}^T Q \mathbf{x}$$

where:

- $\mathbf{x}$ is a binary vector representing asset selection (1 if selected, 0 if not)
- $Q$ is a matrix encoding both the objective function and constraints

The QUBO matrix $Q$ incorporates:

1. **Expected Returns** (diagonal terms): The expected annual return of each asset
2. **Risk Factors** (diagonal terms): The variance of each asset's returns
3. **Correlations** (off-diagonal terms): How assets move in relation to each other
4. **Budget Constraint** (encoded in the structure): Ensuring exactly $K$ assets are selected

The complete objective function balances:

- Maximizing portfolio return
- Minimizing portfolio variance
- Minimizing correlation between selected assets
- Strictly enforcing the budget constraint

### Why This Problem is Significant

Portfolio optimization with binary selection is:

1. **NP-Hard**: Finding the optimal solution becomes computationally intractable as the number of assets increases
2. **Practically Relevant**: It represents a real financial problem that investors face
3. **Constraint-Bound**: The budget constraint adds complexity that challenges optimization algorithms
4. **Multi-Objective**: It requires balancing competing goals (return vs. risk)

## The P-Bit Approach

Our approach leverages physical p-bits with a novel feedback mechanism:

1. We map the portfolio optimization problem to an Ising model compatible with our p-bit hardware
2. We implement a dynamic voltage control system that modulates the probability of each p-bit based on optimization performance
3. The system explores the solution space through physical randomness while learning to exploit promising regions

The true physical randomness of our Nb-nanowire p-bits may provide fundamental advantages for navigating complex solution landscapes compared to traditional algorithms that rely on pseudo-randomness. This is particularly relevant for problems with many local minima, where the quality of randomness can significantly impact the ability to escape suboptimal solutions.

This demonstration showcases how true physical randomness, when properly harnessed with feedback control, can effectively solve complex optimization problems that are relevant to real-world applications.
