---
date: 2026-02-27
categories:
  - XGS-PON
  - Fiber Box X6
  - WAS-110
  - Salt Mobile SA
  - Sagemcom
description: Masquerade as the Salt Mobile SA Fiber Box X6 with the WAS-110 or X-ONU-SFPP
slug: masquerade-as-the-salt-mobile-sa-fiber-box-x6-with-the-was-110
links:
  - xgs-pon/index.md
  - posts/accessing-the-ont.md
  - posts/troubleshoot-connectivity-issues-with-the-was-110.md
ont: Fiber Box X6
---

# Masquerade as the Salt Mobile SA Fiber Box X6 with the WAS-110 or X-ONU-SFPP

![Bypass family]({{ page.meta.slug }}/bypass_{{ page.meta.ont | lower | replace(" ", "_") }}.webp){ class="nolightbox" }

<!-- more -->
<!-- nocont -->

{% include 'salt-sa-box/determine-pon.md' %}

{% include 'salt-sa-box/purchase-ont.md' %}

{% include 'salt-sa-box/pre-config.md' %}

{% include 'bce-inc-hub/install-ont-fw.md' %}

## Configure ONT settings

To masquerade as the {{ page.meta.ont }}, you will need its ONT serial number and other identifiers you [extracted]
previously.

  [extracted]: #extract-required-attributes

Use your preferred setup method and carefully follow the steps to avoid unnecessary downtime and troubleshooting:

* [Web (luci)](#config-via-web)
* [Shell (linux)](#config-via-shell)

### Via web <small>recommended</small> { #config-via-web data-toc-label="Via web"}

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
   and, if asked, input your *root* [password]{ data-preview target="_blank" }.

2. From the __8311 Configuration__ page, on the __PON__ tab, fill in the configuration with the following values:

    !!! info "All attributes below are <ins>mandatory</ins>"

    | Attribute                  | Value                        | Remarks                         |
    | -------------------------- | ---------------------------- | ------------------------------- |
    | PON Serial Number (ONT ID) | GFAB&hellip;                 | [PON serial number]             |
    | Equipment ID               | NJJ Fibre Box                |                                 |
    | Hardware Version           | XGSR1644                     |                                 |
    | Sync Circuit Pack Version  | :check_mark:                 |                                 |
    | Software Version A         | SGCk10005062                 | [Software Versions]             |
    | Software Version B         | SGCk100041C6                 | [Software Versions]             |
    | MIB File                   | /etc/mibs/prx300_1V_bell.ini | [ONU mode]                      |
    | IP Host MAC Address        | AA:BB:CC:DD:EE:FF            | Found on [Transciever] label    |

3. From the __8311 Configuration__ page, on the __ISP Fixes__ tab, disable __Fix VLANs__ from the drop-down.

    ??? tip "Identify VLANs (Optional: Salt uses VLAN `30` for Internet and `40` for VOIP"
        Once configuration is complete and the fiber is connected, wait for successful authentication (__O5 state__).
        You can then use the [VLAN Table Analyser](../tools/vlan.md) to identify service VLANs by copying the table
        from the VLANs page (<https://192.168.11.1/cgi-bin/luci/admin/8311/vlans>) and pasting it into the tool.

4. __Save__ changes and *reboot* from the __System__ menu.

### Via shell { #config-via-shell }

1. Login over secure shell (SSH).

    ``` sh
    ssh root@192.168.11.1
    ```

2. Configure the 8311 U-Boot environment.

    !!! info "All attributes below are <ins>mandatory</ins>"

    ``` sh
    fwenv_set mib_file
    fwenv_set -8 iphost_mac AA:BB:CC:DD:EE:FF #(1)!
    fwenv_set -8 gpon_sn GFAB... #(2)!
    fwenv_set -8 equipment_id "NJJ Fibre Box"
    fwenv_set -8 hw_ver XGSR1644
    fwenv_set -8 cp_hw_ver_sync 1
    fwenv_set -8 sw_verA SGCk10005062 #(3)!
    fwenv_set -8 sw_verB SGCk100041C6 #(3)!
    fwenv_set -8 mib_file /etc/mibs/prx300_1V_bell.ini #(4)!
    fwenv_set -8 fix_vlans 0
    ```

    1. Found on [Transceiver] label
    2. [PON serial number]
    3. [Software Versions]
    4. [ONU mode]

  [PON serial number]: #pon-serial-number
  [Software versions]: #software-versions
  [ONU mode]: #onu-mode
  [Transceiver]: #via-transceiver

3. Verify the 8311 U-boot environment and reboot.

    ``` sh
    fw_printenv | grep ^8311
    reboot
    ```

  [Version listing]: #software-versions
  [password]: ../xgs-pon/ont/bfw-solutions/was-110.md#web-credentials
  [label]: #{{ page.meta.ont | lower | replace(" ", "-") }}-label

{% include 'bce-inc-hub/verify-ont.md' %}

{% include 'salt-sa-box/router-tips.md' %}

{% include 'bce-inc-hub/switch-tips.md' %}

---

Based on contributions from **T G** (8311 Discord), this guide is subject to change. Please note that some details may
be incomplete or superseded by newer firmware versions.
