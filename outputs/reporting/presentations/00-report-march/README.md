## Outline

- Motivation

  - Green Computing
  - Algorithm efficiency: how probalistic annealing compares to simulated annealing and quantum annealing

- physical implementation via MTJ, historically first. there are also Diffusive Memristors and superconducting circuits.

- pbit model

  The state of p-bit is updated according to the equation:

  $$\sigma_i = \text{sign}(\tanh(\beta I_i) - r)$$

  where

  - $r$ is a uniform random number from [-1, 1],
  - $\beta$ is the inverse temperature

- SBN implementation via NbN nanowire
  We chose NbN because this compound is well-studied, has good superconducting properties, it’s compatible with existing technologies
  For stochastic regime being more stable we needed a wide critical temperature hysteresis (bigger difference between temperature at which NbN switches to superconducting state and temperature of switching back to normal state). Literature review showed that for that we needed NbN to have defects and impurities, so We started with nanowires from NbN that was deposited at room temperature. We did a lot of tests and carefully removed noise sources from the measuring circuit, but measurements were still too noisy and didn’t provide proper random stochastic switching. We found out that our nanowires didn’t switch to superconducting state completely. It was clear that we needed NbN with more pure structure, so we decided to move to another NbN technology, in which NbN is deposited at high temperature. This technology provides more structured NbN with better superconducting properties, and in measurements it showed truly random switching. Such technology is more complicated as it requires a fine adjustment of many parameters of deposition and more fabrication steps, so we asked for help of Moscow State Pedagogical University to provide us with finished nanowire of such properties while we’re working on this technology to make more nanowire chips.

- SBN signal measurements
  General view of the measuring stand.

  Measurement is performed in a cryostat from SCONTEL. Lock-in SR860 is used as a source of AC (clocking signal) and DC control signal. An oscilloscope is used as a recording device.

  Measurement scheme. The oscilloscope is connected with a 50 ohm input in parallel with the sample. When the critical current is exceeded, the resistance increases sharply and the current flows through the oscilloscope to a greater extent, on which the peak is recorded.

  The process of reading and processing data from the oscilloscope is laborious and slow. In order to speed up the reading process, a comparator preamplifier is proposed. It is supposed to amplify the signal and bring its level to the value read as a logical 1 or 0, so the need to digitize the analog signal will be eliminated.

  Below is the schematic circuit board and the first prototype of the device.

- pbit data
  pbit data as a function of bias voltage is a probability of sampling 0 or 1 that looks like a sigmoid function

- Probabilistic optimization

  Hamiltonian for spins **σ ∈ {-1, 1}** with interaction of adjacent spins and **h** - magnetic field

  $$H(\sigma) = -\sum_{\langle i,j \rangle} J_{ij}\sigma_i\sigma_j - \mu \sum_j h_j\sigma_j$$

  Consider finding optimal result as it's minimum

  Then influence of one spin/p-bit

  $$I_i = -\frac{\partial E}{\partial \sigma_i} = \sum_j J_{ij}\sigma_j + \mu h_i$$

- TanH fit of NbN wire
  present a picture, say that it was successfully fitted. Also specs like temperature, frequency.

- QUBO portfolio optimization

  - general formula and its terms:
    Quadratic Unconstrained Binary Optimization
    (NP-hard category use of probabilistic architecture)

    $f(x) = -\sum_{i=1}^{n} r_i x_i + \lambda \sum_{i=1}^{n}\sum_{j=1}^{n} \sigma_{ij}x_i x_j$

    $f(x)$ - returns covariance, $-\sum_{i=1}^{n} r_i x_i$ - risk

    - **General QUBO Formula**:

      - $f(x) = -\sum_{i=1}^{n} r_i x_i + \lambda \sum_{i=1}^{n}\sum_{j=1}^{n} \sigma_{ij}x_i x_j$
      - Where:
        - $f(x)$ represents our objective function to minimize
        - $x_i \in \{0,1\}$ represents decision to include asset $i$
        - $r_i$ is expected return of asset $i$
        - $\sigma_{ij}$ is covariance between assets $i$ and $j$
        - $\lambda$ balances return vs. risk tradeoff

    - **Key Components**:

      - First term: $-\sum_{i=1}^{n} r_i x_i$ represents negative of expected returns (we minimize negative returns = maximize returns)
      - Second term: $\lambda \sum_{i=1}^{n}\sum_{j=1}^{n} \sigma_{ij}x_i x_j$ represents portfolio risk (variance)
      - Finding minimum of this function yields optimal risk-adjusted portfolio

    - **Benefits of QUBO**:
      - Natural mapping to Ising spin model used in P-Bit computing
      - Can efficiently incorporate additional constraints (budget, sector limits)
      - Addresses complex nonlinear relationships between assets

  - our case:

    The QUBO problem in Ising representation can be written as:

    $$f(s) = -\lambda_0 \sum_{i=1}^{n} r_i s_i + \lambda_1 \sum_{i=1}^{n} \sigma_i^2 s_i + \lambda_2 \sum_{i=1}^{n} \sum_{j=1,j≠i}^{n} \sigma_{ij} s_i s_j + \lambda_3 \left(\sum_{i=1}^{n} s_i - \text{budget}\right)^2$$

    Where:

    - $s_i$ represents the Ising spin variables (-1 or +1)
    - $n$ is the number of assets
    - $r_i$ is the expected return of asset $i$
    - $\sigma_i^2$ is the variance (risk) of asset $i$
    - $\sigma_{ij}$ is the correlation between assets $i$ and $j$

    **Lambda Meanings**

    From the code:

    - **λ₀ = 2.0**: Profit importance coefficient - scales how much we value returns
    - **λ₁ = 0.3**: Risk penalty coefficient - scales how much we penalize individual asset risk
    - **λ₂ = 0.2**: Correlation penalty coefficient - scales how much we penalize correlated assets
    - **λ₃ = 0.1**: Budget constraint coefficient - ensures the solution uses exactly the budget amount

- discuss figures from optimization
