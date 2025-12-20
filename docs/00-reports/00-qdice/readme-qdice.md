# [Quantum Dice](https://www.quantum-dice.com/) (Oxford, UK) Report

## Physical Performance: The 4 Photonic Sources

The hardware foundation consists of 4 indium phosphide photonic integrated circuits (PICs) manufactured at Fraunhofer HHI and controlled by a Xilinx Zynq UltraScale+ FPGA board. The experimental validation in Figure 13 demonstrates that these 4 physical sources behave as designed. Raw output distributions follow the expected Gaussian behavior across all devices. Bias control via digital voltage threshold produces sigmoid response curves that match the theoretical model with negligible variation in probability responses across all sources.

**Hardware components:**

- 4 InP photonic integrated circuits from Fraunhofer HHI
  - Distributed feedback laser
  - Waveguides
  - Mach-Zehnder interferometer beamsplitters
  - Balanced photodetectors
- Electronic control: Xilinx Zynq UltraScale+ FPGA board, transimpedance amplifiers, drivers, power supply

![Optoelectronic probabilistic processor prototype based on 4 physical photonic p-bit sources, each implemented with a photonic integrated circuit, connected to an FPGA-based digital control implemented using the FPGA evaluation board allowing for the manipulation and programming of 64000 logical p-bits. The inset image shows a zoomed-in image of the photonic integrated circuit used to implement the p-bit.](pics/p0-orbit.png){width=400px #fig:device}

**Physical backend:**

- QRNG(quantum random number generator) generates the randomness through performing a measurement of the quantum electromagnetic vacuum’s fluctuations.

**Measured performance (Figure 13):**

- Relative error in bias curves: < 0.7% across all 4 sources
- Output distributions follow expected Gaussian behavior
- Sigmoid bias response curves match theoretical model

**System performance (stated in text, Figure 14):**

- Flip rate: 2.7 × 10$^9$ flips/s
- Energy consumption: 4.9 nJ/flip
- Definition: complete cycle (apply bias, produce sample, digitize)

The SDI (source-device independent) protocol enables real-time certification of the input photon count via a "sum" measurement, allowing the system to verify randomness quality continuously. Control of the p-bit probabilities is achievable through three independent paths: modulating the MZI splitting ratio photonically, adjusting a biasable comparator in the analog stage, or applying a digital threshold post-digitization.

## Scaling from Physical to Logical P-bits: The 64,000 Claim

The paper claims to implement 64,000 logical p-bits using only 4 physical photonic sources. The stated mechanism (Section 3.4) is time-domain de-multiplexing: the high-speed photonic samples are buffered and held in memory, creating multiple virtual p-bits from each physical source's fast output stream. The de-multiplexing ratio supposedly depends on photonic source speed, control system bandwidth, available memory, and precision requirements.

However, the paper provides no algorithmic description of how this de-multiplexing works. There is no specification of data structures, no memory model, no protocol for maintaining p-bit state across multiple logical instances, and no latency analysis. Critically, there is no experimental validation. The 4 physical p-bits are thoroughly characterized in Figure 13—their probability distributions, bias response curves, and consistency are all demonstrated. None of this characterization is provided for the claimed 64,000 logical p-bits. There is no evidence that they maintain expected probability distributions when operating together, no test of inter-p-bit interactions, no analysis of whether the scaling breaks down at some threshold, and no validation that synchronization between logical p-bits actually works.

## Optimization Capability

The paper makes no computational demonstrations. While the abstract claims capability for "combinatorial optimization" and references QUBO formulations, Section 5 contains no problem solved, no benchmark run, no comparison to classical solvers or other hardware. The paper explains the theory of how p-bit networks map to optimization problems (Sections 2-3) and discusses control mechanisms for biasing p-bits through interaction matrices, but these remain conceptual exercises. The experimental section focuses entirely on characterizing the hardware—measuring flip rates and energy per flip as physical quantities—not on solving any actual problem. The paper explicitly frames Section 5 as measuring "the speed of the probabilistic computer considering the time it takes not only to generate a sample from a source, but the entire process of applying a bias, producing a sample and digitizing it," which is a hardware performance metric, not a computational result.

## [Presentation](https://www.youtube.com/watch?v=kQTl6g0Gc4E) Claims (ORBIT, October 2025)

The ORBIT platform presentation made three key claims:

- 4,096 parallel pbits in one unit, capability for combinatorial problems using QUBO and hypergraph optimization, and room temperature operation. The paper does not explicitly address these claims. The 64,000 figure cited in the paper (through de-multiplexing) differs from the 4,096 stated in the presentation, and there is no indication whether these refer to the same system or different configurations.
- Room temperature operation is mentioned in the abstract and introduction as an advantage over MTJ-based systems.
- The capability for QUBO and hypergraph optimization is discussed theoretically in the paper but never demonstrated computationally.

## Summary

**Validated:** The 4 physical photonic p-bit sources work as described, with measurable precision and consistency across devices.

**Claimed but unsubstantiated:** Scaling to 64,000 logical p-bits via time de-multiplexing. No details, implementation, or functional testing provided.

# Other Pbit Companies

The probabilistic computing sector is nascent with few commercial players. [Extropic](https://extropic.ai/hardware), founded in 2022 by quantum computing researcher Guillaume Verdon and Trevor McCourt, is developing thermodynamic sampling units (TSUs) that harness out-of-equilibrium thermodynamic systems to perform probabilistic computations. The company raised $14.1 million in seed funding in March 2024 from investors including Kindred Ventures, with additional support from angels including executives from Google, Meta, Cohere, and Shopify. Extropic's development platform ([XTR-0](https://extropic.ai/writing/inside-x0-and-xtr-0)) ships Q3 2025, with the Z1 production chip planned for early 2026, targeting 250,000 interconnected pbits per chip.

![XTR-0 by Extropic](pics/p1-xort.png){ width=600px #fig:label}

Early prototypes used superconducting aluminum with Josephson junctions, but the company has shifted to silicon-based designs that operate at room temperature, eliminating the need for cryogenic cooling systems. The company claims transformers on a thermodynamic computer are up to 100 million times more energy efficient than on GPU cloud infrastructure.

# Quantum RNG Companies

The quantum random number generation market includes numerous companies that could technically pivot to probabilistic computing hardware. All QRNG implementations generate the core requirement for probabilistic systems—controllable true randomness—making QRNG expertise a natural foundation for p-bit development.

**Major QRNG vendors by technology approach:**

QRNG based on shot noise and photon detection include ID Quantique (Switzerland), and Toshiba Europe (UK).

QRNG based on quantum tunneling includes Quintessence Labs (Australia), which uses forward-biased diode tunneling to generate random fluctuations.

QRNG from discrete optical modules include Crypta Labs (UK), which developed custom quantum optics modules (QOM) for QRNG.

# Sources

- [QDice](https://www.quantum-dice.com/) :: https://www.quantum-dice.com/
- [Latest arxiv Publications from QDice](https://www.quantum-dice.com/publications/) :: https://www.quantum-dice.com/publications/
- [Presentation @ Abu Dhabi Maritime Academy](https://www.youtube.com/watch?v=kQTl6g0Gc4E) :: https://www.youtube.com/watch?v=kQTl6g0Gc4E
- [Extropic](https://extropic.ai/hardware) :: https://extropic.ai/hardware
