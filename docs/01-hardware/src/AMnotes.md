# Alexandr Morozov notes

Anton Kanos mentioned the work by **Mario Lanza** on _“clicking” field-effect transistors_
([Nature, 2025](https://www.nature.com/articles/s41586-025-08742-4)).

After that, Denis shared a couple more papers about **dark counts** in single-photon photodiodes as a source of random numbers.

---

## Questions That Arose

- Why not?
- Why so complicated?
- What do we actually gain from nanowires?

---

## General Logic

Here’s how I see it:
as long as our program runs on a **classical computer**, and **nanowires** serve only as a **source of randomness** (while NWs still can’t solve problems _within_ a superconducting system), we **don’t gain any fundamental advantage**.

We’ll still be limited by the speed of the computer or FPGA.
Meanwhile, the signal has to be **pulled into and out of the cryostat**, read, and processed.

The main advantage of NWs is the **quantum nature of randomness** (though even that raises some questions).

---

## Consequence

Therefore, in principle, **any system** that provides a **random variable** and is **scalable** would do.

Single-photon photodiodes are also not easy to use —
at the very least, they are **expensive** and **not easy to acquire**.

---

## Choice of Approach

I decided to focus on one of the simplest possible solutions
(only thermal resistor noise would be simpler):

> **Noise from a reverse-biased PN junction under breakdown.**

---

## Breakdown Types

1. **Avalanche breakdown** — caused by impact ionization of accelerated charge carriers.
2. **Tunneling breakdown.**

In both cases, the current **fluctuates strongly**.

---

## Advantages

The advantage of such a noise source over thermal resistor noise
is its **higher signal amplitude**, which is easier to amplify to a detectable level.

---

## Source and Circuit

As a foundation (shamelessly copied), I used the [**Z1FFER** project](https://github.com/robseward/Z1FFER/blob/master/Ziffer_v0.2.0.r1.pdf).

**Power supply:**

- noise-generating section: $V_{CC} = 9\text{–}12,\text{V}$
- digital section: $5,\text{V}$

---

## Circuit Components

- **T2** — the noise-generating transistor.
- **T1, T3** — a transistor pair used to amplify the noise; cutoff frequency at least $300,\text{MHz}$.
- **IC2 (74LS14)** — Schmitt trigger (comparator with fixed threshold and built-in hysteresis),
  with rise/fall times below $22,\text{ns}$ (maximum frequency $\approx 22,\text{MHz}$).
- **IC3** — data storage register for the Arduino.
  In the future, this will be implemented directly in the FPGA.

---

## Performance

From observations:
the system generates about $1,\text{GB}$ of random data in just under an hour,
that is, approximately $2,\text{Mbit/s}$.

---

## Block Diagram and Scaling

At present, the speed is limited by **data transfer to the PC**.
When switching to an **FPGA with Ethernet**, this limit will shift significantly.

If there’s a shortage of random data, the **noise amplifier + comparator** blocks can simply be **duplicated**.

---

Would you like me to continue with an explanation of the **underlying physical principles** —
for example, how avalanche and tunneling breakdown produce noise,
how the amplification and digitization stages work,
and what limits entropy quality and bit rate?
