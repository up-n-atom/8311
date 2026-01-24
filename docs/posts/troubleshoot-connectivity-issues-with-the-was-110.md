---
date: 2024-05-22
categories:
  - WAS-110
  - BFW Solutions
  - XGS-PON
description: Troubleshoot connectivity issues with the WAS-110
pin: true
---

# Troubleshoot connectivity issues with the WAS-110 or X-ONU-SFPP

![WAS-110 troubleshoot](troubleshoot-connectivity-issues-with-the-bfw-solutions-was-110/was_110_troubleshoot.webp){ class="nolightbox" }

<!-- more -->
<!-- nocont -->

The MaxLinear SDK includes an extensive suite of debugging tools that come pre-bundled with the [WAS-110] firmware(s).
These tools can be run either from the shell console or have been tied into the web UI.

## PON troubleshooting

### Digital Diagnostic Monitor Interface

The [WAS-110] supports the Digital Diagnostic Monitor Interface (DDMI)[^1] to provide pseudo-real-time access to its
operating parameters via a host interface. Although simplistic, this interface is suitable for monitoring power and
temperature behaviours, which are the first tells of troubles.

For more details on accessing this interface, please search your hosts' documentation for
*Digital Diagnostic Monitoring (DDM)* or *Digital Optical Monitoring (DOM)*.

#### Host access

##### :simple-linux: Linux / :simple-ubiquiti: UniFi OS { #linux-ddmi data-toc-label="Linux" }

``` sh
ethtool -m <interface>
```

##### :simple-mikrotik: MikroTik RouterOS { #mikrotik-routeros-ddmi data-toc-label="MikroTik RouterOS" }

``` sh
/interface ethernet monitor sfpX #(1)!
```

1. Replace sfp`X` with the port name/number.

### Optical Power

#### Optical specifications

| &nbsp;       | Min. | Max. | Unit | WAS-110 Error |
| ------------ | ---- | ---- | ---- | ------------- |
| __Tx Power__ | 4    | 9    | dBm  | +/- 2         |
| __Rx Power__ | -29  | -8   | dBm  | +/- 3         |

##### Industry Standard Signal Ranges
| &nbsp; | Great       | Good      | Fair (Warning) | Poor (Action)       |
| ------ | ----------- | --------- | -------------- | ------------------- |
| __Rx__ | −14 to −20  | −8 to −24 | −24 to −27     | Lower than −27      |
| __Tx__ | +2 to +4    | +1 to +7  | 0 to +1        | Below 0 or Above +8 |

|                |   |
| -------------- | - |
| <small>__Great__</small> | <small>Your connection is perfect.</small> |
| <small>__Good__</small>  | <small>Your connection is stable and healthy.</small> |
| <small>__Fair__</small>  | <small>Your internet might be slow or drop occasionally. Check your connectors and cables, dirty or bent?</small> |
| <small>__Poor__</small>  | <small>Your connection is failing. Contact support.</small> |

#### Optical status

To determine if the [WAS-110] optics are operating within specification, execute one of the following procedures:

=== "8311 firmware"

    <h5>from the Web UI</h5>

    ![WAS-110 PON status](troubleshoot-connectivity-issues-with-the-bfw-solutions-was-110/was_110_luci_optical_status.webp){ loading=lazy }

    1. Navigate to <https://192.168.11.1/cgi-bin/luci/admin/8311/pon_status> and, if asked, input your *root* password.
    2. From the __PON Status__ page, select the __Optical Status__ tab.
    3. Evaluate __Transmit power__ and __Receive power__ are within [spec](#optical-specifications).

    <h5>from the Linux shell</h5>

    ``` sh
    pontop -b -g 'Optical Interface Status'
    ```

=== "Azores firmware"

    <h5>from the Web UI</h5>

    ![WAS-110 PON status](troubleshoot-connectivity-issues-with-the-bfw-solutions-was-110/was_110_azores_pon.webp){ loading=lazy }

    1. Navigate to <https://192.168.11.1/html/main.html#status/pon> and, if asked, input your *admin*
       [web credentials]{ data-preview target="_blank" }.
    2. From the __Status__ tab, select the __PON__ page.
    3. Evaluate __Tx Power(dBm)__ and __Rx Power(dBm)__ are within [spec](#optical-specifications).

    <h5>from the Linux shell</h5>

    ``` sh
    i2c_cmd show optical
    ```

    <!--
    root@prx126-sfp-pon:~# i2c_cmd show optical
    Rx Power:	-40.00 dBm
    Tx Power:	-40.00 dBm
    Voltage:	3211 mV
    Bias Current:	0 uA
    Temperature:	40.50 C
    SFP Vendor NAME:	E.C.I. NETWORKS
    SFP Vendor REV:	V1.0
    SFP SN:	AZRS6F595EBC
    SFP VENDOR PN:	ENXGSFPPOMACV2
    -->

=== "HLX-SFPX"

    ![HLX-SFPX PON status](shared-assets/hlx_sfpx_pon_status.webp){ loading=lazy }

    1. Within a web browser, navigate to <http://192.168.33.1/> and, if asked, input the *useradmin*
       [web credentials]{ data-preview target="_blank" }.
    2. From the main navigation __Status__ drop-down, click __PON Interface__.
    3. From the __Optical Information__ section, evaluate that the __RX Power__ and __TX Power__ are within [spec](#optical-specifications).

### Validate OLT authentication
And as with a Linux host, the DDMI[^1] is available from the [WAS-110] shell,
where both __Laser output power__ and __Receiver signal average optical power__ can be evaluated.

``` sh
ethtool -m pon0
```

!!! failure "Optic fault test"

    <h5>Test 1</h5>

    1. Unplug the fiber cable.
    2. Check the [optical status](#optical-status), if the transmit (Tx) and receive (Rx) power (dBm) do not report
       __No signal__ or __-40dBm__ or __-inf__, the optics are miscalibrated or faulty.

    <h5>Test 2</h5>

    1. Plug-in the fiber cable.
    2. Check the [optical status](#optical-status), if the transmit (Tx) and receive (Rx) power (dBm) report
       __No signal__, you're likely subscribed to GPON (1490nm downstream and 1310nm upstream) which isn't a compatible
       wavelength for the [WAS-110].

### Fake O5

#### Activation states

- O1 Initial state
- O2 Stand-by state
- O3 Serial number state
- O4 Ranging state
- O5 Operation state
- O6 POPUP state
- O7 Emergancy stop state

A common term tossed around is <q>fake</q> O5, which is a misnomer that occurs when PLOAM message activation succeeds,
including Serial Number and/or Registration ID authentication. However, the failure is further along in the
registration chain, such as OMCI. It pertains to invalid managed entity attributes with common associations to device
integrity, such as hardware and/or software versioning.

#### PLOAM status

To view the current PLOAM status, execute one of the following procedures:

=== "8311 firmware"

    <h5>from the Web UI</h5>

    ![WAS-110 PON status](troubleshoot-connectivity-issues-with-the-bfw-solutions-was-110/was_110_luci_pon_status.webp){ loading=lazy }

    1. Navigate to <https://192.168.11.1/cgi-bin/luci/admin/8311/pon_status> and, if asked, input your *root* password.
    2. From the __PON Status__ page, select the __Status__ tab to ascertain the __PON PLOAM Status__.

    <h5>from the Linux shell</h5>

    ``` sh
    pontop -b -g s
    ```

=== "Azores firmware"

    <h5>from the Web UI</h5>

    ![WAS-110 PON status](troubleshoot-connectivity-issues-with-the-bfw-solutions-was-110/was_110_azores_pon.webp){ loading=lazy }

    1. Navigate to <https://192.168.11.1/html/main.html#status/pon> and, if asked, input your *admin*
       [web credentials].
    2. From the __Status__ tab, select the __PON__ page to ascertain the __ONU State__.

    <h5>from the Linux shell</h5>

    ``` sh
    pontop -b -g s
    ```

=== "HLX-SFPX"

    ![HLX-SFPX PON status](shared-assets/hlx_sfpx_pon_status.webp){ loading=lazy }

    1. Within a web browser, navigate to <https://192.168.33.1/> and, if asked, input the *useradmin*
       [web credentials]{ data-preview target="_blank" }.
    2. From the main navigation __Status__ drop-down, click __PON Interface__.
    3. Evaluate the __PLOAM State__ in the __Link Information__ section.

#### OMCI clarification

To help identify fake O5, execute the following command procedures and if the response is empty, the operational state is
*"fake"* as the OLT did not respond with the dot1q[^6] configuration.

=== "8311 firmware"

    !!! note "As of version 2.7.2 the extended VLAN table(s) can now be dumped in a human readable format"

    <h5>from the Web UI</h5>

    1. Navigate to <https://192.168.11.1/cgi-bin/luci/admin/8311/vlans> and, if asked, input your root password.
    2. From the __VLAN Tables__ page, if the __textarea__ is blank, the ONT configuration has not satisfied the OLT.

    <h5>from the Linux shell</h5>

    ``` sh
    8311-extvlan-decode.sh -t
    ```
=== "Azores firmware"

    <h5>from the Linux shell</h5>

``` sh
omci_pipe.sh md | grep -E '^\|\s+(84|171)\s\|'
```

Additionally, it is possible to identify the connected OLT by executing the following command:

``` sh
omci_pipe.sh meg 131 0
```

Typically, OLT operators enforce versioning compliance when software management is not handled over CWMP[^2].

## LAN troubleshooting

### Link Speed

The [WAS-110] will attempt to auto-negotiate with the host controller and, more often than not, fallback to 1 Gbps.
To prevent this behaviour, forcefully set the speed of the host interface to 10 Gbps.

Furthermore, to force the link speed on the [WAS-110] itself, execute the following `ethtool`[^3] procedures.

=== "8311 firmware"

    <h5>from the Web UI <small>permanent</small></h5>

    ![WAS-110 device tab](troubleshoot-connectivity-issues-with-the-bfw-solutions-was-110/was_110_luci_device.webp){ loading=lazy }

    1. Navigate to <https://192.168.11.1/cgi-bin/luci/admin/8311/config> and, if asked, input your *root* password.
    2. From the __8311 Configuration__ page, select the __Device__ tab.
    3. From the __Device__ tab, set the __Ethtool Speed Settings__ input to one of the following:

           | Parameters  |
           | ----------- |
           | speed 1000  |
           | speed 2500  |
           | speed 10000 |

    <h5>from the Linux shell <small>temporary</small></h5>

    !!! warning "The following command sets the link speed <ins>temporarily</ins> until the next power cycle"

    ``` sh
    ethtool -s eth0_0 speed <speed> #(1)!
    ```

    1. <ins>Replace</ins> the &lt;speed&gt; parameter to either 1000, 2500, or 10000

=== "Azores firmware"

    <h5>from the Web UI <small>permanent</small></h5>

    ![WAS-110 Negotiation Speed](troubleshoot-connectivity-issues-with-the-bfw-solutions-was-110/was_110_azores_speed.webp){ loading=lazy }

    1. Navigate to <https://192.168.11.1/html/main.html#service/setlanfixspeed>, and, if asked, input your *admin*
       [web credentials].
    2. From the __Negotiation Speed__ page, select __OnDemand__ and __10G__ link speed, and click __Save__.

    <h5>from the Linux shell <small>temporary</small></h5>

    !!! warning "The following command sets the link speed <ins>temporarily</ins> until the next power cycle"

    ``` sh
    ethtool -s eth0_0 speed <speed> #(1)!
    ```

    1. <ins>Replace</ins> the &lt;speed&gt; parameter to either 1000, 2500, or 10000

### Tx fault

The SFP tx fault pin[^4] (2) is multiplexed with UART tx. If the serial UART is enabled, tx fault may be asserted by the
host hardware and cause the link state to flap continuously.

#### Serial console

!!! note "By default, serial UART is enabled during boot-up until Linux init, where it is disabled"

=== "8311 firmware"

    <h5>from the Web UI</h5>

    ![WAS-110 device tab](troubleshoot-connectivity-issues-with-the-bfw-solutions-was-110/was_110_luci_device.webp){ loading=lazy }

    1. Navigate to <https://192.168.11.1/cgi-bin/luci/admin/8311/config> and, if asked, input your *root* password.
    2. From the __8311 Configuration__ page, select the __Device__ tab.
    3. From the __Device__ tab, uncheck the __Serial console__ checkbox.

    <h5>from the Linux shell</h5>

    To disable the serial console from the Linux shell, execute the following commands:

    ``` sh
    fwenv_set -8 console_en
    ```

    <h5>from the U-Boot shell</h5>

    To disable the serial console from the U-Boot shell, execute the following commands:

    ``` sh
    env delete 8311_console_en
    env save
    env save
    ```

=== "Azores firmware"

    !!! info "Serial console is disabled by default, except in version 1.0.11"

    To disable the serial console from the Linux shell, execute the following commands:

    ```
    uci -c /ptconf set usrconfig_conf.InternetGatewayDevice__X_PT_CONSOLE_CFG__=interface
    uci -c /ptconf set usrconfig_conf.InternetGatewayDevice__X_PT_CONSOLE_CFG__.Enable=0
    uci -c /ptconf commit usrconfig_conf
    ```

#### Boot console & early printk { #boot-console data-toc-label="Boot console" }

UART tx can be further controlled by two (2) U-Boot environment variables: `uart_select` and `uart_select_preboot`.

!!! warning "<ins>DO NOT</ins> execute the following commands unless you understand the repercussions"

<h5>from the Linux shell</h5>

``` sh
fwenv_set uart_select off
```

<h5>from the U-Boot shell</h5>

``` sh
setenv uart_select off
env save
env save
```

???+ info "To recover, a host device with serial breakout on SFP pins 2 (rx) and 7 (tx) will be required."

    1. Spam ++escape++ in the serial terminal while plugging in the WAS-110

    2. Press ++enter++

    3. Type `mw.b 0xB6180121 0xd8` followed by ++enter++

    4. Delete the `uart_select_preboot` environment variable

        ``` sh
        env set uart_select_preboot
        env save
        env save
        ```

#### Host Solutions

##### :simple-linux: Linux (SFP subsystem)

SFP+ network drivers built on the Linux [SFP subsystem] use SFF-8472[^1] DDMI to manage modules. This causes
issues for non-compliant [GPON] and [XGS-PON] sticks. To work around this, maintainers add hardcoded [quirks]. However,
each new hardware or vendor variant requires a new kernel build. As of kernel 6.17, a quirk for the Yunvo
SFP+ONU-XGSPON ([X-ONU-SFPP]) module has been included to address this.

 [SFP subsystem]: https://www.kernel.org/doc/html/latest/networking/sfp-phylink.html
 [GPON]: ../gpon/index.md
 [XGS-PON]: ../xgs-pon/index.md
 [quirks]: https://git.kernel.org/pub/scm/linux/kernel/git/next/linux-next.git/tree/drivers/net/phy/sfp.c?h=next-20251219#n489

If you see the following output in your kernel log, you are either running an older kernel version, or your
[WAS-110] or [X-ONU-SFPP] module's vendor information does not match an existing quirk.

``` sh
sfp sfp1: module transmit fault indicated
sfp sfp1: module persistently indicates fault, disabling
```

To resolve this issue, you can take one of two approaches:

1. Add a new quirk for your module and recompile your kernel.
2. Modify the vendor information on the module itself to match an existing quirk.

!!! danger "The steps below will make modifications to your module's EEPROM. Make sure you create backups and proceed with caution."

To achieve the latter, SSH into the module and read the current EEPROM value as base64, then paste it into the form below.

``` sh
base64 /sys/class/pon_mbox/pon_mbox0/device/eeprom50
```

<textarea id="eeprom-base64" rows="5" style="width: 100%;"></textarea>
<p>
  <label class="md-typeset">
    <input type="radio" name="device-type" value="WAS-110" checked>
    <span>WAS-110</span>
  </label>
  <label class="md-typeset" style="margin-left: 20px;">
    <input type="radio" name="device-type" value="X-ONU-SFPP">
    <span>X-ONU-SFPP</span>
  </label>
</p>
<a onclick="generate_eeprom_vendor()" class="md-button">Generate</a>
<div class="highlight" style="display: none;">
  <pre><code id="eeprom-output"></code></pre>
</div>

### Rx loss

The SFP rx loss pin[^5] (8) is asserted when the SC/APC fiber cable isn't plugged in and/or inactive. Depending on the
host controller and implementation, the interface may enter a power saving state, making the [WAS-110] inaccessible.

=== "8311 firmware"

    !!! info "Rx loss is deasserted by default as of version 2.3.0"

    <h5>from the Web UI</h5>

    ![WAS-110 device tab](troubleshoot-connectivity-issues-with-the-bfw-solutions-was-110/was_110_luci_device.webp){ loading=lazy }

    1. Navigate to <https://192.168.11.1/cgi-bin/luci/admin/8311/config> and, if asked, input your *root* password.
    2. From the __8311 Configuration__ page, select the __Device__ tab.
    3. From the __Device__ tab, uncheck the __RX Loss of Signal__ checkbox.

    <h5>from the Linux shell</h5>

    To disable rx loss from the Linux shell, execute the following commands:

    ```
    fwenv_set -8 rx_los
    ```

    <h5>from the U-Boot shell</h5>

    To disable rx loss from the U-Boot shell, execute the following commands:

    ``` sh
    env delete 8311_rx_los
    env save
    env save
    ```

=== "Azores firmware"

    Unfortunately, rx loss can't be disabled.

#### Host solutions

##### :simple-mikrotik: MikroTik RouterOS { #mikrotik-routeros-rxlos data-toc-label="MikroTik RouterOS" }

!!! info "Requires RouterOS 7.15+"

``` sh
/interface ethernet set sfpX sfp-ignore-rx-los=yes #(1)!
```

1. Replace spf`X` with the port name/number.

  [WAS-110]: ../xgs-pon/ont/bfw-solutions/was-110.md
  [X-ONU-SFPP]: ../xgs-pon/ont/potron-technology/x-onu-sfpp.md
  [web credentials]: ../xgs-pon/ont/bfw-solutions/was-110.md#web-credentials
  [shell credentials]: ../xgs-pon/ont/bfw-solutions/was-110.md#shell-credentials


[^1]: [SFF-8472](https://members.snia.org/document/dl/25916)
[^2]: <https://en.wikipedia.org/wiki/TR-069>
[^3]: <https://www.linux.org/docs/man8/ethtool.html>
[^4]: <https://en.wikipedia.org/wiki/Small_Form-factor_Pluggable#Signals>
[^5]: [SFF-8419](https://members.snia.org/document/dl/25880)
[^6]: <https://en.wikipedia.org/wiki/IEEE_802.1Q>
