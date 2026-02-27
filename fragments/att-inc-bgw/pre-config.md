## Pre-configuration

Before beginning the ONT configuration, ensure you have addressed the following networking requirements to enable
successful communication with the PON.

### DHCP MAC Spoofing

The ISP’s DHCP server identifies your connection via the Unique MAC address of the original equipment. To ensure the
ISP "trusts" your new hardware immediately, you must __clone the {{ page.meta.ont }} MAC address onto your ^^gateway^^'s
WAN physical interface.__

!!! info "The "Lease Window" Issue"
    ISP DHCP leases are often tied to a specific hardware ID for a set duration (30 minutes for AT&T). If you swap
    hardware without cloning the MAC, the server will detect an "unauthorized" device and refuse to issue a WAN IP
    until the old lease expires.

### LCT Access Route

To install, upgrade, and configure the ONT, your gateway must be able to reach its Local Craft Terminal (LCT) interface.
__Follow the [Accessing the ONT] guide to set up the proper network routing between your gateway and the ONT management plane.__

  [Accessing the ONT]: accessing-the-ont.md

!!! note "HLX-SFPX (HTTP Only)"
    The HLX-SFPX web server uses __unencrypted HTTP__ and does not support HTTPS.

    To access the web management interface, you may need to __disable HTTPS-Only Mode__ (or similar
    &quot;Always use secure connection&quot; settings) in your browser.

    !!! warning "For local management only. Avoid using over public or untrusted networks."
