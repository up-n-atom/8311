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
description: Bridge the BCE Inc. Giga Hub
---

# Bridge the BCE Inc. Giga Hub

![Image title](bridge-the-bce-inc-giga-hub/bridge_giga_hub.webp){ class="nolightbox" }

<!-- more -->
<!-- nocont -->

!!! warning "Bell MTS and Aliant users..."
    Enabling bridge mode will produce an error code[^1]. Follow the [disable bridge mode] steps below to revert back to
    router mode.

      [disable bridge mode]: #disable-bridge-mode

The Giga Hub's bridge mode operates as a pseudo-bridge or rather in IP/PPPoE passthrough mode. It can be enabled or
disabled either remotely by a support technician, or by pressing and holding a secret button combination outlined in this guide.

## Enable bridge mode

Hold the __Reset__ and __OK__ buttons simultaneously for 7 seconds.

### What's happening behind the scenes

When enabling bridge mode, the Giga Hub performs the following XMO actions:

| Action                               | XMO Path                                                      | Value    |
| ------------------------------------ | ------------------------------------------------------------- | -------- |
| Disabling WiFi AP[@Alias=PRIV0]      | `Device/WiFi/AccessPoints/AccessPoint[Alias='PRIV0']/Enable`  | False    |
| Disabling WiFi AP[@Alias=GUEST1]     | `Device/WiFi/AccessPoints/AccessPoint[Alias='GUEST1']/Enable` | False    |
| Disabling WiFi SSID[@Alias=WL_PRIV]  | `Device/WiFi/SSIDs/SSID[Alias='WL_PRIV']/Enable`              | False    |
| Disabling WiFi SSID[@Alias=WL_GUEST] | `Device/WiFi/SSIDs/SSID[Alias='WL_GUEST']/Enable`             | False    |
| Disabling USB                        | `Device/USB/Enable`                                           | False    |
| Disabling BR_LAN bridge              | `Device/IP/Interfaces/Interface[Alias='IP_BR_LAN']/Enable`    | False    |
| Disabling BR_GUEST bridge            | `Device/IP/Interfaces/Interface[Alias='IP_BR_GUEST']/Enable`  | False    |
| Disabling DHCPv4 server              | `Device/DHCPv4/Server/Enable`                                 | False    |
| Disabling Password recovery          | `Device/Services/Notification/CredentialsRequestEnable`       | False    |
| Reset default PPPoE username         | `Device/PPP/Interfaces/Interface/Username`                    | sc5689x  |
| Reset default PPPoE password         | `Device/PPP/Interfaces/Interface/Password`                    | 7yTa3wXU |

!!! danger
    <ins>DO NOT</ins> under any circumstances assign the paths manually using a XMO client; they're guaranteed to
    soft-brick the Giga Hub.

## Disable bridge mode

Hold the __Reset__ and either the __Up__ or __Down__ arrow buttons simultaneously for 7 seconds.

[^1]: <https://support.bell.ca/internet/connection-help/troubleshooting_error_codes_with_my_home_hub_modem>
