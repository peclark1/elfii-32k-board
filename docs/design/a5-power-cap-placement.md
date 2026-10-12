# A5 power planes and decoupling placement — validation checkpoint

Five 100 nF decoupling capacitors were relocated near their intended HCT/SRAM packages:

| Capacitor | New centre (mm) | Device |
|---|---:|---|
| C1 | 100.5, 45.72 | U1 74HCT273 |
| C2 | 169, 47 | U2 62256 |
| C3 | 80, 95.76 | U3 74HCT04 |
| C4 | 112, 95.76 | U4 74HCT86 |
| C5 | 143, 95.76 | U5 74HCT32 |

The original first-pass copper traces do not intentionally terminate at these VCC/GND bypass capacitor pads. Before moving, automated geometric comparison estimated greater than 2.8 mm clearance from all foreign signal traces at the proposed footprints. Refill power/ground zones and rerun actual KiCad DRC to verify.

The PCB now has F.Cu ground pour, B.Cu +5 V pour, a short wide F.Cu connection from the front edge power finger to a plated power via, and a B.Cu connection from the back ground finger to an F.Cu ground via.

**Not released:** The ten remaining address/data signal nets are still not routed. DRC must verify filled +5V/GND copper is connected and there are no new shorts, thermal issues or clearance violations. Real footprint libraries, period bus and TPA timing still require review.
