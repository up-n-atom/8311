## Verify ONT connectivity

!!! note "Do not be alarmed..."
    If you receive an e-mail and/or text informing you to:

    > Check your AT&T Fiber equipment since you might be offline currently.

    The {{ page.meta.ont }} sends telemetry data to *better* the customer experience.

### Hot plug fiber cable

!!! warning "Avoid direct eye contact with the end of the fiber optic cable"

After rebooting the [WAS-110] or [HLX-SFPX], safely remove the SC/APC fiber optic cable from the {{ page.meta.ont }} and
connect it to the [WAS-110] or [HLX-SFPX], confirmed by a double-clicking sound.

=== "WAS-110 / X-ONU-SFPP"

    ![WAS-110 PON status](shared-assets/was_110_luci_pon_status.webp){ loading=lazy }

    1. Navigate to <https://192.168.11.1/cgi-bin/luci/admin/status/overview> and, if asked, input your *root* [password]{ data-preview target="_blank" }.
    2. From the __PON Status__ section, evaluate that the __RX Power__ and __TX Power__ are within [spec](troubleshoot-connectivity-issues-with-the-was-110.md#optical-specifications){ data-preview target="_blank" }.

    !!! tip "For troubleshooting, please read the [Troubleshoot connectivity issues with the WAS-110] guide's [Optical status] section."

      [Optical status]: troubleshoot-connectivity-issues-with-the-was-110.md#optical-status

=== "HLX-SFPX"

    ![HLX-SFPX PON status](shared-assets/hlx_sfpx_pon_status.webp){ loading=lazy }

    1. Within a web browser, navigate to <http://192.168.33.1/> and, if asked, input the *useradmin*
       [web credentials]{ data-preview target="_blank" }.
    2. From the main navigation __Status__ drop-down, click __PON Interface__.
    3. From the __Optical Information__ section, evaluate that the __RX Power__ and __TX Power__ are within [spec](troubleshoot-connectivity-issues-with-the-was-110.md#optical-specifications){ data-preview target="_blank" }.

### Validate OLT authentication

=== "WAS-110 / X-ONU-SFPP"

    <h4>Check for O5.1 PLOAM status</h4>

    ![WAS-110 PON status](shared-assets/was_110_luci_pon_status.webp){ loading=lazy }

    1. Navigate to <https://192.168.11.1/cgi-bin/luci/admin/status/overview> and, if asked, input your *root* [password]{ data-preview target="_blank" }.
    2. From the __PON Status__ section, verify that the __PON PLOAM Status__ is in an *05.1, Associated state*.

    !!! tip "For troubleshooting, please read the [Troubleshoot connectivity issues with the WAS-110] guide's [PLOAM status] section."

      [PLOAM status]: troubleshoot-connectivity-issues-with-the-was-110.md#ploam-status

    <h4>Check for OLT associated VLAN filters</h4>

    1. Navigate to <https://192.168.11.1/cgi-bin/luci/admin/8311/vlans> and, if asked, input your root [password]{ data-preview target="_blank" }.
    2. From the __VLAN Tables__ page, if the __textarea__ states *"No Extended VLAN Tables Detected"*, the ONT configuration has not satisfied the OLT.

=== "HLX-SFPX"

    ![HLX-SFPX PON status](shared-assets/hlx_sfpx_pon_status.webp){ loading=lazy }

    1. Within a web browser, navigate to <http://192.168.33.1/> and, if asked, input the *useradmin*
       [web credentials]{ data-preview target="_blank" }.
    2. From the main navigation __Status__ drop-down, click __PON Interface__.
    3. From the __Link Information__ section, verify that the __PLOAM State__ is *05*.

  [Troubleshoot connectivity issues with the WAS-110]: troubleshoot-connectivity-issues-with-the-was-110.md
  [WAS-110]: ../xgs-pon/ont/bfw-solutions/was-110.md
  [HLX-SFPX]: ../xgs-pon/ont/calix/100-05610.md
