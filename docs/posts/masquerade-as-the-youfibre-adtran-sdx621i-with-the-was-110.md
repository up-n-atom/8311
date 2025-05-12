---
date: 2025-05-12
categories:
  - XGS-PON
  - YouFibre
  - Netomnia
  - WAS-110
  - 8311 Firmware
  - OPNsense
  - Better Internet Store
description: Configure the WAS-110 on YouFibre / Netomnia XGS-PON with a preloaded 8311 firmware
slug: connect-to-youfibre-xgs-pon-with-the-was-110
---

# Connect to YouFibre / Netomnia XGS-PON with the WAS-110

<!--![Connect to YouFibre](shared-assets/youfibre_was_110.webp){ class="nolightbox" }-->

<!-- more -->
<!-- nocont -->

## What you need

- A [WAS-110] module, preferably pre-flashed with [8311 firmware](https://github.com/djGrrr/8311-was-110-firmware-builder)
- SC/APC to LC/APC cable or coupler (check which side your socket terminates with). My YouFibre install came **pre-terminated with SC/APC**, which fits directly into the WAS-110. No extra patch cables or adapters were needed.
- Your provisioned **PON Serial Number**
- A router or firewall (e.g. OPNsense) with SFP+ WAN (or an isolated VLAN for WAN)
- Optional: ability to clone MAC address (for static IP assignment from YouFibre)

!!! question "Do I need to flash the firmware?"
    This guide assumes your module comes preloaded with 8311 firmware. Flashing instructions are available separately.

---

## Configuration overview

Once the WAS-110 is connected to your fiber socket and inserted into an SFP+ port, follow these steps:

### 1. Access the 8311 web UI

- Assign your PC an IP like `192.168.11.3/24`
- Connect directly or via switch to the ONT
- Navigate to: `https://192.168.11.1/cgi-bin/luci/admin/8311/config`

---

## 8311 Configuration

### Configuration tab

| Attribute                  | Value                        | Mandatory  | Notes                          |
| --------------------------|------------------------------|------------|--------------------------------|
| PON Serial Number (ONT ID)| *Your original ONT serial*   | ✅         | Bottom of ONT           |
| Equipment ID              | `ADTN`               | ✅         | Matches ZTE ONTs               |
| Hardware Version          | `1.2.1b`                     | optional   | Can be left as-is              |
| Sync Circuit Pack Version | `1`                          | optional   | Sometimes required by OLT      |
| Software Version A        | `3.7.4-2306.5`               | ✅         | Confirmed working              |
| Software Version B        | `3.7.4-2306.5`               | ✅         | Matches A                      |
| MIB File                  | `/etc/mibs/prx300_1U.ini`    | ✅         | Required 
for VEIP and OLT match|
| MAC                  | Cloned from original ONT    | ✅         | Required

!!! bug "Empty VLAN table or no WAN IP?"
    Disable `Fix VLANs` under the *ISP Fixes* tab and reboot. Without this, DHCP may silently fail.

---

## Real-world usage notes

### 💬 My user report

> I managed to get PLOAM to O5.1 (Associated), but my OPNsense WAN didn’t get a DHCP IP until I:
>
> - Disabled `Fix VLANs`
> - Rebooted OPNsense
>

> The 8311 UI was unaccessible after moving it into the WAN VLAN, tried adding a static route but no use.

> I successfully replaced the ISP ADTRAN SDX621i ONT.

---

## Performance

Running at **1 Gbps symmetric**, reports:

> I saw about a 50 Mbps increase in speed, though the main win was space-saving in the network cabinet by eliminating the external ONT.

---

## Resources

- [8311 Discord Community](https://discord.gg/X7ES6Vu6gJ)
- [WAS-110 Product Page](../xgs-pon/ont/bfw-solutions/was-110.md)
- [Troubleshooting Fake O5](../guides/troubleshoot-connectivity-issues-with-the-was-110.md#fake-o5)

---

## Thanks

Special thanks to [Better Internet Store](https://www.betterinternet.ltd) for support and supplying the pre-flashed module.

