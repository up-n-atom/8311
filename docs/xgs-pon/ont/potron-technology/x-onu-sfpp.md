# X-ONU-SFPP (SFP+ XGSPON ONU Stick)

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

## Default Credentials

### Bootloader

To access the U-Boot console type `admin` at the prompt: `Hit enter to stop autoboot`

## Value-Added Resellers

| Company                                             | Product Number    | E-commerce            |
| --------------------------------------------------- | ----------------- | --------------------- |
| [Full Vision Com-Tech](https://fullvisiontech.com/) | FV-NS10S          | [Alibaba]             |

  [Alibaba]: https://quanjingtong.en.alibaba.com/index.html

[^1]: <https://www.potrontec.com/index/index/list/cat_id/2.html#11-83>
[^2]: <https://www.maxlinear.com/product/access/fiber-access/socs-for-optical-networking-units-onu/prx126>
