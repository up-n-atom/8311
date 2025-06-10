---
date: 2024-06-23
categories:
  - XGS-PON
  - Hub 5x
  - WAS-110
  - Virgin Media
  - Sagemcom
  - FAST 5685
  - F5685LGB-VMB
  - F5685LGB-VMIE
description: Masquerade as the Virgin Media O2 Hub 5x with the WAS-110 or X-ONU-SFPP
slug: masquerade-as-the-virgin-media-o2-hub-5x-with-the-was-110
ont_name: Hub 5x
---

# Masquerade as the Virgin Media O2 Hub 5x with the WAS-110 or X-ONU-SFPP

![Bypass Hub 5x](masquerade-as-the-virgin-media-o2-hub-5x-with-the-bfw-solutions-was-110/bypass_hub_5x.webp){ class="nolightbox" }

<!-- more -->
<!-- nocont -->

{% include-markdown '../assets/common/purchase-ont.md' %}

{% include-markdown '../assets/common/lc-connector-warning.md' %}

{% include-markdown '../assets/common/install-8311.md' %}

## Masquerade setup

To successfully masquerade on XGS-PON, the original ONT serial number is mandatory. It, along with other key
identifiers are available on the bottom label of the Hub 5x, color-coordinated in the following depiction:

<div id="hub-5x-label"></div>

![Hub 5x label](masquerade-as-the-virgin-media-o2-hub-5x-with-the-bfw-solutions-was-110/hub_5x_label.webp){ class="nolightbox" id="hub-5x-label" }

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

    !!! reminder "Reminder"
        <ins>Replace</ins> the mandatory :blue_circle: __PON Serial Number__ with the provisioned value on the bottom
        [label] of the Hub 5x.

    | Attribute                  | Value                         | Mandatory    | Remarks                 |
    | -------------------------- | ----------------------------- | ------------ | ----------------------- |
    | PON Serial Number (ONT ID) | SMBS&hellip;                  | :check_mark: | :blue_circle: PON S/N   |
    | Equipment ID               | F5685LGB                      |              |                         |
    | Hardware Version           | 1.2.1b                        |              |                         |
    | Sync Circuit Pack Version  | :check_mark:                  |              |                         |
    | Software Version A         | 3.7.4-2306.5                  |              | [Version listing]       |
    | Software Version B         | 3.7.4-2306.5                  |              | [Version listing]       |
    | MIB File                   | /etc/mibs/prx300_1V_bell.ini  | :check_mark: | VEIP and more           |

3. From the __8311 Configuration__ page, on the __ISP Fixes__ tab, disable __Fix VLANs__ from the drop-down.

4. __Save__ changes and *reboot* from the __System__ menu.

### from the shell

1. Login over secure shell (SSH).

    ``` sh
    ssh root@192.168.11.1
    ```

2. Configure the 8311 U-Boot environment.

    !!! reminder "Highlighted lines are <ins>mandatory</ins>"
        <ins>Replace</ins> the mandatory :blue_circle: __8311_gpon_sn__ with the provisioned value on the bottom
        [label] of the Hub 5x.

    ``` sh hl_lines="1 2 8 9"
    fwenv_set mib_file
    fwenv_set -8 gpon_sn SMBS... # (1)!
    fwenv_set -8 equipment_id F5685LGB
    fwenv_set -8 hw_ver 1.2.1b
    fwenv_set -8 cp_hw_ver_sync 1
    fwenv_set -8 sw_verA 3.7.4-2306.5 # (2)!
    fwenv_set -8 sw_verB 3.7.4-2306.5
    fwenv_set -8 mib_file /etc/mibs/prx300_1V_bell.ini
    fwenv_set -8 fix_vlans 0
    ```

    1. :blue_circle: PON S/N
    2. [Version listing]

    !!! info "Additional details and variables are described at the original repository [^2]"
        `/usr/sbin/fwenv_set` is a helper script that executes `/usr/sbin/fw_setenv` twice consecutively.

        The WAS-110 functions as an A/B system, requiring the U-Boot environment variables to be set twice, once for each
        environment.

        The `-8` option prefixes the U-Boot environment variable with `8311_`.

3. Verify the 8311 U-boot environment and reboot.

    ``` sh
    fw_printenv | grep ^8311
    reboot
    ```

After rebooting the WAS-110, safely remove the SC/APC cable from the Hub 5x and connect it to the
WAS-110. If all previous steps were followed correctly, the WAS-110 should operate with O5.1 [PLOAM status].
For troubleshooting, please read the [Troubleshoot connectivity issues with the WAS-110] guide before seeking help on
the [8311 Discord community server].

  [PLOAM status]: troubleshoot-connectivity-issues-with-the-was-110.md#ploam-status
  [Troubleshoot connectivity issues with the WAS-110]: troubleshoot-connectivity-issues-with-the-was-110.md

!!! note "Clone the Hub 5x :purple_circle: MAC address on the router's DHCP WAN interface and tag it and anything in-between the WAS-110 with VLAN 100 in the United Kingdom and VLAN 10 in the Republic of Ireland."

## Hub 5x software versions

The software version <ins>can</ins> be utilized as a provisioning attribute by the OLT, but this is not the case for
the Hub 5x, which uses CWMP[^3]. However, it is recommended to keep somewhat up-to-date with the following listing, but
it is not strictly necessary.

| Software Version |
| ---------------- |
| 3.7.4-2306.5     |

Please help us by contributing new versions via the [8311 Discord community server] or submitting a
[Pull Request](https://github.com/up-n-atom/8311/pulls) on GitHub.

  [WAS-110]: ../xgs-pon/ont/bfw-solutions/was-110.md
  [X-ONU-SFPP]: ../xgs-pon/ont/potron-technology/x-onu-sfpp.md
  [label]: #hub-5x-label
  [Version listing]: #hub-5x-software-versions
  [8311 Discord community server]: https://discord.com/servers/8311-886329492438671420

[^1]: <https://www.servethehome.com/apc-and-upc-in-fiber-connectors-and-why-this-matters/>
[^2]: <https://github.com/djGrrr/8311-was-110-firmware-builder>
[^3]: <https://en.wikipedia.org/wiki/TR-069>
