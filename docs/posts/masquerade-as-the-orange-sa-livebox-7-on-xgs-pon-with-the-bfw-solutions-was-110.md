---
draft: true
date: 2025-06-21
categories:
  - XGS-PON
  - Livebox 7
  - WAS-110
  - Orange S.A.
  - Sagemcom
  - FAST 5694
description: Masquerade as the Orange S.A. Livebox 7 on XGS-PON with the BFW Solutions WAS-110
slug: masquerade-as-the-orange-sa-livebox-7-on-xgs-pon-with-the-bfw-solutions-was-110
---

# Masquerade as the Orange S.A. Livebox 7 on XGS-PON with the BFW Solutions WAS-110

<!-- more -->
<!-- nocont -->

## Determine if you're an XGS-PON subscriber

!!! info "5 Gbps or higher packages"
    If you're subscribed to Livebox Max Fibre or a similar 5 Gbps or higher package, skip past to [Purchase a WAS-110].

### with the web UI

1. Within a web browser, navigate to
   <https://livebox/>
   and, if asked, input your Administrator password. (1)
   { .annotate }

    1. The default Administrator password is the first 12 digits of the WiFi key located on the bottom [label] of the
       Livebox 7.

2. ...

## Purchase a WAS-110

The [WAS-110] is available from select distributors and at a discounted rate with group buys on the 
[8311 Discord community server](https://discord.com/servers/8311-886329492438671420).

## Install community firmware

As a prerequisite to masquerading with the WAS-110, the community firmware is necessary; follow the steps 
outlined in the community firmware installation guide:

[Install 8311 community firmware on the BFW Solutions WAS-110](install-8311-community-firmware-on-the-bfw-solutions-was-110.md)

## WAS-110 masquerade setup

To successfully masquerade on XGS-PON, the original ONT serial number is mandatory. It, along with other key 
identifiers are available from the web UI or the bottom label of the Livebox 7, color-coordinated in the following
depiction:

### from the web UI <small>recommended</small> { #from-the-web-ui data-toc-label="from the web UI"}

![WAS-110 login](masquerade-as-the-orange-sa-livebox-7-on-xgs-pon-with-the-bfw-solutions-was-110/was_110_luci_login.webp)

1. Within a web browser, navigate to 
   <https://192.168.11.1/cgi-bin/luci/admin/8311/config> 
   and, if asked, input your <em>root</em> password.

    ??? info "As of version 2.4.0 `https://` is supported and enabled by default"
        All `http://` URLs will redirect to `https://` unless the `8311_https_redirect` environment variable is set to
        0 or false.

![WAS-110 8311 configuration](masquerade-as-the-orange-sa-livebox-7-on-xgs-pon-with-the-bfw-solutions-was-110/was_110_luci_config.webp)

2. From the __8311 Configuration__ page, on the __PON__ tab, fill in the configuration with the following values:

    !!! reminder 
        <ins>Replace</ins> the :blue_circle: __PON serial number__ with the provisioned values on the bottom [label]
        of the Livebox 7.

    | Attribute                  | Value                        | Mandatory    | Remarks                         |
    | -------------------------- | ---------------------------- | ------------ |-------------------------------- |
    | PON Serial Number (ONT ID) | SMBS03831122                 | :check_mark: | :blue_circle:                   |
    | Equipment ID               | SagemcomFast5694OFR          |              |                                 |
    | Hardware Version           | SMBSXLB7400                  | :check_mark: |                                 |
    | Sync Circuit Pack Version  | :check_mark:                 |              |                                 |
    | Software Version A         | SAHEOFR010117                |              | [Version listing]               |
    | Software Version B         | SAHEOFR919117                |              | [Version listing]               |
    | MIB File                   | /etc/mibs/prx300_1U.ini      | :check_mark: | PPTP i.e. default value         |

3. __Save__ changes and reboot from the __System__ menu.

Once rebooted, the SC/APC cable can safely be plugged into the WAS-110 and immediately receive O5 
operational status.

### from the shell

<h4>Login over SSH</h4>

``` sh
ssh root@192.168.11.1
```

<h4>Configure 8311 U-Boot environment</h4>

!!! reminder "Highlighted lines are <ins>mandatory</ins>"
    <ins>Replace</ins> the :blue_circle: __PON serial number__ with the provisioned values on the bottom [label] of
    the Livebox 7.

``` sh hl_lines="1 3"
fwenv_set 8311_gpon_sn SMBS03831122
fwenv_set 8311_equipment_id SagemcomFast5694OFR
fwenv_set 8311_hw_ver SMBSXLB7400
fwenv_set 8311_cp_hw_ver_sync 1
fwenv_set 8311_sw_verA SAHEOFR010117 # (1)!
fwenv_set 8311_sw_verB SAHEOFR010117
```

1. [Version listing]

!!! info "Additional details and variables are described at the original repository [^1]"
    `/usr/sbin/fwenv_set` is a helper script that executes `/usr/sbin/fw_setenv` twice consecutively.

    The WAS-110 functions as an A/B system, requiring the U-Boot environment variables to be set twice, once for each 
    environment.

<h4>Verify and reboot</h4>

Prior to rebooting, verify that the 8311 environment variables are set correctly. If not, proceed to correct them with
the `fwenv_set` command as before.

``` sh
fw_printenv | grep ^8311
reboot
```

Once rebooted, the SC/APC cable can safely be plugged into the WAS-110 and immediately receive O5 
operational status.

## Livebox 7 software versions

The software version <ins>can</ins> be utilized as a provisioning attribute by the OLT, but this is not the case for 
the Livebox 7, which uses CWMP[^3]. However, it is recommended to keep somewhat up-to-date with the following listing.

| Software Version |
| ---------------- |
| SAHEOFR010117    |
| SAHEOFR010112    |

Please help us by contributing new versions via the
[8311 Discord community server](https://discord.com/servers/8311-886329492438671420)
or submitting a
[Pull Request](https://github.com/up-n-atom/8311/pulls) on GitHub.

  [Purchase a WAS-110]: #purchase-a-was-110
  [WAS-110]: /xgs-pon/ont/bfw-solutions/was-110/#value-added-resellers
  [label]: #livebox-7-label
  [Version listing]: #livebox-7-software-versions

[^1]: <https://github.com/djGrrr/8311-was-110-firmware-builder>
[^2]: <https://en.wikipedia.org/wiki/TR-069>
