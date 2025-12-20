# 2017 Single-photon_imager_based_on_a_superconducting_nanowire_delay_line.pdf

> TAG:pbit,base
> This is best practices paper among photon-detection community

- The nanowire is terminated at each end with a Klopfenstein taper to transform from the high characteristic impedance of the nanowire to 50 Ω (ref. 24).
  - The nanowire is terminated at each end with a Klopfenstein taper to transform from the high characteristic impedance of the nanowire to 50 Ω (ref. 24).
    > This ensures an effciient coupling of the electrical pulses triggered by a photon-detection event to a 50 Ω microwave readout circuit, which in turn allows us to extract the time and position of the absorbed photon using the relative arrival times of the output electrical pulses at the two ends of the nanowire.

## Why Klopfenstein taper

"The performance of the Dolph-Tchebycheff transmission-line taper treated here is optimum in the sense that it has minimum reflection coefficient magnitude in the pass band for a specified length of taper, and, likewise, for a specified maximum magnitude reflection coefficient in the pass band, the Dolph-Tchebycheff taper has minimum length."

## How to check fabricated taper

We used the Klopfenstein taper for transforming the nanowire impedance to 50 Ω to preserve the fast-rising edge of a photon-detection pulse. To verify the taper’s performance, we fabricated a 17 mm long NbN taper without a photon-sensitive nanowire at the middle. The taper was designed into a CPW structure with a fxied 3 μm gap to the ground plane and a signal line whose width smoothly changed from 88 μm at the two ends to 10 μm in the centre. To characterize the superconducting taper without switching it to the normal state by the input signals, the narrowest width of the nanowire in the centre was designed to 10 μm to have a switching current (ISW) of 0.4 mA.

The bandwidth of the taper was measured by a network analyser (Supplementary Fig. 1b). The pass band of the taper started at 0.7 GHz, and was able to cover the spectrum of the fast edge triggered by photon absorption. The performance of the taper also validated the calculation of the superconducting transmission line. Although the pass band stopped at 2.4 GHz because of the loss of the printing circuit board (PCB) and the bonding wires, the bandwidth was suffciient to support the readout of the fast output pulses.

We demonstrated the pulse propagation by sending a pulse into the taper and measuring the output pulse from the other end. A 200 ps wide electrical pulse (Avtech, AVMP-2-C-P-EPIA) was split into two. One pulse was acquired by a 6 GHz oscilloscope as a timing reference while the other pulse was fed into the taper and its transmitted signal was acquired by another channel of the oscilloscope. We also compared the transmitted signal from the taper to the transmitted signal from a 50 Ω transmission line with the same length (corresponding to a delay of 94 ps), but made on a PCB. The delay difference between a PCB transmission line and the taper was 760 ps, which indicates the superconducting taper slowed down the average velocity to 11% of a PCB transmission line. The amplitude of the transmitted signal from a taper reduced to 60% of the transmitted signal from the PCB transmission line; however, the rising edge of the pulse was well preserved, which verifies that the taper helped the propagation of the fast pulse through a wire of mismatched impedance.
