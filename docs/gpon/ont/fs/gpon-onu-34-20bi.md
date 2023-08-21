{% from 'credentials.md' import credentials %}

# GPON-ONU-34-20BI

{% include "gpon/ont/sps-34-24t-hp-tdfo/specifications.md" %}

![Image of GPON-ONU-34-20BI](/img/gpon-onu-34-20bi.png){ align=center }

## Login Credentials

{% for cred in gpon_onu_34_20bi.credentials %}
{{ credentials(cred.type, cred.username, cred.password) }}
{% endfor %}

{% include "gpon/ont/sps-34-24t-hp-tdfo/connection-notices.md" %}

{% include "gpon/ont/sps-34-24t-hp-tdfo/backup-uboot-vars.md" %}

{% include "gpon/ont/sps-34-24t-hp-tdfo/backup-firmware.md" %}

{% include "gpon/ont/sps-34-24t-hp-tdfo/flashing-firmware.md" %}
