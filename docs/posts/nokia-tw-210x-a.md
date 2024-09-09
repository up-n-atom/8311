---
date: 2024-09-08
categories:
  - Verizon
  - Nokia
  - TW-210X-A
description: Verizon Nokia TW-210X-A
---

# TL;DR
YO **Verizon users** if you have a **Nokia TW-210X-A** you can't use a WAS-110 your setup. It uses a different technology that does not have a current bypass.

# NOT COMPATIBLE
The Verizon (Nokia TW-210X-A) is a NGPON2 device that is not compatable with the WAS-110. This device uses the Next Generation of Passive Optical Network technology. Verizon is currently the only known user of this fiber stack, that uses wave lengths that are incompatable with the WAS-110 transciver. The Optical Transiver inside of the TW-210X-A is of the XFP form factor. The NGPON2 system uses 4 pairs of wavelengths, one is used by the the transciver in the TW-210X-A's XFP cage. Currently supporting this technology requires a large investment in hardware so it is not on the roadmap for the 8311 firmware.
