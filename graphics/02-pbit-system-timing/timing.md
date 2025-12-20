![timing](timing.png){ width="400px #fig:label}

The measurement scheme consists of modules:

1. PC for control and readout
2. SR-860 Lock-in as a generator outputting a mixture of clock AC and control DC signals
3. SBN (nanowire)
4. Amp-comp combined into one module with Arduino used for receiving data from the comparator and transmitting to the PC

Regarding timing:
The full system response time to changes is about 20ms. This was verified as follows: the control signal was changed from one that gives a guaranteed response of 0 to one that gives a guaranteed response of 1, and we observed when a 1 appeared in the response.

Known characteristic times:

- 10μs or 100kHz maximum operating frequency of Arduino
- 7ns or 130MHz maximum operating frequency of the comparator chip
- The slowest element in the circuit is the Lock-in. Characteristic signal processing times to set DC level are 10-100ms depending on the level difference.

### Summary

Full cycle 20ms.

- Lock-in : 10-100ms
- Arduino : 10μs or 100kHz
- comparator : 7ns or 130MHz
