## Slide 2 — **Algorithm → Stochastic compute → Hardware**

### Visual backbone (keep this)

**Optimization algorithm**
↓
**Stochastic decisions** (sampling, exploration)
↓
**Probabilistic bits (p-bits)**

---

### Concrete example (anchor the abstraction)

**Example: local search step (TSP / QUBO / arbitrage)**

- Propose a random move
  (swap two cities / flip a bit / extend a path)
- Accept or reject based on probability
  (energy difference, cost change, or gain)

You can show this as a tiny 2-step loop icon next to the arrow.

---

### Key message (tight, factual)

- **Algorithms remain unchanged**
  (same objective, same acceptance rules)

- **Only the stochastic decisions are accelerated**
  Random move generation and probabilistic acceptance

---

### Optional one-line clarifier (small text)

> Deterministic arithmetic stays in software; randomness and probability move to hardware.

---

### Why this works

- Shows _exactly_ where p-bits plug in
- Makes it obvious you’re not proposing a new solver
- Bridges cleanly to slide 4 (“this is why latency matters”)

---

### One-sentence narration (for you)

“In every heuristic, there’s a tight loop where we propose and accept random moves — we leave the algorithm alone and only accelerate that loop.”

If you want, next we can:

- Add a **tiny pseudocode snippet** version of this slide, or
- Make **slide 3** the conceptual intro to p-bits as hardware Ising variables.
