---
title: XS-010X-Q (3FE48118AC) / CIG XG-99YF
---

# XS-010X-Q (3FE48118AC) / CIG XG-99YF

![XS-010X-Q](xs-010x-q/xs-010x-q.webp)

## Specifications

|             |                                                     |                     |
| ----------: | --------------------------------------------------- | ------------------- |
| __SoC__     | CA8271A - Taroko @ 500 MHz -                        | [CA8271A]           |
| __NAND__    | 128 MB *(1 Gbit)*                                   | [MX35LF1GE4AB]      |
| __RAM__     | 128 MB                                              | [NT5CC64M16GP]      |
| __BOSA__    | SC/APC - Tx: 1270 nm / Rx: 1577 nm                  | [M02181]            |
| __EEPROM__  | :check_mark:                                        | [M02181]            |
| __UART__    | TTL - 115200-8-1-N                                  |                     |
| __IP__      | 192.168.100.1                                       |                     |
| __HTTP(S)__ | :check_mark:                                        |                     |
| __Telnet__  | :check_mark:                                        |                     |

 [CA8271A]: https://www.cortina-access.com/index.php/products/single-family-unit-sfu-xpon-onu:
 [MX35LF1GE4AB]: https://www.mxic.com.tw/en-us/products/NAND-Flash/Serial-NAND-Flash/Pages/spec.aspx?p=MX35LF1GE4AB&m=Serial+NAND&n=PM2128&epn=MX35LF1GE4AB-Z4I
 [NT5CC64M16GP]: https://www.nanya.com/en/Product/3747/NT5CC64M16GP-DI
 [M02181]: https://www.macom.com/products/product-detail/MALD-02181
 [Shell credentials]: #shell-credentials

## System Information

### Boot log

```
--8<-- "docs/xgs-pon/ont/nokia/xs-010x-q/bootlog"
```

### procfs [^1]

=== "/proc/cpuinfo"


    ```
    --8<-- "docs/xgs-pon/ont/nokia/xs-010x-q/procfs_cpuinfo"
    ```

=== "/proc/meminfo"


    ```
    --8<-- "docs/xgs-pon/ont/nokia/xs-010x-q/procfs_meminfo"
    ```

=== "/proc/mtd"


    ```
    --8<-- "docs/xgs-pon/ont/nokia/xs-010x-q/procfs_mtd"
    ```

## Default Credentials

### Telnet credentials

| Username | Password       |
| -------- | -------------- |
| admin    | 1234           |

### Web credentials

| Username | Password       |
| -------- | -------------- |
| admin    | 1234           |

[^1]: <https://en.wikipedia.org/wiki/Procfs>
