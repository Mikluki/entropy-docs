Slide 4 should be a **single clean pipeline** from “p-bit PCB” → “Zynq” → “Ethernet” → “PC”, with **one timing badge per request path**, and only _one_ fork to show “1 bit” vs “32 bits”.

### What to put on the diagram (minimal but complete)

**Title (active):**
**“From physical p-bits to controllable random bits (0.3 ms per 32-bit request)”**

#### 1) Left block: **p-bit PCB (entropy + digitize)**

A single box with **3 sublabels** (don’t draw the whole schematic):

- Entropy source
- Analog amplifier
- Digitizer

One output arrow labeled:

- **“raw stochastic bitstream”**

#### 2) Middle block: **Zynq SoC (FPGA fabric)**

One box. Inside, only 3 bullets:

- Probability control ("set p")
- Readout interface ("sample bits")
- Batching ("1 bit or 32-bit vector")

Incoming arrow: raw bitstream.
Outgoing arrow: “probabilistic bits API”.

Add a small note near this block:

- **“p-bit PCB mounts directly to Zynq”**

#### 3) Right block: **Control PC**

One box labeled “PC Controller”.
Inside, 2 bullets:

- Runs solver / experiment
- Requests samples, collects results

#### 4) Connection between Zynq and PC

A single arrow labeled:

- **Ethernet / UDP**

That’s it. No “internet” wording on the slide—use “Ethernet (UDP)” to keep it concrete and clean.

---

### Timings (how to show without clutter)

Put **two “timing badges”** near the Ethernet/UDP arrow (or next to the Zynq “API” label):

- UDP hardware call (32-bit): ~0.0003 s (0.3 ms)
- Python + NumPy baseline: ~0.0133 s (13.3 ms)

And one tiny footer note (small font):

- “Measured on current setup; single run microbenchmark.”

If you want a simple “speedup” callout (optional, but PM-friendly):

- **“~44× faster than Python sampling (13.3 ms → 0.3 ms)”**
  (You can say “~40×” if you prefer conservative rounding.)

---

### Labels that keep it PM-level

Use these words on the slide:

- “Entropy source”, “Digitizer”, “FPGA probability control”, “UDP request”, “32-bit batch”.

Avoid these on the slide (keep for narration/Q&A):

- “Schmitt inverter”, “latch synchronizer specifics”, component names, internal signal names.

---

### One sentence narration to glue it together

“Physical noise becomes a digitized stochastic bit on the p-bit PCB, Zynq sets the requested probability and batches bits, and the PC fetches samples over UDP in about **0.3 ms per 32-bit request**.”

That should make slide 4 read like a clean system story, not a lab notebook.
