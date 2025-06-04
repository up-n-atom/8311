---
date: 2025-04-03
categories:
  - XGS-PON
  - BGW620-700
  - WAS-110
  - AT&T
  - Vantiva
description: Masquerade as the AT&T Inc. BGW620-700 with the WAS-110 or HLX-SFPX
slug: masquerade-as-the-att-inc-bgw620-700-with-the-was-110
---

# Masquerade as the AT&T Inc. BGW620-700 with the WAS-110 or HLX-SFPX

![Bypass family](masquerade-as-the-att-inc-bgw620-700-with-the-was-110/bypass_bgw620.webp){ class="nolightbox" }

<!-- more -->
<!-- nocont -->

!!! warning "New Installations"
    Keep the BGW620-700 in active service for roughly a week or two until fully provisioned and the installation ticket
    has been closed.

???+ question "Common misconceptions and answers"

    __Can I take an SFP+ module provided by AT&T and plug it directly into my own router or switch?__

    :   No, the AT&T supplied SFP+ module is only a physical-layer transceiver compliant with XGS-PON
        ([ITU G.9807.1](../xgs-pon/index.md)). It lacks ONT management ([ITU G.988](../xgs-pon/index.md)), meaning it
        cannot function as a standalone ONT.

    __Do the WAS-110 or HLX-SFPX ONTs support GPON wavelengths, specifically 1490 nm downstream and 1310 nm upstream?__

    :   No, the BOSA in these ONTs is calibrated exclusively for XGS-PON wavelengths — 1577 nm downstream and
        1270 nm upstream. They use the Macom M02180 ([WAS-110]) and Semtech GN28L96 ([HLX-SFPX]) drivers, which are
        designed specifically for 10G PON ONT applications.

## Determine if you're an XGS-PON subscriber

!!! info "2 Gbps or higher tiers"
    If you're subscribed to 2 GIG speed or a similar 2 Gbps or higher tier, skip past to [Purchase a WAS-110].

![BGW620-700 Fiber status](masquerade-as-the-att-inc-bgw620-700-with-the-was-110/bgw320_500_505_fiber_status.webp){ loading=lazy }

1. Within a web browser, navigate to
   <http://192.168.1.254/cgi-bin/fiberstat.ha>

If the wave length matches <em>1270 nm</em>, you're subscribed on XGS-PON.

## Purchase a WAS-110 or HLX-SFPX

The [WAS-110] and [HLX-SFPX] are available from select resellers worldwide.
Purchase at your discretion; we take no responsibility or liability for the listed resellers.

[WAS-110 Value-Added Resellers](../xgs-pon/ont/bfw-solutions/was-110.md#value-added-resellers)

[HLX-SFPX Value-Added Resellers](../xgs-pon/ont/calix/100-05610.md#value-added-resellers)

!!! question "Is the WAS-110 or HLX-SFPX a router?"
    The [WAS-110] and [HLX-SFPX] are __NOT__ a substitute for a layer 7 router; They are an *ONT*, and their __ONLY__
    function is to convert *Ethernet* to *PON* over fiber medium. Additional hardware and software are required to access
    the Internet.

## Install firmware

=== "WAS-110"

    Although not strictly necessary for AT&T, the 8311 community firmware is highly recommended for masquerading as
    the BGW620-700 and used for the remainder of the WAS-110 sections of this guide.

    There are two (2) methods to install the 8311 community firmware onto the [WAS-110], outlined in the following guides:

    __Method 1: <small>recommended</small></h4>__

    :    [Install the 8311 community firmware on the WAS-110](install-the-8311-community-firmware-on-the-was-110.md)

    __Method 2:__

    :    [WAS-110 multicast upgrade and community firmware recovery](was-110-mulicast-upgrade-and-community-firmware-recovery.md)

=== "HLX-SFPX"

    [HALNy] has provided a custom firmware with satisfactory customization for masquerading as the BGW62-700.
    It's available by request from [HALNy] and has been made available for download on the
    [8311 Discord community server].

    1. Within a web browser, navigate to <https://192.168.33.1/> and, if asked, input the *useradmin*
       [web credentials]{ data-preview target="_blank" }.
    2. From the main navigation __System__ drop-down, click __Flash Firmware__.
    3. From the __Flash Firmware__ page, click __Choose Image__, browse for `HLX-SFPX_V7-0-6t1.zip`, and click
       __Flash__ to proceed with flashing the firwmare.
    4. Follow the prompts.

## Masquerade setup

To successfully masquerade on XGS-PON, the original ONT serial number is mandatory. It, along with other key
identifiers are available on the fiber stats page at:

<http://192.168.1.254/cgi-bin/fiberstat.ha>

=== "WAS-110"

    Choose your preferred setup method: [web UI](#from-the-web-ui) or [shell](#from-the-shell) and carefully follow the
    steps to avoid unnecessary downtime and troubleshooting.

    <h3 id="from-the-web-ui">from the web UI <small>recommended</small></h3>

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

    ![WAS-110 8311 configuration ISP fixes](shared-assets/was_110_luci_config_fixes.webp){ loading=lazy }

    </div>

    <div class="swiper-slide" markdown>

    ![WAS-110 8311 reboot](shared-assets/was_110_luci_reboot.webp){ loading=lazy }

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

    4. __Save__ changes and *reboot* from the __System__ menu.

    <h3 id="from-the-shell">from the shell</h3>

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

            The WAS-110 functions as an A/B system, requiring the U-Boot environment variables to be set twice, once
            for each environment.

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

=== "HLX-SFPX"

    ![HLX-SFPX custom values](shared-assets/hlx_sfpx_settings.webp){ loading=lazy }

    1. Within a web browser, navigate to <https://192.168.33.1/> and, if asked, input the *useradmin*
       [web credentials]{ data-preview target="_blank" }.
    2. From the main navigation click __System__.
    3. From the __System__ page, in the __Custom values__ section, fill in the configuration with the following values:

        !!! info "All parameters below are <ins>mandatory</ins>"

        | Parameter                  | Value                   | Remarks                 |
        | -------------------------- | -----------------       | ----------------------- |
        | State                      | Enable                  |                         |
        | PON Serial Number          | COMM&hellip;            |                         |
        | Equipment ID               | iONT620700X             |                         |
        | Hardware Version           | BGW620-700_2.5          |                         |
        | Sync Circuit Pack Version  | Enable                  |                         |
        | Software Version A         | BGW620_5.31.9           | [Version listing]       |
        | Software Version B         | BGW620_5.31.9           | [Version listing]       |

    4. Click __Save & Reboot__ to apply the parameters.

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
  [HLX-SFPX]: ../xgs-pon/ont/calix/100-05610.md
  [HALNy]: https://halny.com/
  [Version listing]: #software-versions
  [Troubleshoot connectivity issues with the WAS-110]: troubleshoot-connectivity-issues-with-the-was-110.md
  [web credentials]: ../xgs-pon/ont/calix/100-05610.md#web-credentials

[^1]: <https://github.com/djGrrr/8311-was-110-firmware-builder>
