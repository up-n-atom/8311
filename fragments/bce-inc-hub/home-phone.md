## Bell home phone

Bell does not provide SIP credentials, which requires the {{ page.meta.ont }} to remain in service. To integrate the
[WAS-110] or [X-ONU-SFPP], you must use a managed, unmanaged, or virtual switch to connect both devices and configure a
VLAN to bridge them.

  [WAS-110]: ../xgs-pon/ont/bfw-solutions/was-110.md
  [X-ONU-SFPP]: ../xgs-pon/ont/potron-technology/x-onu-sfpp.md

### Set {{ page.meta.ont }} WAN mode

<div class="swiper" markdown>

<div class="swiper-slide" markdown>

![{{ page.meta.ont }} Administrator login prompt]({{ page.meta.slug }}/{{ page.meta.ont | lower | replace(" ", "_") }}_login.webp){ loading=lazy }

</div>

<div class="swiper-slide" markdown>

![{{ page.meta.ont }} WAN mode]({{ page.meta.slug }}/{{ page.meta.ont | lower | replace(" ", "_") }}_wan_mode.webp){ loading=lazy }

</div>

</div>

1. Within a web browser, navigate to
   <https://home/?c=advancedtools/wan>
   and, if asked, input your Administrator password. (1)
   { .annotate }

    1. The default Administrator password is the serial number (S/N) located on the back [label] of the {{ page.meta.ont }}.

2. From the __WAN mode__ drop-down, switch to `WAN Ethernet` and click __Save__.

3. Set the __Voice WAN modes__ to include `wan` (default: `gpon,xgspon`) using the [xmo-remote-client](#via-xmo-client).

{% if page.meta.ont == 'Giga Hub' %}
    ``` sh
    xmo-remote-client --password=<password> set-value ---path "Device/Services/BellNetworkCfg/VoiceAllowedWANModes" --value "gpon,xgspon,wan" # (1)!
    ```
{% else %}
    ``` sh
    xmo-remote-client --password=<password> -a MD5 set-value ---path "Device/Services/BellNetworkCfg/VoiceAllowedWANModes" --value "gpon,xgspon,wan" # (1)!
    ```
{% endif %}

    1. Replace the `<password>` argument. The default Administrator password is the serial number (S/N) located on the back [label] of the {{ page.meta.ont }}.

### Set WAS-110/X-ONU-SFPP Internet VLAN

=== "Web"

    <div class="swiper">
    <div class="swiper-slide" markdown>
    ![WAS-110 login](shared-assets/was_110_luci_login.webp){ loading=lazy }
    </div>
    <div class="swiper-slide" markdown>
    ![WAS-110 8311 configuration ISP fixes](shared-assets/was_110_luci_config_fixes.webp){ loading=lazy }
    </div>
    </div>

    1. Within a web browser, navigate to
       <https://192.168.11.1/cgi-bin/luci/admin/8311/config>
       and, if asked, input your *root* [password]{ data-preview target="_blank" }.

    2. From the __8311 Configuration__ page, on the __ISP Fixes__ tab, set __Internet VLAN__ to `35`.

    3. __Save__ changes and reboot from the __System__ menu.

  [password]: ../xgs-pon/ont/bfw-solutions/was-110.md#web-credentials

=== "Shell"

    ```
    fwenv_set -8 internet_vlan 35
    ```
