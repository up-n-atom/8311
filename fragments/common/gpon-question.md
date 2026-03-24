
    __Do the [WAS-110], [X-ONU-SFPP], [HLX-SFPX], or [WT-ONU-STICK] ONT's support GPON wavelengths (1490 nm downstream and 1310 nm upstream)?__

    :   No, the BOSA in these ONTs are calibrated exclusively for XGS-PON wavelengths: 1577 nm downstream and
        1270 nm upstream. They use the Macom M02180 ([WAS-110]), Macom M02181 ([X-ONU-SFPP]), and Semtech GN28L96
        ([HLX-SFPX]) laser drivers, which are designed specifically for 10G-PON applications.

  [WAS-110]: ../xgs-pon/ont/bfw-solutions/was-110.md
  [HLX-SFPX]: ../xgs-pon/ont/calix/100-05610.md
  [X-ONU-SFPP]: ../xgs-pon/ont/potron-technology/x-onu-sfpp.md
  [WT-ONU-STICK]: ../xgs-pon/ont/wintop-optical-technology/wt-onu-stick.md
