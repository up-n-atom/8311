---
date: 2024-03-22
categories:
  - XGS-PON
  - Home Hub 4000
  - Vincent
  - WAS-110
  - Bell Canada
  - Bell Aliant
  - Bell MTS
  - Virgin Plus
  - Sagemcom
  - FAST 5689
description: Masquerade as the BCE Inc. Home Hub 4000 with the WAS-110 or X-ONU-SFPP
slug: masquerade-as-the-bce-inc-home-hub-4000-with-the-was-110
links:
  - xgs-pon/index.md
  - posts/troubleshoot-connectivity-issues-with-the-was-110.md
  - posts/masquerade-as-the-bce-inc-giga-hub-with-the-was-110.md
ont: Home Hub 4000
---

# Masquerade as the BCE Inc. Home Hub 4000 with the WAS-110 or X-ONU-SFPP

!!! info "Including the rebadged Virgin Plus Vincent"

![Bypass family]({{ page.meta.slug }}/bypass_{{ page.meta.ont | lower | replace(" ", "_") }}.webp){ class="nolightbox" }

<!-- more -->
<!-- nocont -->

{% include 'bce-inc-hub/determine-pon.md' %}

{% include 'bce-inc-hub/purchase-ont.md' %}

{% include 'bce-inc-hub/install-ont-fw.md' %}

## Configure ONT settings

To masquerade as the {{ page.meta.ont }}, you will need its ONT serial number, which is located on the back label along
with other, optional identifiers, as depicted below.

![{{ page.meta.ont }} label]({{ page.meta.slug }}/{{ page.meta.ont | lower | replace(" ", "_") }}_label.webp){ class="nolightbox" id="{{ page.meta.ont | lower | replace(" ", "-") }}-label" }

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

    !!! reminder
        <ins>Replace</ins> the :blue_circle: mandatory __PON Serial Number__ and optional :purple_circle:
        __IP Host MAC address__ with the provisioned values on the back [label] of the Home Hub 4000.

    | Attribute                  | Value                        | Mandatory    | Remarks                         |
    | -------------------------- | ---------------------------- | ------------ |-------------------------------- |
    | PON Serial Number (ONT ID) | SMBS&hellip;                 | :check_mark: | :blue_circle: ONT S/N           |
    | Equipment ID               | 5689                         |              |                                 |
    | Hardware Version           | Fast5689Bell                 |              |                                 |
    | Sync Circuit Pack Version  | :check_mark:                 |              |                                 |
    | Software Version A         | SGC8210154                   |              | [Version listing]               |
    | Software Version B         | SGC8210154                   |              | [Version listing]               |
    | MIB File                   | /etc/mibs/prx300_1V_bell.ini | :check_mark: | VEIP and more                   |
    | IP Host MAC Address        | 40:65:A3:FF:A7:B1            |              | :purple_circle: @MAC + 1        |

3. From the __8311 Configuration__ page, on the __ISP Fixes__ tab, enable __Fix VLANs__ from the drop-down.

4. __Save__ changes and *reboot* from the __System__ menu.

### Via shell { #config-via-shell }

1. Login over secure shell (SSH).

    ``` sh
    ssh root@192.168.11.1
    ```

2. Configure the 8311 U-Boot environment.

    !!! reminder "Highlighted lines are <ins>mandatory</ins>"
        <ins>Replace</ins> the mandatory :blue_circle: __8311_gpon_sn__ and optional :purple_circle:
        __8311_iphost_mac__ with the provisioned values on the back [label] of the Home Hub 4000.

    ``` sh hl_lines="1 3 9 10"
    fwenv_set mib_file
    fwenv_set -8 iphost_mac 40:65:A3:FF:A7:B1 # (1)!
    fwenv_set -8 gpon_sn SMBS... # (2)!
    fwenv_set -8 equipment_id 5689
    fwenv_set -8 hw_ver Fast5689Bell
    fwenv_set -8 cp_hw_ver_sync 1
    fwenv_set -8 sw_verA SGC8210154 # (3)!
    fwenv_set -8 sw_verB SGC8210154
    fwenv_set -8 mib_file /etc/mibs/prx300_1V_bell.ini
    fwenv_set -8 fix_vlans 1
    ```

    1. :purple_circle: @MAC + 1, e.g. `40:65:A3:FF:A7:B0` becomes `40:65:A3:FF:A7:B1`
    2. :blue_circle: ONT S/N
    2. [Version listing]

3. Verify the 8311 U-boot environment and reboot.

    ``` sh
    fw_printenv | grep ^8311
    reboot
    ```

  [Version listing]: #software-versions
  [password]: ../xgs-pon/ont/bfw-solutions/was-110.md#web-credentials
  [label]: #{{ page.meta.ont | lower | replace(" ", "-") }}-label

{% include 'bce-inc-hub/verify-ont.md' %}

{% include 'bce-inc-hub/home-phone.md' %}

{% include 'bce-inc-hub/router-tips.md' %}

{% include 'bce-inc-hub/switch-tips.md' %}

{% include 'bce-inc-hub/software-ver.md' %}

{{ read_csv('docs/posts/masquerade-as-the-bce-inc-home-hub-4000-with-the-was-110/versions.csv') }}

  [WAS-110]: ../xgs-pon/ont/bfw-solutions/was-110.md
  [X-ONU-SFPP]: ../xgs-pon/ont/potron-technology/x-onu-sfpp.md
