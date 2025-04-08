---
date: 2025-04-03
categories:
  - XGS-PON
  - BGW620-700
  - WAS-110
  - AT&T
  - Vantiva
description: Masquerade as the AT&T Inc. BGW620-700 with the WAS-110
slug: masquerade-as-the-att-inc-bgw620-700-with-the-was-110
---

# Masquerade as the AT&T Inc. BGW620-700 with the WAS-110

![Bypass family](masquerade-as-the-att-inc-bgw620-700-with-the-was-110/bypass_bgw620.webp){ class="nolightbox" }

<!-- more -->
<!-- nocont -->

!!! warning "New Installations"
    Keep the BGW620-700 in active service for roughly a week or two until fully provisioned and the installation ticket
    has been closed.

## Determine if you're an XGS-PON subscriber

!!! info "2 Gbps or higher tiers"
    If you're subscribed to 2 GIG speed or a similar 2 Gbps or higher tier, skip past to [Purchase a WAS-110].

![BGW620-700 Fiber status](masquerade-as-the-att-inc-bgw620-700-with-the-was-110/bgw320_500_505_fiber_status.webp){ loading=lazy }

1. Within a web browser, navigate to
   <http://192.168.1.254/cgi-bin/fiberstat.ha>

If the wave length matches <em>1270 nm</em>, you're subscribed on XGS-PON.

## Purchase a WAS-110

!!! note
    The [WAS-110] is __NOT__ a substitute for a layer 7 router; It is an *ONT*, and its __ONLY__ function is to convert
    *Ethernet* to *PON* over fiber medium. Additional hardware and software are required to access the Internet.

The [WAS-110] is available from select [resellers]{ data-preview } worldwide.

 [resellers]: https://pon.wiki/xgs-pon/ont/bfw-solutions/was-110/#value-added-resellers

## Install community firmware

Although, not strictly necessary for AT&T, the community firmware is highly recommended for masquerading with the
WAS-110 and used for the remainder of this guide. To install the community firmware, follow the steps outlined in the
community firmware installation guide: [Install the 8311 community firmware on the WAS-110].

  [Install the 8311 community firmware on the WAS-110]: install-the-8311-community-firmware-on-the-was-110.md

## WAS-110 masquerade setup

To successfully masquerade on XGS-PON, the original ONT serial number is mandatory. It, along with other key
identifiers are available on the fiber stats page.

### from the web UI <small>recommended</small> { #from-the-web-ui data-toc-label="from the web UI"}

??? info "As of version 2.4.0 `https://` is supported and enabled by default"
    All `http://` URLs will redirect to `https://` unless the `8311_https_redirect` environment variable is set to
    0 or false.

<div class="swiper" markdown>

<div class="swiper-slide" markdown>

![WAS-110 login](shared-assets/was_110_luci_login.webp){ loading=lazy }

</div>

<div class="swiper-slide" markdown>

![WAS-110 8311 configuration](shared-assets/was_110_luci_config.webp){ loading=lazy }

</div>

<div class="swiper-slide" markdown>

![WAS-110 8311 configuration ISP Fixes](shared-assets/was_110_luci_config_fixes.webp){ loading=lazy }

</div>

</div>

1. Within a web browser, navigate to
   <https://192.168.11.1/cgi-bin/luci/admin/8311/config>
   and, if asked, input your <em>root</em> password.

2. From the __8311 Configuration__ page, on the __PON__ tab, fill in the configuration with the following values:

    !!! info "All attributes below are <ins>mandatory</ins>"

    | Attribute                  | Value                   | Remarks                 |
    | -------------------------- | -----------------       | ----------------------- |
    | PON Serial Number (ONT ID) | COMM&hellip;            |                         |
    | Equipment ID               | iONT620700X             |                         |
    | Hardware Version           | BGW620-700_2.5          |                         |
    | Sync Circuit Pack Version  | :check_mark:            |                         |
    | Software Version A         | BGW620_5.31.9           | [Version listing]       |
    | Software Version B         | BGW620_5.31.9           | [Version listing]       |
    | MIB File                   | /etc/mibs/prx300_1U.ini | PPTP i.e. default value |

3. From the __8311 Configuration__ page, on the __ISP Fixes__ tab, enable __Fix VLANs__ from the drop-down.

4. __Save__ changes and reboot from the __System__ menu.

### from the shell


1. Login over secure shell (SSH).

    ``` sh
    ssh root@192.168.11.1
    ```

2. Configure the 8311 U-Boot environment.

    !!! info "All attributes below are <ins>mandatory</ins>"

    ``` sh
    fwenv_set -8 gpon_sn COMM...
    fwenv_set -8 equipment_id iONT620700X
    fwenv_set -8 hw_ver BGW620-700_2.5
    fwenv_set -8 cp_hw_ver_sync 1
    fwenv_set -8 sw_verA BGW620_5.31.9
    fwenv_set -8 sw_verB BGW620_5.31.9
    fwenv_set -8 fix_vlans 1
    ```

    !!! info "Additional details and variables are described at the original repository [^1]"
        `/usr/sbin/fwenv_set` is a helper script that executes `/usr/sbin/fw_setenv` twice consecutively.

        The WAS-110 functions as an A/B system, requiring the U-Boot environment variables to be set twice, once for each
        environment.

        The `-8` option prefixes the U-Boot environment variable with `8311_`.

3. Verify the 8311 U-boot environment and reboot.

    ``` sh
    fw_printenv | grep ^8311
    reboot
    ```

After rebooting the WAS-110, safely remove the SC/APC cable from the BGW620-700 and connect it to the
WAS-110. If all previous steps were followed correctly, the WAS-110 should operate with O5.1 [PLOAM status].
For troubleshooting, please read the [Troubleshoot connectivity issues with the WAS-110] guide before seeking help on
the [8311 Discord community server].

  [PLOAM status]: troubleshoot-connectivity-issues-with-the-was-110.md#ploam-status
  [Troubleshoot connectivity issues with the WAS-110]: troubleshoot-connectivity-issues-with-the-was-110.md
  [8311 Discord community server]: https://discord.com/servers/8311-886329492438671420

!!! tip "Clone the BGW620-700 :purple_circle: __MAC address__ on the router's DHCP WAN interface to avoid waiting for the 20 minute lease to expire."

!!! note "Do not be alarmed..."
    If you receive an e-mail and/or text informing you to:

    > Check your AT&T Fiber equipment since you might be offline currently.

    The BGW620-700 sends telemetry data to *better* the customer experience.

## Software versions

The OLT *can* utilize the software version as a provisioning attribute. It is recommended to stay updated with the
software upgrades of the BGW620-700 if the WAS-110 reports a fake O5 state.

The software version can be acquired by reconnecting the BGW620-700 and navigating to
<http://192.168.1.254/cgi-bin/update.ha> and replacing the `X` placeholders in the following string pattern with the
version number: `BGW620_X.XX.X`.

{{ read_csv('docs/posts/masquerade-as-the-att-inc-bgw620-700-with-the-was-110/versions.csv') }}

  [Purchase a WAS-110]: #purchase-a-was-110
  [WAS-110]: ../xgs-pon/ont/bfw-solutions/was-110.md
  [Version listing]: #software-versions
  [Troubleshoot connectivity issues with the WAS-110]: troubleshoot-connectivity-issues-with-the-was-110.md

[^1]: <https://github.com/djGrrr/8311-was-110-firmware-builder>
