# X-ONU-SFPP (SFP+ XGSPON ONU Stick)

![X-ONU-SFPP](x-onu-sfpp/x-onu-sfpp.webp)

## Specifications

|             |                                         |                     |
| ----------: | --------------------------------------- | ------------------- |
| __SoC__     | PRX126 @ 400 MHz - MIPS interAptiv 34Kc | [Architecture] [^4] |
| __NAND__    | 128 MB *(1 Gbit)*                       | [WN25N01GV]         |
| __RAM__     | 1 GB                                    |                     |
| __BOSA__    | SC/UPC - Tx: 1270 nm / Rx: 1577 nm      | [M02181]            |
| __EEPROM__  | :check_mark:                            | [M02181]            |
| __IP__      | 192.168.1.1                             |                     |
| __HTTP(S)__ | :x:                                     |                     |
| __SSH__     | :check_mark:                            | [Shell credentials] |

 [Architecture]: #architecture
 [WN25N01GV]: https://www.winbond.com/hq/product/code-storage-flash-memory/qspinand-flash/?__locale=en&partNo=W25N01GV 
 [M02181]: https://www.macom.com/products/product-detail/MALD-02181
 [Shell credentials]: #shell-credentials

## Architecture

### MaxLinear PRX126 [^2]

``` mermaid
%%{ init: { 'flowchart': { 'htmlLabels': false, 'curve': 'stepBefore' } } }%%
flowchart LR
    Z[" "] <--Fiber -->
    A(BOSA)
    B("DRIVER/
    LA
    (PMD)")
    A --> B
    B --> A
    subgraph SOC
        C("SERDES
        /CDR")
        subgraph MAC
            D("10G(E)PON
            PCS&MAC/
            TC") ~~~
            E("10G-
            Ethernet
            PCS&MAC")
        end
        C <--> MAC
        F("Network
        Processsor
        /Package
        Switch")
        MAC <--> F
        G("10G-
        Ethernet
        PCS&
        MAC")
        F <--> G <-->
        H("SERDES
        /CDR")
        I("XO/PLL") ~~~
        J("Multi-Core Processor/Subsystem Controller")
    end
    B <--> C
    Y[" "]
    Y -- SFI/XFI --> H
    H --> Y
    J <-- I2C --> X[" "]
    SOC ~~~
    K("Crystal 40Mhz") ~~~
    L("SLC NAND Flash") ~~~
    M("LPDDR3")
    style SOC fill:transparent,stroke:limegreen,stroke-width:2px,color:#fff,stroke-dasharray: 10 5
    style MAC fill:PapayaWhip,stroke:SandyBrown,color:transparent,stroke-width:2px
    classDef SEA fill:LightSkyBlue,font-weight:bold,stroke:DodgerBlue,stroke-width:2px
    classDef CORAL fill:PapayaWhip,font-weight:bold,stroke:SandyBrown,stroke-width:2px
    classDef CLEAR fill:transparent,stroke:transparent,color:transparent
    class A,C,F,G,I,J,K,H,L,M SEA
    class B,D,E,G CORAL
    class Z,Y,X CLEAR
```

## System Information

### Boot log

```
--8<-- "docs/xgs-pon/ont/potron-technology/x-onu-sfpp/bootlog"
```

### procfs [^3]

=== "/proc/cmdline"


    ```
    --8<-- "docs/xgs-pon/ont/potron-technology/x-onu-sfpp/procfs_cmdline"
    ```

=== "/proc/cpuinfo"


    ```
    --8<-- "docs/xgs-pon/ont/potron-technology/x-onu-sfpp/procfs_cpuinfo"
    ```

=== "/proc/meminfo"


    ```
    --8<-- "docs/xgs-pon/ont/potron-technology/x-onu-sfpp/procfs_meminfo"
    ```

=== "/proc/mtd"


    ```
    --8<-- "docs/xgs-pon/ont/potron-technology/x-onu-sfpp/procfs_mtd"
    ```

## Default Credentials

### Shell credentials

| Username | Password |
| -------- | -------- |
| root     |          |

### Bootloader

To access the U-Boot console type `admin` at the prompt: `Hit enter to stop autoboot`

## Value-Added Resellers

| Company                                             | Product Number    | E-commerce            |
| --------------------------------------------------- | ----------------- | --------------------- |
| [Full Vision Com-Tech](https://fullvisiontech.com/) | FV-NS10S          |                       |
| [H-COM](https://www.zhaoyongoptics.com/)            | SPP425H-GAB4      | [Alibaba](https://www.alibaba.com/product-detail/XGS-PON-ONU-SFP-Stick-with_1601261149622.html) / [AliExpress](https://www.aliexpress.com/item/1005007856556526.html) |

<small>^*^ Purchase at your discretion, we take no responsibility or liability for the listed resellers.</small>

[^1]: <https://www.potrontec.com/index/index/list/cat_id/2.html#11-83>
[^2]: <https://www.maxlinear.com/product/access/fiber-access/socs-for-optical-networking-units-onu/prx126>
[^3]: <https://en.wikipedia.org/wiki/Procfs>
[^4]: <https://boxmatrix.info/wiki/Property:Falcon>
