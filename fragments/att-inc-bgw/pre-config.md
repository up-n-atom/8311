## Pre-configuration

Before beginning the ONT configuration, ensure you have addressed the following networking requirements to prevent
authentication lockouts.

### DHCP MAC Spoofing

The ISP’s DHCP server identifies your connection via the Unique MAC address of the original equipment. To ensure the
ISP "trusts" your new hardware immediately, you must __clone the {{ page.meta.ont }} MAC address onto your ^^router^^'s
WAN physical interface.__

!!! info "The "Lease Window" Issue"
    ISP DHCP leases are often tied to a specific hardware ID for a set duration (30 minutes for AT&T). If you swap
    hardware without cloning the MAC, the server will detect an "unauthorized" device and refuse to issue a WAN IP
    until the old lease expires.

### LCT Access Route

To configure the ONT, your router must be able to reach its Local Craft Terminal (LCT) interface. Follow the
[Accessing the ONT] guide to set up the proper network routing between your router and the ONT.

  [Accessing the ONT]: accessing-the-ont.md
