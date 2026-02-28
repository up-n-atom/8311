## Pre-configuration

Before beginning the ONT configuration, ensure you gathered the required data from the {{ page.meta.ont }} and have
addressed the following networking requirements to enable successful communication with the PON.

### Extract required attributes

Install the [XMO client] as described earlier in the guide and extract the following OMCI values to masquerade as the
{{ page.meta.ont }}.

  [XMO client]: #via-xmo-client

#### PON serial number

The PON serial number uniquely identifies your ONT within the network.

``` sh
xmo-remote-client --host=192.168.1.1 get-value --path "Device/Optical/G988/EquipmentManagement/OnuG/SerialNumber"
```

#### Software versions

ONTs utilize an A/B architecture for resilience; consequently, two software versions are identified. These are stored
as hex-encoded strings and must be processed through a hex-to-ASCII converter to be read in a human-readable format.

``` sh
xmo-remote-client --host=192.168.1.1 get-value --path "Device/Optical/G988/EquipmentManagement/SoftwareVersions[@uid=1]/Version"
xmo-remote-client --host=192.168.1.1 get-value --path "Device/Optical/G988/EquipmentManagement/SoftwareVersions[@uid=2]/Version"
```

#### ONU mode (MIB file) { #onu-mode }

The ONU mode will be either **PPTP** (represented by MIB files ending in 'U') or **VEIP** (represented by MIB files ending in 'V').

``` sh
xmo-remote-client --host=192.168.1.1 get-onu-mode
```

### LCT Access Route

To install, upgrade, and configure the ONT, your gateway must be able to reach its Local Craft Terminal (LCT) interface.
__Follow the [Accessing the ONT] guide to set up the proper network routing between your gateway and the ONT mangement plane.__

  [Accessing the ONT]: accessing-the-ont.md
