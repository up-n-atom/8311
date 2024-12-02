---
hide:
  - navigation
  - toc
---

# Issue 1

## Problem <small>stop auto-boot</small> { #problem data-toc-label="Problem" }

Pressing ++enter++ does not stop auto-boot.

``` sh
ROM VER: 2.1.0
CFG 0d
B
DdrOk


U-Boot 2016.07-MXL-v-3.1.261 (Apr 10 2023 - 10:00:42 +0000), Build: prx126-eva-qspi-nand

interAptiv
cps cpu/ddr run in 400/400 Mhz
       Watchdog enabled
DRAM:  256 MiB
NAND:  device found, Manufacturer ID: 0xef, Chip ID: 0xaa
128 MiB
Bad block table found at page 65472, version 0x01
Bad block table found at page 65408, version 0x01
In:    serial
Out:   serial
Err:   serial
Reset cause: POR RESET
Net:   lan-0 config to 1G_XAUI_MODE, lan-1 config to 10G_KR_MODE, prx300-eth

run flash_flash to bring up the kernel

Hit enter to stop autoboot:  0
```

## Solution

The Potron U-boot auto-boot escape is protected by a password. Instead of ++enter++ type `admin` to stop auto-boot.
