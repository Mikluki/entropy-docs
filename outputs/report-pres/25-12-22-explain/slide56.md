## What to INCLUDE (and why)

- **Physical entropy source:** reverse-biased PN junction operated in avalanche regime
- **Origin of randomness:** stochastic impact ionization events in silicon
- **Signal chain:** analog noise → amplification → comparator / digitizer
- **Output:** fast, hardware-generated stochastic bitstream suitable for p-bits

- Implemented with standard room-temperature silicon devices (no exotic materials or cryogenic operation)

---

This board implements 32 fully independent physical noise sources, each locally amplified and digitized, and exposed as parallel stochastic bit streams to the SoC.
