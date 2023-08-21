{% import  'credentials.md' as includes %}
{% block device_name %}
# SPS-34-24T-HP-TDFO
{% endblock %}

{% include "gpon/ont/sps-34-24t-hp-tdfo/specifications.md" %}

{% block device_images %}
{% endblock %}

{% block vendor_specific %}
## Vendor Specific

### Login Credentials

=== "G-010S-P"
    {{ includes.iterate_credentials(g_010s_p) }}

=== "GPON-ONU-34-20BI"
    {{ includes.iterate_credentials(gpon_onu_34_20bi) }}

=== "MA5671A"
    {{ includes.iterate_credentials(ma5671a) }}

{% endblock %}

{% block device_credentials %}
{% endblock %}

{% include "gpon/ont/sps-34-24t-hp-tdfo/connection-notices.md" %}

{% include "gpon/ont/sps-34-24t-hp-tdfo/backup-uboot-vars.md" %}

{% include "gpon/ont/sps-34-24t-hp-tdfo/backup-firmware.md" %}

{% include "gpon/ont/sps-34-24t-hp-tdfo/flashing-firmware.md" %}
