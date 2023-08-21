{% extends "gpon/ont/sps-34-24t-hp-tdfo.md" %}
{% block device_name %}# GPON-ONU-34-20BI{% endblock %}
{% block device_images %}![Image of GPON-ONU-34-20BI](/img/gpon-onu-34-20bi.png){ align=center }{% endblock %}
{% block vendor_specific %}{% endblock %}
{% block device_credentials %}{{ includes.iterate_credentials(gpon_onu_34_20bi) }}{% endblock %}
