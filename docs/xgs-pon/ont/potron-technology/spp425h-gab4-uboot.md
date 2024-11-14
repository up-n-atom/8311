---
hide:
  - navigation
  - toc
---

# SPP425H-GAB4

## Problem <small>Bugged U-boot</small> { #problem data-toc-label="Problem" } 

The SPP425H-GAB4 comes pre-flashed with a bugged U-boot that may trigger the U-boot shell rather than continue the boot
process into Linux when plugged into various host hardware.

!!! bug "Take notice of the ^^Hit any key to stop autoboot^^"

``` sh
ROM VER: 2.1.0
CFG 0d
B
DdrOk


U-Boot 2016.07-INTEL-v-3.1.210-8311 (Jul 08 2024 - 05:03:13 +0000), Build: prx126-sfp-qspi-nand-8311

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

Hit any key to stop autoboot:  0
8311 #
```

## Solution

The solution is to re-flash an OEM bootloader using a hardware host that does not trigger the event or that supports
serial USB such as the [SFP Media Buddy].

 [SFP Media Buddy]: https://whinis.com/sfp-buddy/

!!! note
    The OEM bootloaders from Azores and Potron use ++escape++ and ++enter++ respectively to abort auto boot and are
    highly unlikely to get triggered by a pulled up Rate Select 0 pin (7).

!!! tip "SFP Media Buddy or other serial breakout hardware"
    If the boot process is interrupted, you can continue it along by issuing the `boot` command over serial (hardware pending).

!!! tip "MikroTik RouterOS"
    MikroTik RouterOS sets the Rate Select 0 pin high by default.
    Interfaces > Ethernet > SFP > Rate Select > low

     ``` sh
     /interface ethernet sfp-rate-select low
     ```

1. Download the latest 8311 community release <https://github.com/djGrrr/8311-was-110-firmware-builder/releases/latest>.

2. Extract the bootloader from `whole-image.img` using Linux or WSL and verify it's integrity, i.e. `uboot-azores.bin: OK`.

    ``` sh
    dd if=whole-image.img of=uboot-azores.bin conv=notrunc bs=1 count=216400
    echo "e757517fb8152c0e7b4db57f9cbef0576e2ff76dd45eea76596eddbaeb9e7b8d uboot-azores.bin" | sha256sum -c
    ```

3. Transfer the extracted `uboot-azores.bin` to the now booted SPP425H-GAB4.

    ``` sh
    scp uboot-azores.bin root@192.168.11.1:/tmp/
    ```

4. SSH into the SPP425H-GAB4 and re-verify the transferred `/tmp/uboot-azores.bin`.

    ``` sh
    ssh root@192.168.11.1
    echo "e757517fb8152c0e7b4db57f9cbef0576e2ff76dd45eea76596eddbaeb9e7b8d /tmp/uboot-azores.bin" | sha256sum -c
    ```

5. Erase and flash the `/tmp/uboot-azores.bin` bootloader into `/dev/mtd0`.

    ``` sh
    flash_erase /dev/mtd0 0 0
    nandwrite /dev/mtd0 -p /tmp/uboot-azores.bin
    head -c 216400 /dev/mtd0 | sha256sum
    ```

6. Verify the integrity of the newly flashed bootloader `e757517fb8152c0e7b4db57f9cbef0576e2ff76dd45eea76596eddbaeb9e7b8d`.

    ``` sh
    head -c 216400 /dev/mtd0 | sha256sum
    ```

7. __DO NOT__ continue to reboot unless the checksums match!!!

    ``` sh
    reboot
    ```
