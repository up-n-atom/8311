### Validate OLT authentication

!!! warning "Avoid direct eye contact with the end of the fiber optic cable"

After rebooting the [X-ONU-SFPP], safely remove the SC/APC fiber optic cable from the {{ page.meta.ont }} and
connect it to the [X-ONU-SFPP].

=== "X-ONU-SFPP"

    <h4>Check for O5.1 PLOAM status</h4>

    ![WAS-110 PON status](shared-assets/was_110_luci_pon_status.webp){ loading=lazy }

    1. Navigate to <https://192.168.11.1> and, if asked, input your default credentials, if you haven't changed them.
    2. From the __PON Status__ section, verify that the __PON PLOAM Status__ is in an *05.1, Associated state*.

    !!! tip "For troubleshooting, please read the [Troubleshoot connectivity issues with the WAS-110] guide's [PLOAM status] section."

      [PLOAM status]: troubleshoot-connectivity-issues-with-the-was-110.md#ploam-status

    <h4>Check for OLT associated VLAN filters</h4>

    3. Navigate to <https://192.168.11.1/cgi-bin/luci/admin/8311/vlans> and, if asked, input your root [password]{ data-preview target="_blank" }.
    4. From the __VLAN Tables__ page, if the __textarea__ states *"No Extended VLAN Tables Detected"*, the ONT configuration has not satisfied the OLT.