---
title: "2024Osaba Solving-a-real-world-package-delivery-routing-problem-using-quantum-annealers"
author: "Mikhail Lukianov"
date: "Devember 7, 2025"
---

# Context Summary (for other chats)

I’m implementing a **probabilistic optimization engine** based on **p-bits** (stochastic binary units) that operate like a classical, tunable analogue of quantum annealing. My backend already includes a generic BQM/QUBO sampler using Gibbs/Metropolis updates on p-bits, capable of solving arbitrary quadratic Hamiltonians.

Now I’m applying this backend to a **real-world delivery routing problem** inspired by the Q4RPD (“Quantum for Real Package Delivery”) framework. The goal is to compute efficient delivery routes that respect operational constraints while handling realistic features: heterogeneous trucks, weight/dimension limits, deadlines for priority deliveries (TP items), and maximum driver working hours.

The full routing task is decomposed into an iterative sequence of **Single Routing Problems (SRPs)**. Each SRP computes one **route or sub-route** for a given truck using a **node-based encoding** with binary decision variables $x_{i,p}$, indicating whether delivery $i$ is visited at position $p$ in the sequence. The mathematical structure includes:

- **Objective 1:** minimize total travel distance
- **Objective 2:** schedule the destination TP point as late as possible (maximize intermediate deliveries)
  Combined via weighted sum.

SRP is constrained by seven real-world rules:

1. A delivery appears at most once.
2. Each position is assigned to at most one delivery.
3. Delivery sequence must be contiguous (no internal gaps).
4. Destination must appear exactly once.
5. Total route time ≤ allowed duration.
6. Total weight ≤ truck capacity.
7. Total volume ≤ truck capacity.

These objectives and constraints are encoded as a **QUBO energy function**, which my p-bit solver minimizes. Each SRP thus becomes a probabilistic search over a structured binary space.

The outer algorithm (**Q4RPD**) orchestrates multiple SRPs, selecting trucks, determining whether to compute a full route or a sub-route (Depot→TP, TP→TP, TP→Depot, or Regular), updating remaining deliveries, and concatenating partial routes until all deliveries are assigned.

In short:

- **Backend:** custom p-bit stochastic Ising/QUBO solver.
- **Task:** implement a full routing system by expressing each sub-routing decision as a QUBO.
- **Goal:** reproduce the logic of Q4RPD, but powered entirely by my own probabilistic hardware-inspired solver.

---

# Problem Definition (Lossless + Compact)

We solve a **2-dimensional, heterogeneous package-delivery routing problem with priorities (2DH-PDP)**.
Given deliveries $P$, a depot, and both **owned** and **rented** trucks, we construct depot→deliveries→depot routes minimizing:

- total travel distance,
- rental-truck fees.

A **route** is the trajectory of a single truck serving a subset of deliveries.

## Constraints

- **R1 - 2D Capacity:**

  $$
  \sum_{i\in\text{route}} w_i \le W_v,
  \qquad
  \sum_{i\in\text{route}} d_i \le D_v.
  $$

- **R2 - Priority deadlines:**

  $$
  t_{\text{arrival}}(i) \le t_i .
  $$

- **R3 - Daily duration:**

  $$
  \text{duration(route)} \le T_{\text{workday}}.
  $$

Distance and travel time share the same numeric value.

## Preferences (Lexicographic)

1. **P1:** Each truck runs at most one route per day:

   $$
   r_v \le 1 .
   $$

2. **P2:** Prefer owned trucks over rentals.

3. **P3:** Prefer using fewer total trucks.

---

# Solving Scheme

The algorithm constructs **one trajectory at a time**, using **sub-routes** where necessary to satisfy TP deadlines.

## Sub-route types

- **Depot→TP**
- **TP→TP**
- **TP→Depot**
- **Regular route (Depot→Depot)**

## Each trajectory is solved as a **Single Routing Problem (SRP)** via a **Constrained Quadratic Model (CQM)**.

# Initialization

## Vehicle ordering

Owned trucks sorted by capacity, then rented trucks sorted by capacity (enforces $P2$, $P3$).

## Delivery ordering

TP deliveries are dequeued early (planning priority, not delivery priority).

## Loop start

Initialize pending deliveries and enter the iterative procedure.

---

# Iterative Construction (S1 → S2 → S3)

## S1 - Select Scenario and Parameters

Choose the first truck in the ordered list. Its state (depot or mid-route) and the presence of remaining TP deliveries determine one scenario:

- TP→TP
- TP→Depot
- Depot→TP
- Regular route

### Upper-bound duration $rt$

- **TP→TP:**

  $$
  rt = t_{\text{TP-destination}} - t_{\text{elapsed-from-depot}} .
  $$

- **TP→Depot:**

  $$
  rt = T_{\text{workday}} - t_{\text{elapsed-from-depot}} .
  $$

- **Depot→TP:**

  $$
  rt = t_{\text{TP-destination}} .
  $$

- **Regular route:**

  $$
  rt = T_{\text{workday}} .
  $$

### Capacity update

If partial payload already assigned:

$$
W \leftarrow W - \sum w_i ,
\qquad
D \leftarrow D - \sum d_i .
$$

---

# Single Routing Problem (SRP)

An SRP computes exactly one trajectory (a full route or sub-route).

## Parameters

- $rt$: allowed duration
- $W, D$: remaining capacity
- $P$: pending deliveries
- $M = |P|$
- $w_i, d_i$: weight and volume
- $t_i$: deadline
- $c_{i,j}$, $d_{i,j}$: travel time and distance (numerically equal)

## Variables (node-based encoding)

Binary variables:

$$
x_{i,p} =
\begin{cases}
1 & \text{if delivery } i \text{ is visited at position } p, \\
0 & \text{otherwise},
\end{cases}
\qquad
i \in \{0,\dots,M\},\; p \in \{0,\dots,M\}.
$$

Location index $i=0$ denotes the origin.

The route encoding is:

$$
X = {X_0,\ldots,X_M},
\qquad
X_i = {x_{i,0},\ldots,x_{i,M}}.
$$

Initialization:

- $x_{0,0} = 1$
- Destination variables are included but not position-fixed.

---

# SRP Objectives

Weights: $\omega_1 = 1$, $\omega_2 = 2$.

## Objective $o_1$: minimize route distance

$$
o_1 =
\sum_{p=0}^{M-1}
\sum_{i=0}^{M}
\sum_{j=0}^{M}
d_{i,j}, x_{i,p}, x_{j,p+1},
\qquad i\neq j.
$$

## Objective $o_2$: place destination as late as possible

Destination index is $1$:

$$
o_2 =
\sum_{p=0}^{M}
\left(*x_{1,p} *
\sum_{p'=p}^{M} x_{1,p'}
\right).
$$

## Total objective

$$
\min \big(\omega_1, o_1 + \omega_2, o_2 \big).
$$

---

# SRP Constraints

## Delivery-consistency

$$
\sum_{p=0}^{M} x_{i,p} \le 1
\qquad \forall i\in{0,\ldots,M}.
$$

## Position-consistency

$$
\sum_{i=0}^{M} x_{i,p} \le 1
\qquad \forall p\in{0,\ldots,M}.
$$

## Destination-inclusion

$$
\sum_{p=0}^{M} x_{1,p} = 1 .
$$

## Time-restriction

$$
\sum_{p=0}^{M-1}
\sum_{i=0}^{M}
\sum_{j=0}^{M}
c_{i,j}, x_{i,p}, x_{j,p+1}
\le rt,
\qquad i\neq j.
$$

## Weight-restriction

$$
\sum_{i=0}^{M}
w_i
\sum_{p=0}^{M} x_{i,p}
\le W .
$$

## Dimension-restriction

$$
\sum_{i=0}^{M}
d_i
\sum_{p=0}^{M} x_{i,p}
\le D .
$$

---

# S2 - Solve via LeapCQMHybrid

A CQM instance is submitted to D-Wave’s hybrid solver.
Quantum queries (Advantage_system6.4) guide classical heuristics.
Internal details and qubit requirements are proprietary.

# S3 - Assemble Solution

- Append the new sub-route to the truck’s ongoing trajectory.
- If the truck returns to depot, its route is complete and it is removed from the list.
- Remove all served deliveries from the pending set.

Repeat until no deliveries remain.
