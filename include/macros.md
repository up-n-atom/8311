{% macro image(text, url, align='center') -%}
![Image of {{ text }}]({{ "../../.." + url }}){ align={{ align }} }
{%- endmacro %}

{% macro iterate_images(onu) -%}
{% if onu.images is defined %}
## Images
{% for img in onu.images %}
=== "{{ img[0] }}"
    {{ image(img[0], img[1]) }}
{% endfor %}
{% endif %}
{%- endmacro %}

{% macro render_content_group(group, heading_level=2) -%}
{{ heading(heading_level) + group.heading if group.heading is defined and group.heading is not none }}
{% if group.sections is defined %}
{% for section in group.sections %}
{% if section.heading is defined and section.sections is defined %}
{{ render_content_group(section, heading_level+1) }}
{% else %}
{% if section.title is defined and section.title is not none %}
{{ '=== "' + section.title + '"' if section.tab is defined and section.tab else heading(heading_level+1) + section.title }}
{% endif %}
{% if section.uri is defined and section.uri is not none %}
{% set output %}
{% include section.uri %}
{% endset %}
{{ nest(output) if section.tab is defined and section.tab else output }}
{% endif %}
{% endif %}
{% endfor %}
{% endif %}
{%- endmacro %}
