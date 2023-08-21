{% from 'credentials.md' import credentials %}
# SPS-34-24T-HP-TDFO

{% include "gpon/ont/sps-34-24t-hp-tdfo/specifications.md" %}

## Vendor Specific

### Login Credentials

=== "G-010S-P"
    {% for cred in g_010s_p.credentials %}
    {{ credentials(cred.type, cred.username, cred.password) }}
    {% endfor %}

=== "GPON-ONU-34-20BI"
    {% for cred in gpon_onu_34_20bi.credentials %}
    {{ credentials(cred.type, cred.username, cred.password) }}
    {% endfor %}

=== "MA5671A"
    {% for cred in ma5671a.credentials %}
    {{ credentials(cred.type, cred.username, cred.password) }}
    {% endfor %}

{% include "gpon/ont/sps-34-24t-hp-tdfo/connection-notices.md" %}

{% include "gpon/ont/sps-34-24t-hp-tdfo/backup-uboot-vars.md" %}

{% include "gpon/ont/sps-34-24t-hp-tdfo/backup-firmware.md" %}

{% include "gpon/ont/sps-34-24t-hp-tdfo/flashing-firmware.md" %}
