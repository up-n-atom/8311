---
hide:
  - feedback
links:
  - ../xgs-pon/index.md
---

# Gigabit Passive Optical Network

G-PON is a gigabit-capable passive optical network standard ([ITU-T](#itu-t-standards) G.984) that delivers
asymmetrical speeds of up to 2.5 Gbit/s downstream and 1.25 Gbit/s upstream.

It emerged as a successor to the EPON ([IEEE 802.3ah]) standard, offering higher bandwidth and greater efficiency. The
two standards share the same distinct wavelengths for downstream (1490 nm) and upstream (1310 nm). A differentiator
for G-PON is its optional use of a third wavelength (1550 nm) for downstream video overlay.

Despite this physical layer similarity, the standards are not compatible due to their fundamentally different framing
and management protocols. G-PON uses GEM framing and OMCI management, while EPON uses native Ethernet framing with
MPCP.

  [IEEE 802.3ah]: https://en.wikipedia.org/wiki/IEEE_802.3

## ITU-T Standards

<div class="grid cards" markdown>

-   __[G.984.1]__

    ---

    Gigabit-capable passive optical networks (GPON): General characteristics

-   __[G.984.2]__

    ---

    Gigabit-capable Passive Optical Networks (GPON): Physical Media Dependent (PMD) layer specification

-   __[G.984.3]__

    ---

    Gigabit-capable passive optical networks (GPON): Transmission convergence layer specification

-   __[G.984.4]__

    ---

    Gigabit-capable passive optical networks (GPON): ONT management and control interface specification

-   __[G.988]__

    ---

    ONU management and control interface (OMCI) specification

    ---

    <small>__The most relevent for those attempting to setup a bypass with compatible hardware__</small>

</div>

  [G.984.1]: https://www.itu.int/rec/T-REC-G.984.1/en
  [G.984.2]: https://www.itu.int/rec/T-REC-G.984.2/en
  [G.984.3]: https://www.itu.int/rec/T-REC-G.984.3/en
  [G.984.4]: https://www.itu.int/rec/T-REC-G.984.4/en
  [G.988]: http://www.itu.int/rec/T-REC-G.988/en
