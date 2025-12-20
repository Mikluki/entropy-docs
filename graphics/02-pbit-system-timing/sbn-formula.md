## Formula Summary

The SBN formula converts continuous input current into binary output through a **temperature-controlled stochastic threshold**.

The state of SBN is updated according to the equation:

$$\sigma = \text{sign}(\tanh(\beta I) - r)$$

where:

- $I$ --- input current
- $\beta$ --- the inverse temperature
- $r$ --- a uniform random number from [-1, 1]

### Mathematical Connection

The uniform random number **implements** the probability:

$$P(\sigma_i = +1) = P(\tanh(\beta I_i) > r) = P(r < \tanh(\beta I_i))$$

Since $r \sim \text{Uniform}[-1,1]$:
$$P(r < \tanh(\beta I_i)) = \frac{\tanh(\beta I_i) - (-1)}{1 - (-1)} = \frac{1 + \tanh(\beta I_i)}{2}$$

### Sampling Implementation (How we achieve it)

$$\sigma_i = \text{sign}(\tanh(\beta I_i) - r)$$

**Purpose**: **Sampling mechanism** to achieve that probability

- Uniform random number $r$ is the **tool** that converts probability → actual binary response
- Each time we run it, we get a concrete +1 or -1

### Uniform random number

> **Maps** from probability space to response space"

- **Probability space**: $P(\sigma_i = +1) \in [0,1]$ (continuous)
- **Response space**: $\sigma_i \in \{-1, +1\}$ (discrete binary)

1. Stochastic SBN (Sampling Implementation)

   $$\sigma_i = \text{sign}(\tanh(\beta I_i) - r)$$

1. Deterministic SBN (No randomness)

   $$\sigma_i = \text{sign}(\tanh(\beta I_i))$$

### Beta as "Smearing" Parameter

Large $\beta$ (Sharp/Less Smeared)

- $\beta \to \infty$: $\tanh(\beta I_i) \to \text{step function}$
- Nearly deterministic: $P(\sigma_i = +1) \approx 0$ or $1$
- **Sharp transition** at $I_i = 0$

Small $\beta$ (Smooth/More Smeared)

- $\beta \to 0$: $\tanh(\beta I_i) \to 0$ (flat)
- Maximum randomness: $P(\sigma_i = +1) \approx 0.5$ for all $I_i$
- **Gradual transition** - heavily smeared

Moderate $\beta$ (Balanced)

- Sigmoid-like probability curve
- Smooth but responsive to input
