## Install ONT firmware

You must first install the 8311 community firmware for VEIP support to masquerade as the {{ page.meta.ont }} on XGS-PON.

If you have a pre-flashed [WAS-110] or [X-ONU-SFPP], you can skip ahead.

=== "WAS-110"

    There are two (2) methods to install the 8311 community firmware onto the [WAS-110], outlined in the following guides:

    <div class="grid cards" markdown>

    -    __Method 1: <small>recommended</small>__

         [Install the 8311 community firmware on the WAS-110](install-the-8311-community-firmware-on-the-was-110.md)

    -    __Method 2__

         [WAS-110 multicast upgrade and community firmware recovery](was-110-mulicast-upgrade-and-community-firmware-recovery.md)

    </div>

=== "X-ONU-SFPP"

    The [X-ONU-SFPP] 8311 community firmware installation requires a two-step process and is more prone to failure or
    bricking.

    !!! warning "This process is not thoroughly documented and can lead to a bricked device"

    __Step 1: Install the Azores bootloader__

    :    Skip past to the solution in the following [issue tracker](../xgs-pon/ont/potron-technology/8311-uboot.md#solution)
         on how to install the Azores bootloader.

    __Step 2: Multicast upgrade__

    :    Follow through the [WAS-110 multicast upgrade and community firmware recovery](was-110-mulicast-upgrade-and-community-firmware-recovery.md)
         guide to install the 8311 community firmware.

  [WAS-110]: ../xgs-pon/ont/bfw-solutions/was-110.md
  [X-ONU-SFPP]: ../xgs-pon/ont/potron-technology/x-onu-sfpp.md
