## Router tips

!!! info "VLAN..."
    When __Fix VLANs__ is enabled and the __Internet VLAN__ is set to `0`, the [WAS-110]/[X-ONU-SFPP] strips the
    [Dot1q] VLAN header. This means your router does NOT require a VLAN 35 configuration, functionally similar as the
    {{ page.meta.ont }} in passthrough mode.

    If you are migrating from a [GPON] bypass and want to keep your router's VLAN 35 configuration, you must specify
    the __Internet VLAN__, as detailed in [Set WAS-110/X-ONU-SFPP Internet VLAN](#set-was-110x-onu-sfpp-internet-vlan).

  [GPON]: ../gpon/index.md
  [Dot1q]: https://en.wikipedia.org/wiki/IEEE_802.1Q

=== "Bell Canada"

    * Configure your router WAN interface for PPPoE mode using your B1 username and password.
    * Enable baby jumbo frames by setting the physical WAN interface's MTU to `1508` and the PPPoE virtual Interface's
      MTU to `1500`.

    !!! note "If you have forgotten your B1 password, you can reset it on the [MyBell](https://mybell.bell.ca/) portal."

=== "Bell Aliant/MTS"

    * Configure your router WAN interface for DHCP mode.
    * Clone the {{ page.meta.ont }} :purple_circle: __MAC address__ on the router's DHCP WAN interface.

  [WAS-110]: ../xgs-pon/ont/bfw-solutions/was-110.md
  [X-ONU-SFPP]: ../xgs-pon/ont/potron-technology/x-onu-sfpp.md
