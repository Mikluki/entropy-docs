---
title: "Documentation on pn-based True Random Number Generator"
author: "Mikhail Lukianov"
date: "November 5, 2025"
---

# Physical Basis of Breakdown Noise

## PN Junction Under Reverse Bias

When a p–n junction is reverse-biased, the depletion region widens and a strong electric field $E$ develops.
At moderate voltages, the reverse current is limited by thermally generated minority carriers.
However, beyond a certain critical field strength ($E_\text{crit} \sim 3\times10^5\text{–}10^6\ \text{V/cm}$ for silicon), the junction enters **breakdown**.

Depending on the doping level and field distribution, two main regimes exist:

| Regime                          | Dominant mechanism                | Typical junction doping                    | Typical voltage         |
| ------------------------------- | --------------------------------- | ------------------------------------------ | ----------------------- |
| **Avalanche breakdown**         | Impact ionization                 | Lightly doped ($<10^{17}\ \text{cm}^{-3}$) | $>6\text{–}8\ \text{V}$ |
| **Tunneling (Zener) breakdown** | Quantum tunneling through barrier | Heavily doped ($>10^{18}\ \text{cm}^{-3}$) | $<5\ \text{V}$          |

---

## Avalanche Breakdown and Noise Generation

In **avalanche breakdown**, a minority carrier accelerated by the field acquires enough kinetic energy to ionize atoms via impact, creating an **electron–hole pair**.
Each newly created carrier can in turn trigger further ionization events, leading to a **multiplication chain**.

Let $M$ be the avalanche multiplication factor:

$$
M = \frac{1}{1 - \int_0^W (\alpha_n + \alpha_p) dx},
$$

where $\alpha_n$ and $\alpha_p$ are the ionization coefficients for electrons and holes, and $W$ is the depletion width.

Because the ionization process is **stochastic**, the number of carriers produced per initiating event fluctuates strongly.
These fluctuations translate into **current noise** with a nearly flat (white) power spectral density up to hundreds of MHz.

The spectral density of avalanche noise current is approximately:

$$
S_I(f) \approx 2qI_\text{av} F(M),
$$

where $I_\text{av}$ is the average avalanche current, $q$ is the elementary charge, and $F(M)$ is the **excess noise factor** (typically $F(M) = kM + (1-k)(2 - 1/M)$, with $k$ the ratio of ionization coefficients).

At low currents, individual avalanches appear as discrete spikes — “clicks” — whose **arrival times are random** and obey a Poisson distribution.
This gives rise to _shot noise_–like statistics, making avalanche diodes effective physical entropy sources.

---

## Tunneling (Zener) Breakdown and Noise

In heavily doped junctions, the depletion region becomes extremely thin ($\sim 10\text{–}20\ \text{nm}$), and carriers can **quantum-tunnel** through the potential barrier even without impact ionization.

The tunneling current density is given approximately by

$$
J \propto E^2 \exp!\left(-\frac{B}{E}\right),
$$

where $E$ is the electric field and $B$ is a material constant depending on bandgap $E_g$ and effective masses.

Tunneling events are also **probabilistic** — each carrier crossing the barrier is an independent quantum event.
The resulting **tunneling shot noise** has spectral density:

$$
S_I(f) = 2qI_\text{tun},
$$

where $I_\text{tun}$ is the average tunneling current.
Since each tunneling event is uncorrelated, this noise is **white** up to the RC-limited bandwidth of the circuit.

---

## Comparison of Mechanisms

| Property               | Avalanche breakdown                            | Tunneling (Zener) breakdown  |
| ---------------------- | ---------------------------------------------- | ---------------------------- |
| Dominant physics       | Impact ionization                              | Quantum tunneling            |
| Doping level           | Low / medium                                   | High                         |
| Breakdown voltage      | 6–20 V                                         | 3–5 V                        |
| Noise character        | Burst-like, broad spectrum                     | Continuous, shot-like        |
| Temperature dependence | Strong                                         | Moderate                     |
| Practical use in TRNGs | Requires bias control, gives high entropy rate | Lower amplitude, very stable |

---

## Entropy Origin

Both mechanisms generate **microscopic, unpredictable fluctuations** originating in:

- **Carrier statistics** (quantum uncertainty in emission or collision timing)
- **Field inhomogeneities** (local microplasma initiation sites)
- **Thermal and phonon interactions**, modulating impact probabilities

Hence the noise current $i_n(t)$ can be modeled as:

$$
i_n(t) = \bar{I} + \delta i(t),
$$

with $\langle \delta i(t)\rangle = 0$ and

$$
\langle \delta i(t)\delta i(t+\tau) \rangle = \int_0^\infty S_I(f), e^{j2\pi f\tau},df.
$$

The randomness of $\delta i(t)$ is _fundamentally quantum_ and forms the **entropy source** of the hardware TRNG.

## References by Phenomenon

### Avalanche Breakdown - General Theory and Discovery

- **McKay, K.G.** (1954). "Avalanche Breakdown in Silicon," _Physical Review_, 94(4), 877-884.
- **Goetzberger, A.** (1964). "Avalanche Breakdown in Silicon," in _Festkörperprobleme 3 (Advances in Solid State Physics)_, vol. 3, Springer, Berlin. _(historic - comprehensive review)_
- **Miller, S.L.** (1955). "Avalanche Breakdown in Germanium," _Physical Review_, 99(4), 1234-1241. _(historic)_

### Avalanche Noise and Excess Noise Factor

- **McIntyre, R.J.** (1966). "Multiplication Noise in Uniform Avalanche Diodes," _IEEE Transactions on Electron Devices_, ED-13(1), 164-168.
- **van Vliet, K.M. and Rucker, L.M.** (1979). "Theory of Carrier Multiplication and Noise in Avalanche Devices—Part I: One-Carrier Processes," _IEEE Transactions on Electron Devices_, 26(5), 746-751.
- **van Vliet, K.M., Friedmann, A., and Rucker, L.M.** (1979). "Theory of Carrier Multiplication and Noise in Avalanche Devices—Part II: Two-Carrier Processes," _IEEE Transactions on Electron Devices_, 26(5), 752-764.

### Microplasma and Noise Sources

- **Chynoweth, A.G. and McKay, K.G.** (1956). "Photon Emission from Avalanche Breakdown in Silicon," _Physical Review_, 102(2), 369-376.
- **Rose, D.J.** (1957). "Microplasma Propagation in Silicon," _Physical Review_, 105(2), 413-418. _(historic)_
- **Haitz, R.H.** (1964). "Mechanisms Contributing to the Noise Pulse Rate of Avalanche Diodes," _Journal of Applied Physics_, 35(5), 1370-1376.

### Zener Tunneling (Breakdown) - Discovery and Theory

- **Zener, C.** (1934). "A Theory of the Electrical Breakdown of Solid Dielectrics," _Proceedings of the Royal Society of London A_, 145(855), 523-529. _(historic - original discovery)_
- **Kane, E.O.** (1960). "Zener Tunneling in Semiconductors," _Journal of Physics and Chemistry of Solids_, 12(2), 181-188.
- **Esaki, L.** (1958). "New Phenomenon in Narrow Germanium p-n Junctions," _Physical Review_, 109(2), 603-604. _(historic - experimental observation)_
- **McAfee, K.B., Ryder, E.J., Shockley, W., and Sparks, M.** (1951). "Observations of Zener Current in Germanium p-n Junctions," _Physical Review_, 83(3), 650-651. _(historic)_

### Shot Noise - General Theory

- **Schottky, W.** (1918). "Über spontane Stromschwankungen in verschiedenen Elektrizitätsleitern," _Annalen der Physik_, 362(23), 541-567. _(historic - original discovery of shot noise)_
  - _English translation_: Burkhardt, M. (2018). "On Spontaneous Current Fluctuations in Various Electrical Conductors," _Journal of Micro/Nanolithography, MEMS, and MOEMS_, 17(4), 041001.

### Quantum Randomness and TRNGs using Avalanche Noise

- **Stipčević, M. and Koç, Ç.K.** (2014). "True Random Number Generators," in _Open Problems in Mathematics and Computational Science_, Springer, pp. 275-315.
- **Wang, F.-X., et al.** (2015). "Robust Quantum Random Number Generator Based on Avalanche Photodiodes," _Applied Physics Letters_, 106(24), 241110.
- **Herrero-Collantes, M. and Garcia-Escartin, J.C.** (2017). "Quantum Random Number Generators," _Reviews of Modern Physics_, 89(1), 015004.

# Signal Processing and Sampling

## Overview of the Digital Path

After analog amplification and digitization by the Schmitt inverter, the system produces a **two-level random signal** $v(t) \in \{0,1\}$, switching between logic states according to the underlying analog noise.

This signal is **asynchronous**, meaning transitions occur at random times determined by the stochastic noise process, not by any system clock. To safely interface with microcontrollers or FPGAs and to improve statistical independence, the circuit uses a **D-type flip-flop (CD4013) in toggle mode**.

The complete signal processing chain consists of:

$$\text{Avalanche Noise} \xrightarrow{\text{Amplifier}} v_{\text{analog}}(t) \xrightarrow{\text{Schmitt}} v(t) \xrightarrow{\text{Toggle FF}} Q(t) \xrightarrow{\text{MCU}} x[n]$$

where:

- $v_{\text{analog}}(t)$ = continuous-valued noise voltage
- $v(t)$ = binary digital signal from Schmitt trigger
- $Q(t)$ = flip-flop output (frequency-divided)
- $x[n]$ = final sampled bit sequence

---

## The D Flip-Flop in Toggle Mode

### Circuit Configuration

The CD4013 D-type flip-flop is wired in **toggle configuration** (T flip-flop):

**Pin connections:**

- **CLK** input ← Schmitt trigger output $v(t)$
- **D** input ← $\overline{Q}$ (inverted output, feedback)
- **Q** output → Microcontroller input
- **S, R** (Set, Reset) → Ground (normal operation)

This feedback connection ($\overline{Q} \to D$) transforms the D flip-flop into a toggle flip-flop, which changes state on every active clock edge.

### Operation and Frequency Division

**Truth table for toggle mode:**

| Clock Transition | Current State $Q$ | $D = \overline{Q}$ | Next State $Q^+$ |
| ---------------- | ----------------- | ------------------ | ---------------- |
| Rising edge ↑    | 0                 | 1                  | 1 (toggle)       |
| Rising edge ↑    | 1                 | 0                  | 0 (toggle)       |
| Falling edge ↓   | —                 | —                  | No change        |

**Timing diagram:**

```
Schmitt v(t):  ↑___↑_↑____↑__↑___↑____↑_↑_↑___  (random transitions at rate λ)
Rising edges:  1   2 3    4  5   6    7 8 9

FF output Q:   0_____1_________0_________1____  (toggles on rising edges only)
               ↑     ↑         ↑         ↑
               1     3         5         8
```

**Frequency division mechanism:**

Since the flip-flop:

1. Responds only to **rising edges** (ignores falling edges)
2. **Toggles** its output on each rising edge
3. Requires **two input transitions** (one full cycle) to complete one output cycle

The output frequency is exactly **half** the input frequency:

$$f_Q = \frac{f_v}{2} = \frac{\lambda}{2}$$

where:

- $\lambda$ = average transition rate of Schmitt output $v(t)$ [Hz]
- $f_Q$ = average transition rate of flip-flop output $Q(t)$ [Hz]

**Period relationship:**

$$T_Q = 2T_v = \frac{2}{\lambda}$$

This is a **hardware frequency divider** - the output toggles half as often as the input.

### Benefits for Randomness Extraction

The toggle mode provides three advantages for true random number generation:

**Benefit 1: Automatic Minimum Spacing**

By dividing the transition rate by 2, the flip-flop enforces a minimum time between consecutive output transitions:

$$\Delta t_{\min} = \frac{2}{\lambda}$$

This prevents excessively rapid state changes that might be correlated due to:

- Schmitt trigger hysteresis effects
- Analog noise bandwidth limitations
- Circuit settling times

**Benefit 2: Edge Selection and Symmetry**

The toggle mode responds only to **rising edges** of $v(t)$, effectively:

- Discarding all falling edge information
- Breaking potential correlation between rising and falling transitions
- Ensuring symmetric treatment of 0→1 and 1→0 output transitions

If the Schmitt trigger has asymmetric rise/fall behavior, this edge selection helps decorrelate the output from input asymmetries.

**Benefit 3: Hardware-Based Decorrelation**

The frequency division acts as a **temporal filter**, increasing the effective spacing between transitions. If the input has burst correlations (multiple rapid toggles), the output will be more evenly spaced.

**Comparison:**

| Configuration   | Input rate | Output rate | Min. spacing | Typical correlation |
| --------------- | ---------- | ----------- | ------------ | ------------------- |
| Direct sampling | $\lambda$  | $\lambda$   | $1/\lambda$  | Higher              |
| Toggle mode     | $\lambda$  | $\lambda/2$ | $2/\lambda$  | Lower               |

---

## Two-Stage Sampling Architecture

The complete TRNG employs **two cascaded sampling stages** to convert continuous analog noise into discrete, statistically independent random bits.

### Stage 1: Toggle Flip-Flop (Noise → FF)

**Function:** Asynchronous-to-synchronous conversion with frequency division

**Input:** Schmitt trigger output $v(t)$

- Binary random signal
- Asynchronous transitions
- Average toggle rate $\lambda$

**Process:** Toggle on rising edges
$$Q(t_{k+1}) = \overline{Q(t_k)} \quad \text{when } v(t) \text{ rises}$$

**Output:** Flip-flop state $Q(t)$

- Binary random signal
- Still asynchronous, but frequency-divided
- Average toggle rate $\lambda_Q = \lambda/2$

**Mathematical model:**

Let $\{t_k\}$ denote the sequence of rising edges in $v(t)$. The flip-flop output obeys:

$$Q(t) = Q(0) \oplus \left\lfloor \frac{N(t)}{2} \right\rfloor \pmod 2$$

where:

- $N(t)$ = number of rising edges up to time $t$
- $\oplus$ = XOR (modulo-2 addition)
- $Q(0)$ = initial state

**Effect:** First level of decorrelation and rate reduction.

### Stage 2: Microcontroller Sampling (FF → Bits)

**Function:** Synchronous sampling at controlled rate

**Input:** Flip-flop output $Q(t)$

- Frequency-divided random signal
- Toggle rate $\lambda_Q = \lambda/2$

**Process:** Periodic sampling at rate $f_{\text{sample}}$

$$x[n] = Q(nT_s), \quad T_s = \frac{1}{f_{\text{sample}}}, \quad n = 0, 1, 2, \ldots$$

**Output:** Discrete bit sequence $\{x[n]\}$

- Binary random sequence
- Synchronous (fixed rate)
- Updates at frequency $f_{\text{sample}}$ [bits/s]

**Mathematical model:**

The sampled sequence is:

$$x[n] = Q(t)\Big|_{t=nT_s}$$

where $T_s$ is chosen to satisfy the independence criterion (see Section 4.1).

**Effect:** Second level of decorrelation via controlled undersampling, producing statistically independent bits.

---

**Complete signal flow:**

$$\boxed{\text{Noise}} \xrightarrow[\text{BW} \sim 10\text{ MHz}]{\text{Analog}} \boxed{v_{\text{analog}}} \xrightarrow[\text{Schmitt}]{\lambda \sim 1\text{ MHz}} \boxed{v(t)} \xrightarrow[\text{Toggle}]{\lambda/2} \boxed{Q(t)} \xrightarrow[f_{\text{sample}}]{\text{Sample}} \boxed{x[n]}$$

**Design goal:** Choose $f_{\text{sample}} \ll \lambda/2$ such that $x[n]$ consists of independent, identically distributed (IID) bits with entropy $H \approx 1$ bit/sample.

---

## Theory of Sub-Sampling Random Processes

### Correlation Time and Independence

**Definition of Correlation Time**

For a stationary random process $x(t)$ with mean $\mu = \langle x(t) \rangle$ and autocorrelation function:

$$R_x(\tau) = \langle [x(t) - \mu][x(t+\tau) - \mu] \rangle$$

the **correlation time** $\tau_c$ characterizes the timescale over which the process "remembers" its past:

$$R_x(\tau) \approx 0 \quad \text{for } |\tau| \gg \tau_c$$

**Formal definition (exponential decay model):**

$$R_x(\tau) \approx R_x(0) \cdot e^{-|\tau|/\tau_c}$$

where $R_x(0) = \sigma^2$ is the variance.

Physically, $\tau_c$ represents:

- The duration of memory in the stochastic process
- The timescale for fluctuations to become uncorrelated
- The reciprocal of the effective noise bandwidth

**Relationship to Toggle Rate**

For avalanche noise processed through a Schmitt trigger:

**Case A: Bandwidth-limited noise**

If the analog noise has bandwidth $B$:

$$\tau_c \approx \frac{1}{2\pi B}$$

**Case B: Toggle-limited process**

If the Schmitt trigger is the bottleneck (low noise amplitude, slow switching):

$$\tau_c \sim \frac{1}{\lambda}$$

where $\lambda$ is the average toggle rate of $v(t)$.

**Practical estimate:**

For well-designed TRNGs with high-amplitude noise:

$$\tau_c \approx \max\left\{\frac{1}{2\pi B}, \frac{1}{\lambda}\right\} \sim \frac{1}{\lambda}$$

After the toggle flip-flop:

$$\tau_{c,Q} \approx \frac{2}{\lambda}$$

The flip-flop effectively doubles the correlation time by halving the transition rate.

**Independence Criterion**

For two samples $x[n]$ and $x[n+1]$ separated by time $T_s$ to be **statistically independent**:

$$\langle x[n] \cdot x[n+1] \rangle \approx \langle x[n] \rangle \cdot \langle x[n+1] \rangle$$

This requires the autocorrelation to have decayed to negligible levels:

$$R_Q(T_s) \ll R_Q(0)$$

**Design rule (exponential decay assumption):**

For $R_Q(T_s) < 0.01 \cdot R_Q(0)$ (1% residual correlation):

$$T_s \geq -\tau_{c,Q} \ln(0.01) \approx 4.6 \tau_{c,Q}$$

**Conservative guideline:**

$$\boxed{T_s \geq 10 \tau_{c,Q} = \frac{20}{\lambda}}$$

Equivalently, the sampling frequency must satisfy:

$$\boxed{f_{\text{sample}} \leq \frac{\lambda}{20}}$$

This ensures:

- Autocorrelation $< 0.0001$ (negligible)
- Statistical independence for NIST tests
- Entropy $H \approx 1$ bit/sample

---

### Spectral Aliasing and White Noise Preservation

**The Sampling Theorem for Random Processes**

For a **stationary random process** $x(t)$ with power spectral density $S_x(f)$, sampling at rate $f_s = 1/T_s$ produces a discrete sequence $x[n] = x(nT_s)$ with power spectral density:

$$S_{x[n]}(f) = \frac{1}{T_s} \sum_{k=-\infty}^{\infty} S_x\left(f - \frac{k}{T_s}\right), \quad |f| \leq \frac{1}{2T_s}$$

**Symbol definitions:**

- $S_x(f)$ = power spectral density of continuous signal $x(t)$ [units²/Hz]
- $S_{x[n]}(f)$ = power spectral density of sampled sequence $x[n]$ [units²/Hz]
- $f_s = 1/T_s$ = sampling frequency [Hz]
- $k$ = integer summation index for spectral replicas
- The sum represents **spectral aliasing**: all frequency components at $f + k/T_s$ fold into the baseband $[-1/(2T_s), 1/(2T_s)]$

**White Noise Preservation**

**Definition:** A process is **white** if its power spectral density is constant:

$$S_x(f) = S_0 \quad \text{for all } f$$

**Theorem:** Sampling white noise produces white noise.

**Proof:**

$$S_{x[n]}(f) = \frac{1}{T_s} \sum_{k=-\infty}^{\infty} S_0 = \frac{S_0}{T_s} \sum_{k=-\infty}^{\infty} 1$$

While the infinite sum formally diverges, in practice we consider **finite-bandwidth white noise** with $S_x(f) = S_0$ for $|f| < f_{\max}$ and $S_x(f) = 0$ otherwise.

If $f_{\max} \gg 1/(2T_s)$ (wideband noise, slow sampling), then:

$$S_{x[n]}(f) \approx \frac{S_0}{T_s} \quad \text{for } |f| < \frac{1}{2T_s}$$

The sampled spectrum remains **flat** (white).

**Colored Noise Degradation**

**Colored noise** has frequency-dependent power spectral density, e.g.:

- **$1/f$ noise:** $S_x(f) \propto 1/f$
- **Narrowband noise:** $S_x(f)$ peaked near some $f_0$

When sampled, spectral components from different frequencies fold into the baseband:

$$S_{x[n]}(f) = \frac{1}{T_s} \left[S_x(f) + S_x\left(f - \frac{1}{T_s}\right) + S_x\left(f + \frac{1}{T_s}\right) + \cdots\right]$$

This **mixes** high and low frequencies, creating:

- Spectral structure in the sampled signal
- Temporal correlations in the bit sequence
- Reduced entropy per sample

**Intuitive interpretation:**

| Original spectrum    | Sampled spectrum         | Randomness quality        |
| -------------------- | ------------------------ | ------------------------- |
| White (flat)         | White (flat)             | Preserved ($H \approx 1$) |
| Colored (structured) | Mixed (folded structure) | Degraded ($H < 1$)        |

### When Does Subsampling Preserve Randomness?

**TLDR - Key Condition:**

> Subsampling preserves randomness if and only if the sampling period greatly exceeds the correlation time:
> $$T_s \gg \tau_c$$

**Three regimes:**

| Condition            | Regime        | Sample correlation              | Entropy per bit       |
| -------------------- | ------------- | ------------------------------- | --------------------- |
| $T_s \ll \tau_c$     | Oversampling  | Strong ($R(T_s) \approx R(0)$)  | Low ($H \ll 1$)       |
| $T_s \approx \tau_c$ | Critical      | Moderate ($R(T_s) \sim R(0)/2$) | Medium ($H \sim 0.5$) |
| $T_s \gg \tau_c$     | Undersampling | Negligible ($R(T_s) \to 0$)     | High ($H \approx 1$)  |

**Physical interpretation:**

When samples are spaced by $T_s$:

- If $T_s \ll \tau_c$: Each sample "sees" nearly the same noise realization → high correlation
- If $T_s \gg \tau_c$: The noise has "refreshed" many times → independent samples

**Mathematical criterion (white noise case):**

For white noise with bandwidth $B$, the autocorrelation is approximately:

$$R_x(\tau) \propto \text{sinc}(2\pi B \tau) = \frac{\sin(2\pi B \tau)}{2\pi B \tau}$$

The first zero crossing occurs at $\tau = 1/(2B)$, suggesting:

$$T_s \geq \frac{1}{2B}$$

For practical independence with exponential-type decay:

$$T_s \geq \frac{10}{2\pi B} \approx \frac{1.6}{B}$$

**Combined criterion for toggle flip-flop output:**

$$\boxed{T_s \geq \max\left\{\frac{10}{\lambda}, \frac{1.6}{B}\right\}}$$

where:

- $\lambda$ = Schmitt toggle rate
- $B$ = analog noise bandwidth

---

## Optimal Sampling Strategy

**Condition: Undersampling for Independence**

The design employs **undersampling** where the microcontroller sampling frequency is much lower than the flip-flop toggle rate:

$$f_{\text{sample}} \ll \lambda_Q = \frac{\lambda}{2}$$

Specifically: $T_s \gg \tau_c$, ensuring statistical independence between consecutive samples.

**Design Parameters (Example)**

- Schmitt transition rate: $\lambda = 2 \text{ MHz}$
- Flip-flop output rate: $\lambda_Q = 1 \text{ MHz}$
- Estimated correlation time: $\tau_{c,Q} \approx 2/\lambda = 1\ \mu\text{s}$
- Arduino sampling: $f_{\text{sample}} = 100 \text{ kHz}$
- Sampling period: $T_s = 10\ \mu\text{s} = 10\tau_{c,Q}$

**Transitions between samples:**

$$N_{\text{avg}} = \lambda_Q \cdot T_s = 1 \text{ MHz} \times 10\ \mu\text{s} = 10 \text{ toggles per sample}$$

\

> **Warning - Oversampling:** If $f_{\text{sample}} \gtrsim \lambda_Q$ (sampling too fast), consecutive samples fall within the same flip-flop state. This produces correlated bit runs like $[0,0,0,1,1,1,0,0,\ldots]$ with $H \approx 0.3\text{-}0.7$ bits/sample. The autocorrelation $R(T_s) \sim 0.5 R(0)$ remains significant, causing failures in statistical tests.

> **Note - Excessive Undersampling:** If $f_{\text{sample}} \ll \lambda/100$ (sampling too slowly), entropy per bit remains $H \approx 1$ but total entropy rate decreases proportionally. This wastes the available randomness bandwidth without improving quality. Optimal performance occurs around $f_{\text{sample}} \approx \lambda/20$.

---

## Practical Design Guidelines

### Parameter Selection

**Primary design variables:**

| Parameter           | Symbol              | Role                     | Typical Range         |
| ------------------- | ------------------- | ------------------------ | --------------------- |
| Noise bandwidth     | $B$                 | Analog randomness source | 1–100 MHz             |
| Schmitt toggle rate | $\lambda$           | Digital transition rate  | 0.1–10 MHz            |
| FF output rate      | $\lambda_Q$         | Frequency-divided rate   | $\lambda/2$           |
| Correlation time    | $\tau_c$            | Decorrelation timescale  | $\sim 1/\lambda$      |
| Sampling frequency  | $f_{\text{sample}}$ | Microcontroller rate     | 10 kHz–1 MHz          |
| Sampling period     | $T_s$               | Time between bits        | $1/f_{\text{sample}}$ |

**Design constraints:**

1. **Independence criterion:**
   $$\boxed{f_{\text{sample}} \leq \frac{\lambda}{20}}$$

2. **Correlation decay:**
   $$T_s \geq 10\tau_c \approx \frac{10}{\lambda}$$

3. **Bandwidth requirement:**
   $$\lambda \ll 2\pi B$$

4. **Toggle mode benefit:**
   $$\lambda_Q = \frac{\lambda}{2} \implies \tau_{c,Q} \approx \frac{2}{\lambda}$$

**Design procedure:**

1. **Measure** Schmitt toggle rate $\lambda$ (oscilloscope)
2. **Estimate** correlation time: $\tau_c \approx 1/\lambda$
3. **Choose** sampling frequency: $f_{\text{sample}} = \lambda/20$ (or lower)
4. **Verify** independence: Run autocorrelation test
5. **Validate** entropy: Use NIST SP800-90B estimators

---

### Entropy vs. Bit Rate Trade-off

The fundamental relationship in TRNG design is:

$$\text{Entropy Rate} = H \cdot f_{\text{sample}}$$

where $H$ = entropy per sample and $f_{\text{sample}}$ = sampling frequency.

**Optimal operating point:** $f_{\text{sample}} \approx \lambda/20$

At this point:

- Entropy per bit: $H \approx 0.99$ (near maximum)
- Efficiency: $\eta \approx 99\%$ (minimal waste)
- Test compliance: Pass NIST SP800-22 ($\geq 99\%$ pass rate)

> **Trade-off Note:** Increasing $f_{\text{sample}}$ beyond $\lambda/20$ provides diminishing returns. For example, sampling at $\lambda/5$ (4× faster) only increases entropy rate by $\sim 3×$ due to correlation-induced entropy loss ($H \approx 0.75$). Conversely, sampling below $\lambda/50$ wastes entropy bandwidth without improving $H$ beyond 1.0 bit/sample.

---

## **Our** Design Stats ( Anton [x], Sasha [~] )

**Measured system parameters:**

- Avalanche noise bandwidth (estimated): $B \approx 10 \text{ MHz}$
- Schmitt inverter toggle rate (measured): $\lambda = 5 \text{ MHz}$
- Schmitt hysteresis: $V_{\text{hyst}} \approx 200 \text{ mV}$
- Supply voltage: $V_{\text{CC}} = 5 \text{ V}$

**Step 1: Estimate correlation time**

$$\tau_c \approx \frac{1}{\lambda} = \frac{1}{5 \text{ MHz}} = 0.2\ \mu\text{s}$$

Alternative estimate from bandwidth:

$$\tau_c \approx \frac{1}{2\pi B} = \frac{1}{2\pi \times 10 \text{ MHz}} \approx 16 \text{ ns}$$

Use the larger (more conservative) value: $\tau_c \approx 0.2\ \mu\text{s}$

**Step 2: Flip-flop output characteristics**

Toggle mode divides frequency:

$$\lambda_Q = \frac{\lambda}{2} = \frac{5 \text{ MHz}}{2} = 2.5 \text{ MHz}$$

Effective correlation time increases:

$$\tau_{c,Q} = \frac{2}{\lambda} = 0.4\ \mu\text{s}$$

**Step 3: Choose sampling frequency**

Apply independence criterion:

$$f_{\text{sample}} \leq \frac{\lambda}{20} = \frac{5 \text{ MHz}}{20} = 250 \text{ kHz}$$

Choose: $f_{\text{sample}} = 250 \text{ kHz}$

**Step 4: Verify independence**

Sampling period:

$$T_s = \frac{1}{f_{\text{sample}}} = \frac{1}{250 \text{ kHz}} = 4\ \mu\text{s}$$

Ratio to correlation time:

$$\frac{T_s}{\tau_{c,Q}} = \frac{4\ \mu\text{s}}{0.4\ \mu\text{s}} = 4$$

**Check:** $T_s = 10\tau_{c,Q}$ ✓ (meets criterion)

**Step 5: Predict autocorrelation**

Assuming exponential decay:

$$R_Q(T_s) \approx R_Q(0) \cdot e^{-T_s/\tau_{c,Q}} = R_Q(0) \cdot e^{-10} \approx 4.5 \times 10^{-5} \cdot R_Q(0)$$

**Negligible** (< 0.01% of maximum)

**Step 6: Estimate entropy**

For nearly independent bits with balanced probability:

$$H \approx -0.5\log_2(0.5) - 0.5\log_2(0.5) = 1.0 \text{ bits/sample}$$

With residual correlation $\rho \approx 4.5 \times 10^{-5}$:

$$H \approx 1 - \frac{\rho^2}{2\ln 2} \approx 1 - 10^{-9} \approx 0.9999 \text{ bits/sample}$$

**Step 7: Validation tests**

After implementation, verify:

1. **Mean:** $\langle x \rangle \approx 0.5$ (within [0.49, 0.51])
2. **Lag-1 autocorrelation:** $|\rho_1| < 0.01$
3. **NIST SP800-90B min-entropy:** $H_{\min} \geq 0.95$ bits/sample
4. **NIST SP800-22 statistical tests:** Pass rate $\geq 99\%$

---

# PCB Layout

## Noise Generator (T1, T2, T3, R1–R4, C1)

### Circuit

Two NPN transistors (**T1, T2: MMBT3904**) are connected in **reverse breakdown mode**:
their base–emitter junctions are reverse-biased through resistor **R1**, producing avalanche noise.

- **T1, T2** act as **avalanche noise sources**.
- **R1 (4.7 kΩ)** limits current through them.
- **T3** is a **buffer amplifier** (common-emitter), boosting the noise signal amplitude.
- **R2–R4** set T3’s bias and gain; **C1 (0.1 µF)** filters out DC components and shapes the noise bandwidth.

### Function

When Vcc (≈ 9–12 V) is applied, T1–T2 produce microscopic avalanche discharges across their junctions.
Each discharge generates a pulse of current with random amplitude and timing — the **entropy source**.
T3 amplifies this weak signal into a measurable, broadband random voltage (~hundreds of mV RMS).

This stage outputs **analog white noise**, typically spanning tens to hundreds of MHz.

---

## Schmitt Inverter (IC2A: 74LS14D)

### Circuit

**IC2A** is one gate of the **74LS14 hex Schmitt-trigger inverter**.
It has a built-in **hysteresis window**, meaning it switches from “0” to “1” only when input voltage crosses a specific threshold (~1.6 V rising, ~0.8 V falling).

### Function

It serves as a **comparator + digitizer**:

- Converts the **analog noise waveform** from the previous stage into **clean logic pulses**.
- Removes slow fluctuations and ensures sharp transitions (rise/fall time < 22 ns).
- The hysteresis prevents false triggering on mid-level noise, improving stability.

Output is a **digital two-level random signal**, toggling between logic “0” and “1” unpredictably — effectively a **raw random bit stream**.

---

## Data Latch / Synchronizer (IC3A: 4013D)

### Circuit

**IC3A** is one flip-flop of a **CD4013 dual D-type latch**.
Connections:

- **D** — data input receives the digital noise stream from 74LS14.
- **CLK** — clock input (likely from Arduino or internal timing).
- **Q** — output bit (read by Arduino digital pin).
- **S**, **R** — asynchronous set/reset (here tied low for normal operation).

### Function

This module **samples** the random bit stream in a controlled way.

Without it, the Arduino might read metastable or glitchy data from the noisy inverter output.
The flip-flop ensures that:

- Each bit is **captured at a defined time** (synchronized to a system clock).
- Output complies with **logic timing constraints** of the microcontroller.
- Optional post-processing (whitening, XOR folding, etc.) can be applied later.

In short:

> **Schmitt inverter** → digitizes noise,
> **Flip-flop (4013)** → samples and stabilizes it.

---

### Arduino Interface

The **Arduino UNO R3** then reads the digital output through GPIO and can:

- Transfer raw data to a PC (via UART/USB).
- Perform simple statistical checks.
- Or later, be replaced with **FPGA** for higher-rate entropy harvesting.

# Bills of materials per Block

## Noise Generator & Pre-Amp

| Ref          | Part / Value                                                              | Suggested part    | Purpose / Notes                                                                                |
| ------------ | ------------------------------------------------------------------------- | ----------------- | ---------------------------------------------------------------------------------------------- |
| T1, T2       | NPN BJT (used in reverse BE breakdown)                                    | MMBT3904 (SOT-23) | Avalanche noise sources (reverse-bias base-emitter junctions). Low cost, consistent breakdown. |
| R1           | 4.7 kΩ, 1/8 W, 1%                                                         | any               | Limits reverse current through T1/T2; sets bias point/noise rate.                              |
| T3           | NPN BJT, pre-amp                                                          | MMBT3904 (SOT-23) | Common-emitter gain stage to boost noise amplitude.                                            |
| R2           | 10 kΩ, 1/8 W, 1%                                                          | any               | Bias network for T3 (collector or base, per your schematic labeling).                          |
| R3           | 10 kΩ, 1/8 W, 1%                                                          | any               | Bias/gain setting for T3.                                                                      |
| R4           | 100 Ω–1 kΩ, 1/8 W, 1% _(shown “10Ω–10MΩ” range in draft — pick ~330–1kΩ)_ | any               | Emitter/collector load or series element to shape gain/stability; pick to avoid saturation.    |
| C1           | 0.1 µF, X7R                                                               | 0603/0805         | AC-couples / shapes bandwidth; also shunts LF drift.                                           |
| VCC (analog) | 9–12 V                                                                    | —                 | Supply for noise source & BJT stage. Keep separate trace from digital where possible.          |

**Notes:**

- Start with R4 ≈ 330–680 Ω; adjust for clean, broadband spectrum without clipping.
- Add optional RF cap (e.g., 10–47 pF) across collector-base of T3 if oscillations appear.
- Place C1 and any decoupling close to T3.

---

## Schmitt Inverter (Digitizer)

| Ref            | Part / Value     | Suggested part    | Purpose / Notes                                                                         |
| -------------- | ---------------- | ----------------- | --------------------------------------------------------------------------------------- |
| IC2A           | Schmitt inverter | 74LS14D (SOIC-14) | Converts analog noise to clean logic levels with hysteresis. Rise/fall < 22 ns typical. |
| VCC (logic)    | +5 V             | —                 | Logic supply (separate from 9–12 V analog).                                             |
| Decoupling     | 100 nF near IC2  | any, X7R          | Local decoupling for fast edges / noise immunity.                                       |
| Input coupling | from T3 via C1   | —                 | Ensure input swings across Schmitt thresholds (~0.8 V/1.6 V for LS).                    |

**Notes:**

- 74HC14 or 74HCT14 also work on 5 V; HC/HCT offer lower power.
- Keep input trace short; ground reference solid to avoid false triggers.

---

## Data Latch / Synchronizer

| Ref        | Part / Value      | Suggested part    | Purpose / Notes                                                            |
| ---------- | ----------------- | ----------------- | -------------------------------------------------------------------------- |
| IC3A       | D-type flip-flop  | CD4013D (SOIC-14) | Samples Schmitt output on clock; stabilizes timing for MCU/FPGA.           |
| CLK        | from Arduino/FPGA | —                 | Sampling clock; choose rate << inverter toggle rate to avoid correlations. |
| D          | from IC2A output  | —                 | Random data input.                                                         |
| Q          | to MCU/FPGA GPIO  | —                 | Synchronized random bit.                                                   |
| S, R       | tie low           | —                 | Normal operation (no async set/reset).                                     |
| VDD        | +5 V              | —                 | Matches MCU logic.                                                         |
| Decoupling | 100 nF near IC3   | —                 | Local supply decoupling.                                                   |

**Notes:**

- If using 74xx D-FF (e.g., 74HC74), ensure logic-level compatibility and timing with your clock.
- For higher rates, move this function into FPGA fabric (synchronizer + debiasing inside).

---

## Arduino Interface (I/O & Power)

| Ref        | Part / Value   | Suggested part | Purpose / Notes                                             |
| ---------- | -------------- | -------------- | ----------------------------------------------------------- |
| MCU        | Arduino UNO R3 | ATmega328P     | Reads Q, provides CLK, streams data to PC.                  |
| IO pins    | D-pins         | —              | Q → digital in; CLK → digital out; optional status LEDs.    |
| +5 V / GND | board headers  | —              | Power for logic; ensure common ground with analog stage.    |
| USB/UART   | onboard        | —              | Data transfer; will bottleneck high bitrates (> ~2 Mbit/s). |

**Notes:**

- For > few Mbit/s, consider FPGA + Ethernet, or at least a faster USB CDC device.

---

## Power & Decoupling (recommended)

| Ref      | Part / Value        | Suggested part        | Purpose / Notes                                            |
| -------- | ------------------- | --------------------- | ---------------------------------------------------------- |
| Cbulk-A  | 10–47 µF on 9–12 V  | electrolytic/tantalum | Stabilize analog rail for avalanche stage.                 |
| Cdec-A   | 100 nF at T-stage   | X7R                   | HF decoupling close to T3.                                 |
| Cdec-L   | 100 nF per logic IC | X7R                   | Place next to 74x inputs (IC2/IC3).                        |
| Star GND | layout practice     | —                     | Keep analog return short; join to digital at single point. |
