---
date: 2024-04-01
categories:
  - Bridge Mode
  - Giga Hub
  - Bell Canada
  - Bell Aliant
  - Bell MTS
  - Sagemcom
  - FAST 5689E
---

# Bridge the BCE Inc. Giga Hub

![Image title](bridge-the-bce-inc-giga-hub/bridge_giga_hub.webp)

<!-- more -->
<!-- nocont -->

The Giga Hub's bridge mode operates as a pseudo-bridge or rather in IP/PPPoE passthrough mode. It can be enabled or
disabled either remotely by a support technician, or by pressing and holding a secret button combination outlined in this guide.

## Enable bridge mode

Hold the __Reset__ and __OK__ buttons simultaneously for 7 seconds.

### What's happening behind the scenes

When enabling bridge mode, the Giga Hub performs the following XMO actions:

| Action                               | XMO Path                                                      | Value     |
| ------------------------------------ | ------------------------------------------------------------- | ---------- |
| Disabling WiFi AP[@Alias=PRIV0]      | `Device/WiFi/AccessPoints/AccessPoint[Alias='PRIV0']/Enable`  | `False`    |
| Disabling WiFi AP[@Alias=GUEST1]     | `Device/WiFi/AccessPoints/AccessPoint[Alias='GUEST1']/Enable` | `False`    |
| Disabling WiFi SSID[@Alias=WL_PRIV]  | `Device/WiFi/SSIDs/SSID[Alias='WL_PRIV']/Enable`              | `False`    |
| Disabling WiFi SSID[@Alias=WL_GUEST] | `Device/WiFi/SSIDs/SSID[Alias='WL_GUEST']/Enable`             | `False`    |
| Disabling USB                        | `Device/USB/Enable`                                           | `False`    |
| Disabling BR_LAN bridge              | `Device/IP/Interfaces/Interface[Alias='IP_BR_LAN']/Enable`    | `False`    |
| Disabling BR_GUEST bridge            | `Device/IP/Interfaces/Interface[Alias='IP_BR_GUEST']/Enable`  | `False`    |
| Disabling DHCPv4 server              | `Device/DHCPv4/Server/Enable`                                 | `False`    |
| Disabling Password recovery          | `Device/Services/Notification/CredentialsRequestEnable`       | `False`    |
| Reset default PPPoE username         | `Device/PPP/Interfaces/Interface/Username`                    | `sc5689x`  |
| Reset default PPPoE password         | `Device/PPP/Interfaces/Interface/Password`                    | `7yTa3wXU` |

These actions can be mimicked, permissions pending, with the open source XMO client that was introduced in
[Masquerade as the BCE Inc. Giga Hub on XGS-PON with the BFW Solutions WAS-110](masquerade-as-the-bce-inc-giga-hub-on-xgs-pon-with-the-bfw-solutions-was-110.md#with-a-xmo-client)

!!! danger
    <ins>DO NOT</ins> under any circumstances execute any of the following commands; they're guaranteed to soft-brick the
    Giga Hub.

```
xmo-remote-client -p <password> set-value --path "Device/WiFi/AccessPoints/AccessPoint[Alias='PRIV0']/Enable" --value False
xmo-remote-client -p <password> set-value --path "Device/WiFi/AccessPoints/AccessPoint[Alias='GUEST1']/Enable" --value False
xmo-remote-client -p <password> set-value --path "Device/WiFi/SSIDs/SSID[Alias='WL_PRIV']/Enable" --value False
xmo-remote-client -p <password> set-value --path "Device/WiFi/SSIDs/SSID[Alias='WL_GUEST']/Enable" --value False
xmo-remote-client -p <password> set-value --path "Device/USB/Enable" --value False
xmo-remote-client -p <password> set-value --path "Device/IP/Interfaces/Interface[Alias='IP_BR_LAN']/Enable" --value False
xmo-remote-client -p <password> set-value --path "Device/IP/Interfaces/Interface[Alias='IP_BR_GUEST']/Enable" --value False
xmo-remote-client -p <password> set-value --path "Device/DHCPv4/Server/Enable" --value False
xmo-remote-client -p <password> set-value --path "Device/Services/Notification/CredentialsRequestEnable" --value False
xmo-remote-client -p <password> set-value --path "Device/PPP/Interfaces/Interface/Username" --value "sc5689x"
xmo-remote-client -p <password> set-value --path "Device/PPP/Interfaces/Interface/Password" --value "7yTa3wXU"
```

## Disable bridge mode

Hold the __Reset__ and either the __Up__ or __Down__ arrow buttons simultaneously for 7 seconds.
