## Active Cooling

!!! warning "Caution: Hot surface"
    It is advisable to provide sufficient cooling. Although temperatures in excess of 60&deg;C are within specification,
    over time they may decrease the product lifespan.

    The 8311 community has produced many active cooling designs to improve overall temperatures.
    Join the [Discord](https://discord.pon.wiki) for additional tips.

<iframe width=300" height="340" src="https://www.printables.com/embed/1392938" scrolling="no" frameborder="0" referrerpolicy="strict-origin-when-cross-origin"></iframe>

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

Version 2.8.2 and later support a [JSON](https://en.wikipedia.org/wiki/JSON) endpoint at
<https://192.168.11.1/cgi-bin/luci/8311/metrics>.
