---
title: "Template (Ignored)"
date: 1970-01-01
draft: true
---

<!-- more -->

# --8<-- [start:purchase-ont]
## Purchase a WAS-110 or X-ONU-SFPP

The [WAS-110] and [X-ONU-SFPP] are available from select resellers worldwide. To streamline the process, some resellers
are pre-flashing the 8311 community firmware and highly recommended for the [X-ONU-SFPP]. Purchase at your discretion;
we take no responsibility or liability for the listed resellers.

[WAS-110 Value-Added Resellers](../xgs-pon/ont/bfw-solutions/was-110.md#value-added-resellers)

[X-ONU-SFPP Value-Added Resellers](../xgs-pon/ont/potron-technology/x-onu-sfpp.md#value-added-resellers)

!!! question "Is the WAS-110 or X-ONU-SFPP a router?"
    The [WAS-110] and [X-ONU-SFPP] are __NOT__ a substitute for a layer 7 router; They are an *ONT*, and their __ONLY__
    function is to convert *Ethernet* to *PON* over fiber medium. Additional hardware and software are required to access
    the Internet.
# --8<-- [end:purchase-ont]


# --8<-- [start:lc-warning]
!!! warning "APC and UPC connectors are not equal nor compatible[^1]"

A Female LC/APC to Male SC/APC adapter is necessary for connecting to the [WAS-110] or [X-ONU-SFPP] with the
provisioned LC/APC cable, or a Male LC/APC to Male SC/APC patch cable, both of which can be purchased at
<https://www.amazon.co.uk/>.
# --8<-- [start:lc-warning]

# --8<-- [start:install-8311]
## Install the 8311 community firmware

As a prerequisite to masquerading, the 8311 community firmware is recommended and required for the remainder
of this guide. If you purchased a pre-flashed [WAS-110] or [X-ONU-SFPP], skip past to the [masquerade setup](#masquerade-setup).

=== "WAS-110"

    There are two methods to install the 8311 community firmware onto the [WAS-110], outlined in the following guides:

    __Method 1: <small>recommended</small></h4>__

    :    [Install the 8311 community firmware on the WAS-110](install-the-8311-community-firmware-on-the-was-110.md)

    __Method 2:__

    :    [WAS-110 multicast upgrade and community firmware recovery](was-110-mulicast-upgrade-and-community-firmware-recovery.md)

=== "X-ONU-SFPP"

    The [X-ONU-SFPP] 8311 community firmware installation requires a two-step process and is more prone to failure and
    bricking.

    !!! warning "This process is not thoroughly documented and can lead to a bricked device"

    __Step 1: Install the Azores bootloader__

    :    Skip past to the solution in the following [issue tracker](../xgs-pon/ont/potron-technology/8311-uboot.md#solution)
         on how to install the Azores bootloader.

    __Step 2: Multicast upgrade__

    :    Follow through the [WAS-110 multicast upgrade and community firmware recovery](was-110-mulicast-upgrade-and-community-firmware-recovery.md)
         guide to install the 8311 community firmware.
# --8<-- [start:install-8311]
