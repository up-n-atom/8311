---
date: 2024-03-22
categories:
  - XGS-PON
  - Home Hub 4000
  - WAS-110
  - Bell Canada
  - Bell Aliant
  - Bell MTS
  - Sagemcom
  - FAST 5689
description: Masquerade as the BCE Inc. Home Hub 4000 on XGS-PON with the BFW Solutions WAS-110
---

# Masquerade as the BCE Inc. Home Hub 4000 on XGS-PON with the BFW Solutions WAS-110

![Bypass family](masquerade-as-the-bce-inc-home-hub-4000-on-xgs-pon-with-the-bfw-solutions-was-110/bypass_home_hub_4000.webp){ class="nolightbox" }

<!-- more -->
<!-- nocont -->

## Determine if you're an XGS-PON subscriber

!!! info "3Gbps or higher packages"
    If you're subscribed to Gigabit Fibe 3.0 or a similar 3Gbps or higher package, skip past to [Purchase a WAS-110].

There are two (2) methods to determine if you're an XGS-PON subscriber: the simpler [Web UI](#with-web-ui) WAN mode 
switcheroo and the more comprehensive [XMO API client](#with-xmo-client). 

### with the web UI <small>recommended</small> { #with-the-web-ui data-toc-label="with the web UI" }

!!! info "Firmware version __1.7.11__ removed the helpful auto-detected mode output"

![Home Hub 4000 Administrator login prompt](masquerade-as-the-bce-inc-home-hub-4000-on-xgs-pon-with-the-bfw-solutions-was-110/home_hub_4000_login.webp)

1. Within a web browser, navigate to
   <https://home/?c=advancedtools/wan>
   and, if asked, input your Administrator password. (1)
   { .annotate }

    1. The default Administrator password is the S/N located on the back [label] of the Home Hub 4000.

![Home Hub 4000 WAN mode](masquerade-as-the-bce-inc-home-hub-4000-on-xgs-pon-with-the-bfw-solutions-was-110/home_hub_4000_wan_mode.webp)

2. From the __WAN mode__ drop-down, switch from `AUTO` to `XGS-PON` and click __Save__.

If your internet access doesn't drop out, you're subscribed on XGS-PON.

### with a XMO client

The open-source XMO client[^1] has a prerequisite of Python 3.10 or newer.
Python installation varies by Operating System and has been outlined by the tutors at 
[Real Python &mdash; Python 3 Installation & Setup Guide](https://realpython.com/installing-python).

<h4>Install client</h4>

Open a terminal and install the open-source XMO client with:

=== ":fontawesome-brands-windows: Windows"

    ``` sh hl_lines="5"
    py --version
    py -m venv venv
    venv\Scripts\activate
    py -m pip install --upgrade pip 
    pip install https://github.com/up-n-atom/sagemcom-modem-scripts/releases/download/v0.0.4/xmo_remote_client-0.0.4-py3-none-any.whl
    ```

=== ":material-apple: macOS / :material-linux: Linux"

    ``` sh hl_lines="5"
    python3 --version # (1)!
    python3 -m venv .venv
    . .venv/bin/activate
    python3 -m pip install --upgrade pip
    pip3 install https://github.com/up-n-atom/sagemcom-modem-scripts/releases/download/v0.0.4/xmo_remote_client-0.0.4-py3-none-any.whl
    ```

    1. Verify the installed Python version is >= __3.10__

<h4>Exec client</h4>

Finally, to determine if you're an XGS-PON subscriber, execute the following:

``` sh
xmo-remote-client --password=<password> -a MD5 get-wan-mode
```

!!! note
    Replace the `<password>` argument; the default Administrator password is the S/N located on the back [label] of the 
    Home Hub 4000.

## Purchase a WAS-110

The WAS-110 is available from select distributors and at a discounted rate with group buys on the 
[8311 Discord community server](https://discord.com/servers/8311-886329492438671420).

## Install community firmware

As a prerequisite to masquerading with the WAS-110, the community firmware is necessary; follow the steps 
outlined in the community firmware installation guide:

[Install 8311 community firmware on the BFW Solutions WAS-110](install-8311-community-firmware-on-the-bfw-solutions-was-110.md)

## WAS-110 masquerade setup

To successfully masquerade on XGS-PON, the original ONT serial number is mandatory. It, along with other key 
identifiers are available on the back label of the Home Hub 4000, color-coordinated in the following depiction:

![Home Hub 4000 label](masquerade-as-the-bce-inc-home-hub-4000-on-xgs-pon-with-the-bfw-solutions-was-110/home_hub_4000_label.webp){ class="nolightbox" id="home-hub-4000-label" }

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
        <ins>Replace</ins> the :blue_circle: __PON serial number__ and :purple_circle: __MAC address__ with the 
        provisioned values on the back [label] of the Home Hub 4000.

    | Attribute                  | Value                        | Mandatory    | Remarks                         |
    | -------------------------- | ---------------------------- | ------------ |-------------------------------- |
    | PON Serial Number (ONT ID) | SMBS03831122                 | :check_mark: | :blue_circle:                   |
    | Equipment ID               | 5689                         |              |                                 |
    | Hardware Version           | Fast5689Bell                 |              |                                 |
    | Sync Circuit Pack Version  | :check_mark:                 |              |                                 |
    | Software Version A         | SGC8210154                   |              | [Version listing]               |
    | Software Version B         | SGC8210154                   |              | [Version listing]               |
    | MIB File                   | /etc/mibs/prx300_1V_bell.ini | :check_mark: | VEIP and more                   |
    | IP Host MAC Address        | 40:65:A3:FF:A7:B1            |              | :purple_circle: MAC address + 1 |

3. __Save__ changes and reboot from the __System__ menu.

Once rebooted, the SC/APC cable can safely be plugged into the WAS-110 and immediately receive O5 
operational status.

### from the shell

<h4>Login over SSH</h4>

``` sh
ssh root@192.168.11.1
```

<h4>Configure 8311 U-Boot environment</h4>

!!! reminder 
    <ins>Replace</ins> the :blue_circle: __PON serial number__ and :purple_circle: __MAC address__ with the 
    provisioned values on the back [label] of the Home Hub 4000.

!!! note "Highlighted lines are mandatory"

``` sh hl_lines="1 3 9"
fwenv_set mib_file
fwenv_set 8311_iphost_mac 40:65:A3:FF:A7:B1 # (1)!
fwenv_set 8311_gpon_sn SMBS03831122
fwenv_set 8311_equipment_id 5689
fwenv_set 8311_hw_ver Fast5689Bell
fwenv_set 8311_cp_hw_ver_sync 1
fwenv_set 8311_sw_verA SGC8210154 # (2)!
fwenv_set 8311_sw_verB SGC8210154
fwenv_set 8311_mib_file /etc/mibs/prx300_1V_bell.ini 
```

1. :purple_circle: MAC address + 1, e.g. 
   `40:65:A3:FF:A7:B0` becomes `40:65:A3:FF:A7:B1`
2. [Version listing]

!!! info "Additional details and variables are described at the original repository [^2]"
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

## Home Hub 4000 software versions

The software version can be used as a provisioning attribute by the OLT. Therefore, it is important to keep up-to-date
with the latest listing.

| Firmware Version | External Firmware Version |
| ---------------- | ------------------------- |
| 1.7.11           | SGC8210154                |
| 1.7.8.1          | SGC8210140                |
| 1.7.2            | SGC821011A                |

Please help us by contributing new versions via the
[8311 Discord community server](https://discord.com/servers/8311-886329492438671420)
or submitting a
[Pull Request](https://github.com/up-n-atom/8311/pulls) on GitHub.

The following command extracts the external firmware version used by OMCI managed entity 7 and requires the
[XMO client] described earlier in this guide.

``` sh
xmo-remote-client -p <password> -a MD5 get-value --path "Device/DeviceInfo/SoftwareVersion" --path "Device/DeviceInfo/ExternalFirmwareVersion"
```

  [Purchase a WAS-110]: #purchase-a-was-110
  [label]: #home-hub-4000-label
  [Version listing]: #home-hub-4000-software-versions
  [XMO client]: #with-a-xmo-client

[^1]: <https://github.com/up-n-atom/sagemcom-modem-scripts>
[^2]: <https://github.com/djGrrr/8311-was-110-firmware-builder>
