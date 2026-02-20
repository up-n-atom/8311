## Install ONT firmware

You must first install the 8311 community firmware for VEIP support to masquerade as the {{ page.meta.ont }} on XGS-PON.

!!! note "Upgrading a pre-flashed 8311 WAS-110 or X-ONU-SFPP"
    If your [WAS-110] came with 8311 firmware pre-installed, you do not need to follow the full installation guide
    below. Instead, you can go directly to the [Supplementary Upgrades] section to re-install the
    [official 8311 community build] to both A and B partitions.

  [official 8311 community build]: https://github.com/djGrrr/8311-was-110-firmware-builder/releases/latest
  [Supplementary Upgrades]: install-the-8311-community-firmware-on-the-was-110.md#supplementary-upgrades

=== "WAS-110"

    There are two (2) methods to install the 8311 community firmware onto the [WAS-110], outlined in the following guides:

    <div class="grid cards" markdown>

    -    __Method 1: <small>recommended</small>__

         [Install the 8311 community firmware on the WAS-110](install-the-8311-community-firmware-on-the-was-110.md)

    -    __Method 2__

         [WAS-110 multicast upgrade and community firmware recovery](was-110-multicast-upgrade-and-community-firmware-recovery.md)

    </div>

=== "X-ONU-SFPP"

    The [X-ONU-SFPP] 8311 community firmware installation requires a two-step process and is more prone to failure or
    bricking.

    !!! warning "This process is not thoroughly documented and can lead to a bricked device"

    __Step 1: Install the Azores bootloader__

    :    Skip past to the solution in the following [issue tracker](../xgs-pon/ont/potron-technology/8311-uboot.md#solution)
         on how to install the Azores bootloader.

    __Step 2: Multicast upgrade__

    :    Follow through the [WAS-110 multicast upgrade and community firmware recovery](was-110-multicast-upgrade-and-community-firmware-recovery.md)
         guide to install the 8311 community firmware.

  [WAS-110]: ../xgs-pon/ont/bfw-solutions/was-110.md
  [X-ONU-SFPP]: ../xgs-pon/ont/potron-technology/x-onu-sfpp.md
