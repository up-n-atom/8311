---
date: 2024-05-02
categories:
  - Frontier
  - WAS-110
  - XGS-PON
  - FOX222
  - FRX523
  - CIG
  - XG-99M
slug: masquerade-as-the-frontier-comms-inc-fox222-frx523-with-the-bfw-solutions-was-110
---

# Masquerade as the Frontier Communications Inc. FOX222 or FRX523 with the BFW Solutions WAS-110

<!-- more -->
<!-- nocont -->

## Purchase a WAS-110

The WAS-110 is available from select distributors and at a discounted rate with group buys on the
[8311 Discord community server](https://discord.com/servers/8311-886329492438671420).

## Install community firmware

As a prerequisite to masquerading with the WAS-110, the community firmware is necessary; follow the steps
outlined in the community firmware installation guide:

[Install 8311 community firmware on the BFW Solutions WAS-110](install-8311-community-firmware-on-the-bfw-solutions-was-110.md)

## WAS-110 masquerade setup

To successfully masquerade on XGS-PON, the original ONT serial number is mandatory. It, along with other key
identifiers are available on the bottom label of the FOX222 or FRX523, color-coordinated in the following depiction:

<div id="fox222-frx523-label"></div>

=== "FOX222"

    ![FOX222 label](masquerade-as-the-frontier-comms-inc-fox222-frx523-with-the-bfw-solutions-was-110/fox222_label.webp){ class="nolightbox" }

=== "FRX523"

    ![FRX523 label](masquerade-as-the-frontier-comms-inc-fox222-frx523-with-the-bfw-solutions-was-110/frx523_label.webp){ class="nolightbox" }

### from the web UI <small>recommended</small> { #from-the-web-ui data-toc-label="from the web UI"}

![WAS-110 login](masquerade-as-the-bce-inc-home-hub-4000-on-xgs-pon-with-the-bfw-solutions-was-110/was_110_luci_login.webp)

1. Within a web browser, navigate to
   <https://192.168.11.1/cgi-bin/luci/admin/8311/config>
   and, if asked, input your <em>root</em> password.

    ??? info "As of version 2.4.0 `https://` is supported and enabled by default"
        All `http://` URLs will redirect to `https://` unless the `8311_https_redirect` environment variable is set to
        0 or false.

![WAS-110 8311 configuration](masquerade-as-the-bce-inc-home-hub-4000-on-xgs-pon-with-the-bfw-solutions-was-110/was_110_luci_config.webp)

2. From the __8311 Configuration__ page, on the __PON__ tab, fill in the configuration with the following values:

    !!! reminder
        <ins>Replace</ins> the :blue_circle: **PON serial number** with the provisioned values on the bottom [label] 
        of the FOX222 or FRX523.

    !!! info "All attributes below are mandatory to achieve O5 operation state"

    === "FOX222"

        | Attribute                  | Value                   | Remarks                 |
        | -------------------------- | ----------------------- | ----------------------- |
        | PON Serial Number (ONT ID) | FTRO0A0A803A            | :blue_circle:           |
        | Equipment ID               | FOX222                  |                         |
        | Hardware Version           | FOX222                  |                         |
        | Sync Circuit Pack Version  | :check_mark:            |                         |
        | Software Version A         | R4.4.08.030             | [Version listing]       |
        | Software Version B         | R4.4.08.030             | [Version listing]       |
        | Registration ID (HEX)      | 44454641554c54          | `DEFAULT` in hex        |
        | MIB File                   | /etc/mibs/prx300_1U.ini | PPTP i.e. default value |
        | Pon Slot                   | 10                      |                         |

    === "FRX523"

        | Attribute                  | Value                   | Remarks                 |
        | -------------------------- | ----------------------- | ----------------------  |
        | PON Serial Number (ONT ID) | FTRO27900CD6            | :blue_circle:           |
        | Equipment ID               | FRX523                  |                         |
        | Hardware Version           | FRX523                  |                         |
        | Sync Circuit Pack Version  | :check_mark:            |                         |
        | Software Version A         | R4.4.13.057             | [Version listing]       |
        | Software Version B         | R4.4.13.057             | [Version listing]       |
        | Registration ID (HEX)      | 44454641554c54          | `DEFAULT` in hex        |
        | MIB File                   | /etc/mibs/prx300_1U.ini | PPTP i.e. default value |
        | Pon Slot                   | 10                      |                         |

3. __Save__ changes and reboot from the __System__ menu.

Once rebooted, the SC/APC cable can safely be plugged into the WAS-110 and immediately receive O5 operational status.

### from the shell

<h4>Login over SSH</h4>

```sh
ssh root@192.168.11.1
```

<h4>Configure 8311 U-Boot environment</h4>

!!! reminder
    <ins>Replace</ins> the :blue_circle: __PON serial number__ with the provisioned values on the bottom [label] of 
    the FOX222 or FRX523.

!!! info "All attributes below are mandatory to achieve O5 operation state"

=== "FOX222"

    ``` sh
    fw_setenv 8311_gpon_sn FTRO0A0A803A
    fw_setenv 8311_equipment_id FOX222
    fw_setenv 8311_hw_ver FOX222
    fw_setenv 8311_cp_hw_ver_sync 1
    fw_setenv 8311_sw_verA R4.4.08.030 # (1)!
    fw_setenv 8311_sw_verB R4.4.08.030
    fw_setenv 8311_pon_slot 10
    fw_setenv 8311_reg_id_hex 44454641554c54
    ```

    1. [Version listing]

=== "FRX523"

    ``` sh
    fw_setenv 8311_gpon_sn FTRO27900CD6
    fw_setenv 8311_equipment_id FRX523
    fw_setenv 8311_hw_ver FRX523
    fw_setenv 8311_cp_hw_ver_sync 1
    fw_setenv 8311_sw_verA R4.4.13.057 # (1)!
    fw_setenv 8311_sw_verB R4.4.13.057
    fw_setenv 8311_pon_slot 10
    fw_setenv 8311_reg_id_hex 44454641554c54
    ```

    1. [Version listing]

!!! info "Additional details and variables are described at the original repository [^1]"
    `/usr/sbin/fwenv_set` is a helper script that executes `/usr/sbin/fw_setenv` twice consecutively.

    The WAS-110 functions as an A/B system, requiring the U-Boot environment variables to be set twice, once for each
    environment.

<h4>Verify and reboot</h4>

Prior to rebooting, verify that the 8311 environment variables are set correctly. If not, proceed to correct them with
the `fwenv_set` command as before.

```sh
fw_printenv | grep ^8311
reboot
```

Once rebooted, the SC/APC cable can safely be plugged into the WAS-110 and immediately receive O5 operational status.

## Software versions

The software version is used as a provisioning attribute by the OLT and must be kept up-to-date with the latest
version. Otherwise, upon a reboot, the WAS-110 will operate in a fake O5 state. 

=== "FOX222"

    | Software Version |
    | ---------------- |
    | R4.4.08.030      |
    | R4.4.08.025      |

=== "FRX523"

    | Software Version |
    | ---------------- |
    | R4.4.13.057      |
    | R4.4.13.051      |
    | R4.4.13.041      |

Please help us by contributing new versions via the
[8311 Discord community server](https://discord.com/servers/8311-886329492438671420)
or submitting a
[Pull Request](https://github.com/up-n-atom/8311/pulls) on GitHub.

  [label]: #fox222-frx523-label
  [Version listing]: #software-versions

[^1]: <https://github.com/djGrrr/8311-was-110-firmware-builder>
