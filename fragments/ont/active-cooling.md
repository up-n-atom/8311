## Active Cooling

!!! warning "Caution: Hot surface"
    It is advisable to provide sufficient cooling. Although temperatures in excess of 60&deg;C are within specification,
    over time they may decrease the product lifespan.

    The 8311 community has produced many active cooling designs to improve overall temperatures.
    Join the [Discord](https://discord.pon.wiki) for additional tips.

<iframe width="300" height="340" src="https://www.printables.com/embed/1392938" scrolling="no" frameborder="0" referrerpolicy="strict-origin-when-cross-origin"></iframe>

<iframe width="300" height="340" src="https://www.printables.com/embed/1387322" scrolling="no" frameborder="0" referrerpolicy="strict-origin-when-cross-origin"></iframe>

### Temperature monitoring

#### Digital Diagnostic Monitor Interface

For more details on accessing this interface, please search your hosts' documentation for
Digital Diagnostic Monitoring (DDM) or Digital Optical Monitoring (DOM).

##### :simple-linux: Linux host { #linux-host-ddmi data-toc-label="Linux" }

``` sh
ethtool -m <interface> #(1)!
```

1. Replace `<interface>` with the interface name.

##### :simple-freebsd: FreeBSD host { #freebsd-host-ddmi data-toc-label="FreeBSD" }

``` sh
ifconfig -vvv <interface> #(1)!
```

1. Replace `<interface>` with the interface name.

##### :simple-mikrotik: RouterOS host { #routeros-host-ddmi data-toc-label="RouterOS" }


``` sh
/interface ethernet monitor <sfpX> #(1)!
```

1. Replace sfp`X` with the port name/number.

#### 8311 Community Firmware API

##### JSON Endpoint
Version 2.8.2 and later support a [JSON](https://en.wikipedia.org/wiki/JSON) endpoint at
<https://192.168.11.1/cgi-bin/luci/8311/metrics>.

##### Home Assistant Entities based on JSON Endpoint
``` YAML
rest:
    scan_interval: 600
    resource: https://192.168.11.1/cgi-bin/luci/8311/metrics
    sensor:
      - name: "PON CPU 1 Temp"
        value_template: "{{ value_json.cpu1_tempC | round(2) }}"
        unit_of_measurement: "°C"
        device_class: temperature
        state_class: measurement
      - name: "PON CPU 2 Temp"
        value_template: "{{ value_json.cpu2_tempC | round(2) }}"
        unit_of_measurement: "°C"
        device_class: temperature
        state_class: measurement
      - name: "PON Optics Temp"
        value_template: "{{ value_json.optic_tempC | round(2) }}"
        unit_of_measurement: "°C"
        state_class: measurement
        device_class: temperature
      - name: "PON Voltage"
        value_template: "{{ value_json.module_voltage | round(2) }}"
        device_class: voltage
        state_class: measurement
        unit_of_measurement: "V"
      - name: "PON State"
        value_template: "{{ value_json.ploam_state }}"
      - name: "PON Rx Power"
        value_template: "{{ value_json.rx_power_dBm }}"
        device_class: signal_strength
        state_class: measurement
        unit_of_measurement: "dBm"
      - name: "PON Tx Power"
        value_template: "{{ value_json.tx_power_dBm }}"
        device_class: signal_strength
        state_class: measurement
        unit_of_measurement: "dBm"
      - name: "PON Tx Bias"
        value_template: "{{ value_json.tx_bias_mA }}"
        device_class: current
        state_class: measurement
        unit_of_measurement: "mA"
```
