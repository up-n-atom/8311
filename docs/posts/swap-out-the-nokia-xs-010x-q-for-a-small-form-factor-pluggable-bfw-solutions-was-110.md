---
date: 2024-08-11
categories:
  - XGS-PON
  - XS-010X-Q
  - WAS-110
  - NOKIA
description: Swap out the Nokia XS-010X-Q for a Small Form-factor Pluggable BFW Solutions WAS-110
---

# Swap out the Nokia XS-010X-Q for a Small Form-factor Pluggable BFW Solutions WAS-110

!!! warning "This is strictly for the form-factor as they're both SFU ONTs"

![Swap XS-010X-Q](swap-out-the-nokia-xs-010x-q-for-a-small-form-factor-pluggable-bfw-solutions-was-110/swap_xs010xq_was110.webp){ class="nolightbox" }

<!-- more -->
<!-- nocont -->

## Purchase a WAS-110

The [WAS-110] is available from select [resellers].

 [resellers]: https://pon.wiki/xgs-pon/ont/bfw-solutions/was-110/#value-added-resellers

## Install community firmware

As a prerequisite to masquerading with the WAS-110, the community firmware is necessary; follow the steps
outlined in the community firmware installation guide:

[Install 8311 community firmware on the BFW Solutions WAS-110](install-8311-community-firmware-on-the-bfw-solutions-was-110.md)

## Extract attributes from the XS-010X-Q

![XS-010X-Q login](swap-out-the-nokia-xs-010x-q-for-a-small-form-factor-pluggable-bfw-solutions-was-110/xs010xq_login.webp)

!!! warning "Power off and remove fiber before continuing"

1. Power on the XS-010X-Q with an Ethernet cable plugged between the host PC.

2. Setup a static **IP address** `192.168.100.2` and **Netmask** `255.255.255.0` on the host PC.

3. Within a web browser, navigate to <https://192.168.100.1> and, if asked, input the *admin* password `1234`.

4. From the __ONT install__ page, click on __More info__ button.

![XS-010X-Q info](swap-out-the-nokia-xs-010x-q-for-a-small-form-factor-pluggable-bfw-solutions-was-110/xs010xq_info.webp)

5. Copy all the attributes for entry later in the guide.

## WAS-110 masquerade setup

Additionally, mandatory identifiers are available on the back label of the XS-010X-Q, such as ONT P/N, ICS, and CLEI.

<div id="xs-010x-q-label"></div>

![XS-010X-Q label](swap-out-the-nokia-xs-010x-q-for-a-small-form-factor-pluggable-bfw-solutions-was-110/xs010xq_label.webp){ class="nolightbox" }

### from the web UI <small>recommended</small> { #from-the-web-ui data-toc-label="from the web UI"}

![WAS-110 login](shared-assets/was_110_luci_login.webp)

1. Within a web browser, navigate to
   <https://192.168.11.1/cgi-bin/luci/admin/8311/config>
   and, if asked, input your <em>root</em> password.

    ??? info "As of version 2.4.0 `https://` is supported and enabled by default"
        All `http://` URLs will redirect to `https://` unless the `8311_https_redirect` environment variable is set to
        0 or false.

![WAS-110 8311 configuration](shared-assets/was_110_luci_config.webp)

2. From the __8311 Configuration__ page, on the __PON__ tab, fill in the configuration with the following values:

    !!! reminder "All attributes below are <ins>mandatory</ins> to achieve O5 operation state"
        <ins>Replace</ins> the __PON Serial Number__, __IP Host MAC address__, __Registration ID__, and
        __Software Version A/B__ with the provisioned values.

    | Attribute                  | Value                         | Remarks                                    |
    | -------------------------- | ----------------------------- | ------------------------------------------ |
    | PON Serial Number (ONT ID) | ALCL&hellip;                  | Serial number                              |
    | Equipment ID               | BVMGY10BRAXS010XQ             | CLEI + Mnemonic                            |
    | Hardware Version           | 3FE49331AAAB01                | ONT P/N. + ICS                             |
    | Sync Circuit Pack Version  | :check_mark:                  |                                            |
    | Software Version A         | 3FE49337AOCK10                | Active software version                    |
    | Software Version B         | 3FE49337AOCK80                | Standby software version                   |
    | Firmware Version Match     | ^(3FE4933\d[A-Z]OCK\d{2})$    |                                            |
    | Registration ID            |                               | Input if __ONT ID__ is not null (all 00's) |
    | MIB File                   | /etc/mibs/prx300_1U.ini       | PPTP i.e. default value                    |
    | PON Slot                   | 10                            |                                            |
    | IP Host MAC Address        | FC:B2:D6:18:47:40             | MAC ID                                     |

3. __Save__ changes and reboot from the __System__ menu.

Once rebooted, the SC/APC cable can safely be plugged into the WAS-110 and immediately receive O5 operational status.

For troubleshooting, please read:

[Troubleshoot connectivity issues with the BFW Solutions WAS-110]

### from the shell

<h4>Login over SSH</h4>

```sh
ssh root@192.168.11.1
```

<h4>Configure 8311 U-Boot environment</h4>

!!! reminder "All attributes below are <ins>mandatory</ins> to achieve O5 operation state"
    <ins>Replace</ins> the __8311_gpon_sn__, __8311_iphost_mac__, and __8311_sw_verA/B__ with
    the provisioned values.

``` sh
fwenv_set -8 iphost_mac FC:B2:D6:18:47:40 # (1)!
fwenv_set -8 gpon_sn ALCL... # (2)!
fwenv_set -8 equipment_id BVMGY10BRAXS010XQ # (3)!
fwenv_set -8 hw_ver 3FE49331AAAB01 # (4)!
fwenv_set -8 cp_hw_ver_sync 1
fwenv_set -8 sw_verA 3FE49337AOCK10
fwenv_set -8 sw_verB 3FE49337AOCK80
fwenv_set -8 -b fw_match '^(3FE4933\d[A-Z]OCK\d{2})$'
fwenv_set -8 pon_slot 10
```

1. MAC ID
2. Serial number or S/N
3. CLEI + Mnemonic
4. ONT P/N + ICS

!!! info "Additional details and variables are described at the original repository [^1]"
    `/usr/sbin/fwenv_set` is a helper script that executes `/usr/sbin/fw_setenv` twice consecutively.

    The WAS-110 functions as an A/B system, requiring the U-Boot environment variables to be set twice, once for each
    environment.

    The `-8` option prefixes the U-Boot environment variable with `8311_`.

<h4>Verify and reboot</h4>

Prior to rebooting, verify that the 8311 environment variables are set correctly. If not, proceed to correct them with
the `fwenv_set` command as before.

```sh
fw_printenv | grep ^8311
reboot
```

Once rebooted, the SC/APC cable can safely be plugged into the WAS-110 and immediately receive O5 operational status.

For troubleshooting, please read:

[Troubleshoot connectivity issues with the BFW Solutions WAS-110]

  [WAS-110]: ../xgs-pon/ont/bfw-solutions/was-110.md#value-added-resellers
  [Troubleshoot connectivity issues with the BFW Solutions WAS-110]: troubleshoot-connectivity-issues-with-the-bfw-solutions-was-110.md

[^1]: <https://github.com/djGrrr/8311-was-110-firmware-builder>
