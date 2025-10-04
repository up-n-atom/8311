!!! warning "New installations"
    Keep the {{ page.meta.ont }} in active service for roughly a week or two until fully provisioned and the installation ticket
    has been closed.

???+ question "Common misconceptions and answers"

    __Can I take an SFP+ module provided by AT&T and plug it directly into my own router or switch?__

    :   No, the AT&T supplied SFP+ module is only a physical-layer transceiver compliant with XGS-PON
        ([ITU G.9807.1](../xgs-pon/index.md)). It lacks ONT management ([ITU G.988](../xgs-pon/index.md)), meaning it
        cannot function as a standalone ONT.

    __Do the WAS-110 or HLX-SFPX ONTs support GPON wavelengths, specifically 1490 nm downstream and 1310 nm upstream?__

    :   No, the BOSA in these ONTs is calibrated exclusively for XGS-PON wavelengths: 1577 nm downstream and
        1270 nm upstream. They use the Macom M02180 ([WAS-110]) and Semtech GN28L96 ([HLX-SFPX]) laser drivers, which
        are designed specifically for 10G-PON applications.

    __Is the WAS-110 or HLX-SFPX a router?__

    :   No, the [WAS-110] and [HLX-SFPX] are __NOT__ substitutes for a Layer 7 router. They are SFU ONTs, as opposed to
        HGU, and their sole function is to convert Ethernet to PON over fiber. Additional hardware and software are
        required for internet access.

## Determine if you're an XGS-PON subscriber

!!! info "2 Gbps or higher tiers"
    If you're subscribed to 2 GIG speed or a similar 2 Gbps or higher tier, skip past to
    [Purchase a WAS-110 or HLX-SFPX ONT].

There are two (2) methods to determine if you're an XGS-PON subscriber. First, through the [web UI](#with-the-web-ui)
Fiber Status page, and second, by inspecting the SFP [transceiver](#with-the-transceiver).

### with the web UI <small>recommended</small> { #with-the-web-ui data-toc-label="with the web UI" }

!!! info "Since the 6x series firmware, the web UI may report 0 (zero) for the Wave Length. Jump past to [with the transciever](#with-the-transceiver) to help determine if you're an XGS-PON subscriber."

![{{ page.meta.ont }} Fiber status]({{ page.meta.slug }}/bgw320_500_505_fiber_status.webp){ loading=lazy }

1. Within a web browser, navigate to
   <http://192.168.1.254/cgi-bin/fiberstat.ha>
2. Check the status listing for the __Wave Length__ value. A reading of *1270 nm* indicates an XGS-PON subscription.

### with the transceiver

![Nokia Transceiver](shared-assets/transceiver.webp){ loading=lazy }

1. Identify the bale clasp color. If *orange/red* :red_circle:, proceed.
2. Engage the bale clasp to release the latch and pull out the transceiver.
3. Inspect the label for *XGS-PON* or *1270* TX.

!!! note "If your wavelength is *1310 nm* and/or the bale clasp is *green* :green_circle:, you're using [GPON] and should follow the [PON Madness] guide instead"

  [GPON]: ../gpon/index.md
  [PON Madness]: https://docs.google.com/document/d/1gcT0sJKLmV816LK0lROCoywk9lXbPQ7l_4jhzGIgoTo
