!!! warning "New installations"
    Keep the {{ page.meta.ont }} in active service for roughly a week or two until fully provisioned and the installation ticket
    has been closed.

???+ question "Common misconceptions and answers"

    __Do the WAS-110 or X-ONU-SFPP ONTs support GPON wavelengths, specifically 1490 nm downstream and 1310 nm upstream?__

    :   No, the BOSA in these ONTs is calibrated exclusively for XGS-PON wavelengths: 1577 nm downstream and
        1270 nm upstream. They use the Macom M02180 ([WAS-110]) and Macom M02181 ([X-ONU-SFPP]) laser drivers, which
        are designed specifically for 10G-PON applications.

    __Is the WAS-110 or X-ONU-SFPP a router?__

    :   No, the [WAS-110] and [X-ONU-SFPP] are __NOT__ substitutes for a Layer 7 router. They are SFU ONTs, as opposed to
        HGU, and their sole function is to convert Ethernet to PON over fiber. Additional hardware and software are
        required for internet access.

## Verify XGS-PON service

!!! info "3 Gbps or higher packages"
    If you're subscribed to Gigabit Fibe 3.0 or a similar 3 Gbps or higher package, skip past to [Purchase WAS-110/X-ONU-SFPP ONT].

  [Purchase WAS-110/X-ONU-SFPP ONT]: #purchase-was-110-x-onu-sfpp-ont

Your fiber internet subscription can use different underlying technologies. Use one of these methods to confirm if your
connection uses [XGS-PON]:

* [Web](#via-web) <small>recommended</small>
* [XMO client](#via-xmo-client)


### Via web <small>recommended</small> { #via-web data-toc-label="Via web" }

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

    1. The default Administrator password is located on the back [label] of the {{ page.meta.ont }}.

2. From the __WAN__ page, verify the displayed __current mode__ is XGS-PON.

{% if page.meta.ont == 'Home Hub 4000' %}
!!! info "Firmware version __1.7.11__ removed the helpful auto-detected mode output"

2. From the __WAN mode__ drop-down, switch from `AUTO` to `XGS-PON` and click __Save__. If your internet access doesn't
   drop out, you're subscribed on XGS-PON.
{% endif %}

### Via XMO client

The open-source XMO client[^1] requires Python 3.10 or newer. For installation instructions, see the Real Python guide:
[Python 3 Installation & Setup Guide](https://realpython.com/installing-python).

[^1]: <https://github.com/up-n-atom/sagemcom-modem-scripts>

<h4>Install client</h4>

Open a terminal and install the open-source XMO client using:

=== ":material-microsoft: Windows"

    ``` sh hl_lines="5"
    py --version # (1)!
    py -m venv venv
    venv\Scripts\activate
    py -m pip install --upgrade pip
    pip install https://github.com/up-n-atom/sagemcom-modem-scripts/releases/download/v0.0.10/xmo_remote_client-0.0.10-py3-none-any.whl
    ```

    1. Verify the installed Python version is >= __3.10__

=== ":simple-apple: macOS / :simple-linux: Linux"

    ``` sh hl_lines="5"
    python3 --version # (1)!
    python3 -m venv .venv
    . .venv/bin/activate
    python3 -m pip install --upgrade pip
    pip3 install https://github.com/up-n-atom/sagemcom-modem-scripts/releases/download/v0.0.10/xmo_remote_client-0.0.10-py3-none-any.whl
    ```

    1. Verify the installed Python version is >= __3.10__

<h4>Execute client</h4>

Finally, to determine if you have XGS-PON service, execute the following:

{% if page.meta.ont == 'Giga Hub' %}
``` sh
xmo-remote-client --password=<password> get-wan-mode # (1)!
```
{% else %}
``` sh
xmo-remote-client --password=<password> -a MD5 get-wan-mode # (1)!
```
{% endif %}

1. Replace the `<password>` argument. The default Administrator password is the serial number (S/N) located on the back [label] of the {{ page.meta.ont }}.

  [label]: #{{ page.meta.ont | lower | replace(" ", "-") }}-label

???- note "If your *current mode* is *GPON*, you should follow the [How to Bypass Gigahub for Bell Aliant (GPON)] guide instead"
    Before you begin, please be aware of the following important caveats to ensure a successful installation:

    1. Ensure you use the correct firmware image for your hardware:
         * __G-010S-P__ `alcatel-g010sp_new_busybox-squashfs.image`
         * __MA5671A__ or __GPON-ONU-34-20BI__ `huawei-ma5671a_new_busybox-squashfs.image`
    2. Install the non-themed firmware image(s). The themed versions don't render correctly in modern web browsers.
    3. Changing the language via the shell is easier than using the web UI. Run the following commands:
       ```
       uci set luci.main.lang='en'
       uci commit
       ```

  [XGS-PON]: ../xgs-pon/index.md
  [How to Bypass Gigahub for Bell Aliant (GPON)]: https://github.com/dukeseb/Bell-Gigahub-Bypass-GPON
  [WAS-110]: ../xgs-pon/ont/bfw-solutions/was-110.md
  [X-ONU-SFPP]: ../xgs-pon/ont/potron-technology/x-onu-sfpp.md
