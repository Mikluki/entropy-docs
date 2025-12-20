# Klopfenstein taper

## Basics

- Naming:
  Taper is basically something that gets narrow the further it goes

- Requirements:

  1. 1 GHz -> 30 cm or 0.3 meters

## 2017 Single-photon_imager_based_on_a_superconducting_nanowire_delay_line.pdf

Impedance matching tapers could in principle be used to minimize reflections, enhance signal levels, and provide faster rising edges to reduce timing jitter [32]. In our case, instead of performing a perfect impedance matching with a centimeter long taper, we used a short taper with high cut-off frequency. Though the imperfect impedance matching resulted in large reflections, it was possible to trigger at a lower threshold to capture only the initial part of the rising edge. Also, as will be shown later, the distinctive pulse shapes caused by reflection actually enabled us to resolve more than two photons.

## Links

> NOTE:
>
> - MICROWAVE AND RF DESIGN NETWORKS vol3 RFDesign_vol3.pdf
> - 2017 Single-photon_imager_based_on_a_superconducting_nanowire_delay_line.pdf

## How to check fabricated taper

> 2017 Single-photon_imager_based_on_a_superconducting_nanowire_delay_line.pdf

We used the Klopfenstein taper for transforming the nanowire impedance to 50 Ω to preserve the fast-rising edge of a photon-detection pulse. To verify the taper’s performance, we fabricated a 17 mm long NbN taper without a photon-sensitive nanowire at the middle. The taper was designed into a CPW structure with a fxied 3 μm gap to the ground plane and a signal line whose width smoothly changed from 88 μm at the two ends to 10 μm in the centre. To characterize the superconducting taper without switching it to the normal state by the input signals, the narrowest width of the nanowire in the centre was designed to 10 μm to have a switching current (ISW) of 0.4 mA.

The bandwidth of the taper was measured by a network analyser (Supplementary Fig. 1b). The pass band of the taper started at 0.7 GHz, and was able to cover the spectrum of the fast edge triggered by photon absorption. The performance of the taper also validated the calculation of the superconducting transmission line. Although the pass band stopped at 2.4 GHz because of the loss of the printing circuit board (PCB) and the bonding wires, the bandwidth was suffciient to support the readout of the fast output pulses.

We demonstrated the pulse propagation by sending a pulse into the taper and measuring the output pulse from the other end. A 200 ps wide electrical pulse (Avtech, AVMP-2-C-P-EPIA) was split into two. One pulse was acquired by a 6 GHz oscilloscope as a timing reference while the other pulse was fed into the taper and its transmitted signal was acquired by another channel of the oscilloscope. We also compared the transmitted signal from the taper to the transmitted signal from a 50 Ω transmission line with the same length (corresponding to a delay of 94 ps), but made on a PCB. The delay difference between a PCB transmission line and the taper was 760 ps, which indicates the superconducting taper slowed down the average velocity to 11% of a PCB transmission line. The amplitude of the transmitted signal from a taper reduced to 60% of the transmitted signal from the PCB transmission line; however, the rising edge of the pulse was well preserved, which verifies that the taper helped the propagation of the fast pulse through a wire of mismatched impedance.
