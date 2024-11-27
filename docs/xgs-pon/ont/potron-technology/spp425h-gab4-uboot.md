---
hide:
  - navigation
  - toc
---

# SPP425H-GAB4

## Problem <small>Bugged U-boot</small> { #problem data-toc-label="Problem" } 

Early SPP425H-GAB4 units *may* have had an experimental U-boot pre-flashed that may trigger the U-boot shell rather than
continue on with the boot process into OpenWrt when plugged into various host hardware, such as the Ubiquiti UDM-SE.

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
    The OEM bootloaders from Azores and Potron use ++escape++ and ++enter++ (or [password]) respectively to abort
    auto-boot and are highly unlikely to get triggered by a pulled-down Rate Select 0 pin (7).

 [password]: x-onu-sfpp.md#bootloader

!!! tip "SFP Media Buddy or other serial breakout hardware"
    If the boot process is interrupted, you can continue it along by issuing the `run bootcmd` command over serial.

!!! tip "MikroTik RouterOS"
    MikroTik RouterOS sets the Rate Select 0 pin high by default. If it was changed to low, try to revert back to default.
    Interfaces > Ethernet > SFP > Rate Select > high

     ``` sh
     /interface ethernet sfp-rate-select high
     ```

1. Download the latest 8311 community release <https://github.com/djGrrr/8311-was-110-firmware-builder/releases/latest>.

    !!! note
        The 8311 community firmware includes the Azores bootloader with the preboot multicast upgrade feature as
        described in the guide:

        [WAS-110 multicast upgrade and community firmware recovery](../../../posts/was-110-mulicast-upgrade-and-community-firmware-recovery.md)

2. Extract the bootloader from `whole-image.img` using Linux, macOS or WSL and verify it's integrity, i.e. `uboot-azores.bin: OK`.

    ``` sh
    dd if=whole-image.img of=uboot-azores.bin conv=notrunc bs=1 count=216400
    echo 'e757517fb8152c0e7b4db57f9cbef0576e2ff76dd45eea76596eddbaeb9e7b8d uboot-azores.bin' | sha256sum -c
    ```

3. Transfer the extracted `uboot-azores.bin` to the now booted SPP425H-GAB4.

    ``` sh
    scp uboot-azores.bin root@192.168.11.1:/tmp/
    ```

4. SSH into the SPP425H-GAB4 and verify the integrity of the transferred `/tmp/uboot-azores.bin`.

    ``` sh
    ssh root@192.168.11.1
    echo 'e757517fb8152c0e7b4db57f9cbef0576e2ff76dd45eea76596eddbaeb9e7b8d /tmp/uboot-azores.bin' | sha256sum -c
    ```

5. Erase and flash the `/tmp/uboot-azores.bin` bootloader into `/dev/mtd0`.

    ``` sh
    flash_erase /dev/mtd0 0 0
    nandwrite /dev/mtd0 -p /tmp/uboot-azores.bin
    ```

6. Verify the integrity of the newly flashed bootloader `e757517fb8152c0e7b4db57f9cbef0576e2ff76dd45eea76596eddbaeb9e7b8d`.

    ``` sh
    head -c 216400 /dev/mtd0 | sha256sum
    ```

7. __DO NOT__ continue to reboot unless the checksums match!!!

    ``` sh
    reboot
    ```
