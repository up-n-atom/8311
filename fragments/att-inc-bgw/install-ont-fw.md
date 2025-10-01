## Install ONT firmware

=== "WAS-110"

    Although not strictly necessary for AT&T, the 8311 community firmware is highly recommended for masquerading as
    the {{ page.meta.ont }} and used for the remainder of the [WAS-110] sections of this guide.

    There are two (2) methods to install the 8311 community firmware onto the [WAS-110], outlined in the following guides:

    <div class="grid cards" markdown>

    -    __Method 1: <small>recommended</small>__

         [Install the 8311 community firmware on the WAS-110](install-the-8311-community-firmware-on-the-was-110.md)

    -    __Method 2__

         [WAS-110 multicast upgrade and community firmware recovery](was-110-mulicast-upgrade-and-community-firmware-recovery.md)

    </div>

=== "HLX-SFPX"

    [HALNy] has provided a custom firmware with satisfactory customization for masquerading as the {{ page.meta.ont }}.
    It's available by request from [HALNy] and has been made available for download at:

    <https://active-fw.fibrain.pl/aktywa/MATERIALY/HALNy/HLX-SFPX/FIRMWARE/HLX-SFPX_V7-0-8pt2.zip>

    <div class="swiper" markdown>

    <div class="swiper-slide" step="2" markdown>

    ![HLX-SFPX Firmware](shared-assets/hlx_sfpx_firmware.webp){ loading=lazy }

    </div>

    <div class="swiper-slide" step="3" markdown>

    ![HLX-SFPX Firmware Select](shared-assets/hlx_sfpx_firmware_select.webp){ loading=lazy }

    </div>

    </div>

    1. Within a web browser, navigate to <https://192.168.33.1/> and, if asked, input the *useradmin*
       [web credentials]{ data-preview target="_blank" }.
    2. From the main navigation __System__ drop-down, click __Flash Firmware__.
    3. From the __Flash Firmware__ page, click __Choose Image__, browse for `G_ONU_HLX_SFPX_V7-0-8pt2-e.bin`, and click
       __Flash__ to proceed with flashing the firwmare.
    4. Follow the prompts.
