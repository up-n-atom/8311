---
date: 2024-11-02
categories:
  - XGS-PON
  - BFW Solutions
  - WAS-110
description: WAS-110 Multicast Upgrade and Recovery
---

# WAS-110 Multicast Upgrade and Community Firmware Recovery

<!-- !!! question "Forgot your root password?" -->

![WAS-110 Recovery](was-110-mulicast-upgrade-and-community-firmware-recovery/was_110_recovery.webp){ class="nolightbox" }

<!-- more -->
<!-- nocont -->

The [WAS-110] from the Azores factory includes a handy multicast upgrade utility baked into its U-boot bootloader,
including models from the following resellers:

* Azores Networks XSS
* E.C.I. Networks EN-XGSFPP-OMAC-V2
* FiberMall XGSPON-ONU-STICK

## Upgrade Sequence

The upgrade sequence is tied into the boot delay loop and therefore will not trigger if the [U-Boot] environment variable
`bootdelay` is less than or equal to zero (0); The default value is three (3).

<div class="grid" markdown>
  <div>
    <h5>OpenWrt</h5>
    ``` sh
    fw_printenv bootdelay
    ```
  </div>
  <div>
    <h5>U-Boot</h5>
    ``` sh
    env print bootdelay
    ```
  </div>
</div>

The upgrade sequence will wait 5 seconds for the first magic UDP packet on port `13456`. Each packet must include the
following header:

``` mermaid
packet-beta
title Multicast Upgrade Packet Header (st_upg_hdr)
0-31: "Sequence Number (ui_sn: 4 bytes, starts at 1)"
32-63: "Block Size (blk_sz: 4 bytes)"
64-95: "Unknown (4 bytes, must not be 0)"
96-127: "Image Size (img_sz: 4 bytes)"
128-287: "bfw-HGW\\0\\0\\0\\0\\0\\0\\0\\0\\0\\0\\0\\0\\0 (20 byte string)"
```

An ordered bit-map of the blocks received is updated from the sequence number along with the image size as the packets
can be sent and received non-sequentially.

Once all the blocks have been received the upgrade will commence from the final image stored at the hardcoded offset
`0x82000000`, otherwise set in the [U-Boot] environment variable `loadaddr` with the following command sequence:

``` sh
nand erase.part system_sw; run ubi_init; run switchbankA && upgrade 0x82000000 0x<size>
run switchbankB && upgrade 0x82000000 0x<size>
ubi remove rootfs_data && ubi create rootfs_data 0x2000000
```

## Image format

!!! note "The 8311 community firmware includes the multicast images, skip past to [Upgrade Script](#upgrade-script)"

The multicast image is a concatenated binary blob of the following uImage files: `kernel.bin`, `bootcore.bin`, and
`rootfs.img`.

**kernel.bin**

:       dumpimage -T kernel kernel.bin -o zImage
        7z e -so zImage > vmlinux
        mkimage -A MIPS -O Linux -T kernel -a 0xa0020000 -C lzma -e 0xa0020000 -n "PON_1.18.1" -d zImage kernel.bin

**bootcore.bin**

:       dumpimage -T kernel bootcore.bin -o u-boot.bin
        mkimage -A MIPS -O Linux -T kernel -a 0x88000000 -C none -e 0x88000000 -n "MIPS 4Kec Bootcore" -d u-boot.bin bootcore.bin

**rootfs.img**

:       unsquashfs -d rootfs rootfs.img
        mksquashfs
        mkimage -A MIPS -O Linux -T filesystem -C none -n "<version>" -d rootfs.squashfs rootfs.bin

## Upgrade Script

<script src="https://gist.github.com/djGrrr/802c5652d3610d3e0a63243fe1119c56.js"></script>

### Host setup

#### Download

!!! info "For use in conjunction with the 8311 community firmware"
    <https://github.com/djGrrr/8311-was-110-firmware-builder/releases/latest>

``` sh
curl https://gist.github.com/djGrrr/802c5652d3610d3e0a63243fe1119c56/raw/3d9feef42107232e0ef7f2a4c469a00e915a16d3/multicast_upgrader.py
chmod +x multicast_upgrader.py
```

#### Requirements

**10G SFP+ port**

:   !!! info
        The [WAS-110] SFP+ side is forced to **10GBASE-KR**[^1] in [U-Boot] as can be observed from the environment variable
        `lan1-xpcs-mode`.

        <h5>OpenWrt</h5>

        ``` sh
        fw_printenv lan1-xpcs-mode
        ```

        <h5>U-Boot</h5>

        ``` sh
        env print lan1-xpcs-mode
        ```

**Static IP address `192.168.1.2/24`**

:        ip address add 192.168.1.2/24 dev <interface>

    !!! info
        The default [WAS-110] IP address in [U-Boot] is `192.168.1.1` and can be retrieved from the environment variable
        `ipaddr`.

        <h5>OpenWrt</h5>

        ``` sh
        fw_printenv ipaddr

        ```
        <h5>U-Boot</h5>

        ``` sh
        env print ipaddr
        ```

**Static ARP entry**

:   **Unicast** (1 to 1)

        arp -s 192.168.1.1 00:E0:92:00:01:40

    **Multicast**

        arp -s 192.168.1.1 01:E0:92:00:01:40

    !!! info
        The default [WAS-110] MAC address in [U-Boot] is `00:E0:92:00:01:40` and can be retrieved from the environment variable
        `ethaddr`.

        <h5>OpenWrt</h5>

        ``` sh
        fw_printenv ethaddr
        ```

        <h5>U-Boot</h5>

        ``` sh
        env print ethaddr
        ```

### Usage

!!! warning "Without serial access, you'll be running blind"
    It's advisable to increase the wait time

#### Upgrade

1. Remove the [WAS-110]

2. Run the `multicast_upgrader.py` script

       ```
       ./multicast_upgrader.py --path=multicast_upgrade.img
       ```

3. Insert the [WAS-110]

4. Wait several minutes (3-5)

5. Press ++ctrl+x++ to end the `multicast_upgrader.py` script

6. Reseat the [WAS-110]

    ??? tip "Run a continuous ping"
        To recieve an early indication that the [WAS-110] has completed its first boot, run a continuous ping:

        ``` sh
        ping 192.168.11.1
        ```

#### Reset

!!! tip "Previous settings will be backed up and stored in `/ptconf`."

1. Remove the [WAS-110]

2. Run the `multicast_upgrader.py` script

       ```
       ./multicast_upgrader.py --path=multicast_reset.img
       ```

3. Insert the [WAS-110]

4. Wait several minutes (3-5)

5. Press ++ctrl+x++ to end the `multicast_upgrader.py` script

6. Reseat the [WAS-110]

    ??? tip "Run a continuous ping"
        To recieve an early indication that the [WAS-110] has completed its first boot, run a continuous ping:

        ``` sh
        ping 192.168.11.1
        ```

  [WAS-110]: ../xgs-pon/ont/bfw-solutions/was-110.md
  [U-Boot]: https://www.u-boot.org/

[^1]: https://en.wikipedia.org/wiki/10_Gigabit_Ethernet#10GBASE-KR
