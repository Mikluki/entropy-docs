## Demo task

Match source to load

- frequency range 0.9 - 1.1 MHz
- source with impedance of 50 Ohms
- load with impedance of 0.1 Ohms

### Example: Taper matching 10 GHz

- Suppose a **50 Ω to 0.1 Ω taper** is used at **10 GHz**. The wavelength at 10 GHz (assuming free-space propagation) is:

  $$
  \lambda = \frac{c}{f} = \frac{3 \times 10^8}{10 \times 10^9} = 3 \text{ cm}
  $$

- If the taper is **3 cm long** (~1$\lambda$), the impedance transition is **smooth over a full wavelength**. This allows the wave to **gradually adapt** to the impedance change, reducing reflections.

Thus, at high frequencies, **tapers act as broadband impedance transformers** by leveraging distributed effects.

### Example: Taper matching 1 MHz

- Suppose we use the same **50 Ω to 0.1 Ω** taper at **1 MHz**. The wavelength at 1 MHz is:

  $$
  \lambda = \frac{3 \times 10^8}{1 \times 10^6} = 300 \text{ m}
  $$

- If the taper is **3 cm long** (~$\frac{3}{30000} \lambda$), it covers a **tiny fraction of the wavelength**. The impedance transition is effectively a **sharp step**, making the taper **useless**.

At low frequencies, the best way to match impedances is **using lumped-element components** (inductors, capacitors, or transformers) instead of tapers.

### Example: Pi matching newtwork 1 MHz

### Summary

- At low frequencies, taper length is too small relative to $\lambda$, so lumped-element matching is preferred.
- At high frequencies, tapers enable smooth impedance transitions and broadband matching.

## Results

![Component Layout](graphics/pi-network-1MHz-10-01/00-pi-network_cut.png){ width=300px }

Matching scheme for a typical Pi newtwork consits of 2 shunt Capacitors and 1 series inductor

![Absroption](plots-mnws/Pi-match-abs.png){ width=400px }

From either S11 or Absroption profiles perfect match can be observed despite high $Q_\text{source} / Q_\text{load} = 50 / 0.1$ ratio. Only potential drawback is rather low bandwidth of $\pm 20\ \text{KHz}$.

::: {#fig:subfigs layout-ncol=2}
![S11](plots-mnws/Pi-match-s-db.png){width=380px #fig:left}
![Impedance](plots-mnws/Pi-match-z.png){width=380px #fig:right}
:::

## SUPP: L-Pi-T matching networks

Naming is motivated by a form that series and shunt components crate.

### **1. L-Matching Network**

[Detailed guide on L-Matching newtwork configuration](https://eng.libretexts.org/Courses/Fontys_University_of_Applied_Sciences/Telecommunications/03%3A_Impedance_Matching/3.04%3A_The_L_Matching_Network)

- **When to use:**
  - You need a simple, low-component matching network.
  - The impedance transformation ratio is moderate.
  - Narrowband applications where minimal components are preferred.
- **Limitations:**
  - It only works in one frequency band.
  - It provides limited control over bandwidth.

### **2. Pi-Matching Network (π)**

- **When to use:**
  - High impedance transformation ratio is required.
  - You need **better filtering** (Pi-networks have a low-pass response).
  - You want a **wider bandwidth** than an L-network.
  - Commonly used in RF power amplifiers and antenna matching.
- **Limitations:**
  - More complex than an L-network.

### **3. T-Matching Network**

- **When to use:**
  - You need an **even higher** impedance transformation range than Pi-networks.
  - You want a **high-pass filtering** characteristic (opposite to Pi-network).
  - Good for cases where impedance varies widely (like antenna tuners).
- **Limitations:**
  - More complex than an L-network.
  - Higher insertion loss compared to L-networks.
