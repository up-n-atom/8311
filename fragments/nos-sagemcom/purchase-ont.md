## Purchase WAS-110/X-ONU-SFPP/HLX-SFPX ONT { #purchase-was-110-hlx-sfpx-ont }

The [WAS-110] and [HLX-SFPX] are available from select resellers worldwide; purchase at your discretion. We assume no
responsibility or liability for the listed resellers.

??? info "Purchase SC/APC variant; if unavailable, add an SC/APC (female) to SC/UPC (male) 0dB attenuator for conversion."
    AT&T and most North American ISPs terminate their fiber at the ONT using SC/APC (green) connectors.

    Angled Physical Contact (APC) tips are polished to 8 degrees. This eliminates signal reflections on the
    fiber.

    !!! warning "Never mismatch SC/APC (green) and SC/UPC (blue). This causes signal loss and can permanently damage the fiber faces."

??? quote "HALNy issued a statement on 2025-09-23 concerning the firmware problems and resolution with the HLX-SFPX."
    > The HLX-SFPX firmware suffers from I/O errors that corrupt the overlay filesystem, soft-bricking the module.

    First of all we want to thank you for all your effort during the tests of our product HLX-SFPX. We are impressed by all your experience and knowledge about GPON/XGS-PON ONTs and embedded devices

    All HALNy products are designed to meet the ISP(Internet Service Providers) requirements.
    In terms of GPON/XGS-PON ONTs, based on the standard, they are fully managed by the ISP (from the OLT side)

    Although our goal is to support ISPs - we decided to make some exception and implement some of the request from end users on best-effort basis.

    Unlucky V7.0.6t1. version dedicated to end-users was released to fast to community - causing issue with unable to login on LAN side. The problem is not always present and few actions need to happen to reveal it.
    The device is not bricked, it will work, pass the traffic, just not possible to login. On version V7.0.7p2 please be careful when you copy the data from the other device. Wrong data may affects OMCI communication which cause not passing the traffic and login to fail.

    We released the new firmware version V7.0.8pt2, which doesn't have this issue:

    <https://active-fw.fibrain.pl/aktywa/MATERIALY/HALNy/HLX-SFPX/FIRMWARE/HLX-SFPX_V7-0-8pt2.zip>

    We strongly recommend to update product to above version.

    Again apologize for all inconvenience. We are really amazed with these community! Keep it going.

    In case of any problem with HALNy products please contact with our support team: <support@halny.com>

<div class="grid cards" markdown>

-    __WAS-110__

     [Value-Added Resellers](../xgs-pon/ont/bfw-solutions/was-110.md#value-added-resellers)

-    __HLX-SFPX__

     [Value-Added Resellers](../xgs-pon/ont/calix/100-05610.md#value-added-resellers)

-    __X-ONU-SFPP <small>WAS-110 substitute</small>__

     [Value-Added Resellers](../xgs-pon/ont/potron-technology/x-onu-sfpp.md#value-added-resellers)

     ---

     :flag_gb: [EXEN Shop](https://store.betterinternet.ltd/product/x-onu-sfpp/?affiliates=6) <small class="affiliate"></small>

</div>

  [WAS-110]: ../xgs-pon/ont/bfw-solutions/was-110.md
  [HLX-SFPX]: ../xgs-pon/ont/calix/100-05610.md
