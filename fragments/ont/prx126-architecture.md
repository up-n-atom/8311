## Architecture

### MaxLinear PRX126 [^2]

# --8<-- [start:arch]
``` mermaid
%%{ init: { 'flowchart': { 'htmlLabels': false, 'curve': 'stepBefore' } } }%%
flowchart LR
  Z[" "] <-- Fiber --> A(BOSA)
  B("DRIVER/<br/>LA<br/>(PMD)")
  A --> B
  B --> A

  subgraph SOC
    C("SERDES<br/>/CDR")
    subgraph MAC
      D("10G(E)PON<br/>PCS&MAC/<br/>TC") ~~~
      E("10G-<br/>Ethernet<br/>PCS&MAC")
    end
    C <--> MAC
    F("Network<br/>Processsor<br/>/Package<br/>Switch")
    MAC <--> F
    G("10G-<br/>Ethernet<br/>PCS&<br/>MAC")
    F <--> G <--> H("SERDES<br/>/CDR")
    I("XO/PLL") ~~~
    J("Multi-Core Processor/Subsystem Controller")
  end

  B <--> C
  Y[" "]
  Y -- SFI/XFI --> H
  H --> Y
  J <-- I2C --> X[" "]

  SOC ~~~ K("Crystal 40Mhz") ~~~ L("SLC NAND Flash") ~~~ M("LPDDR3")

  classDef slateNode fill:#ffffff,stroke:#475569,stroke-width:2px,color:#1e293b
  classDef slateHighlight fill:#f1f5f9,stroke:#475569,stroke-width:2px,color:#1e293b
  classDef slateInterface fill:#334155,stroke:#1e293b,color:#ffffff,font-weight:bold
  classDef ghost fill:transparent,stroke:transparent,color:transparent

  style SOC fill:#f8fafc,stroke:#1e293b,stroke-width:2px,stroke-dasharray: 10 5
  style MAC fill:#e2e8f0,stroke:#64748b,stroke-width:2px

  class A,C,F,H,I,J,K,L,M slateNode
  class B,D,E,G slateHighlight
  class Z,Y,X ghost
```
# --8<-- [end:arch]
