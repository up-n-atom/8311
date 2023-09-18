{% macro image(text, url, align='center') -%}
![Image of {{ text }}]({{ "../../.." + url }}){ align={{ align }} }
{%- endmacro %}

{% macro iterate_images(onu) -%}
{% if onu.images is defined %}
{% for img in onu.images %}
=== "{{ img[0] }}"
    {{ image(img[0], img[1]) }}
{% endfor %}
{% endif %}
{%- endmacro %}

{% macro render_content_group(content_group) -%}
{% set group = include_content(content_group) %}
{% if group is defined and group is not none %}
{{ "## " + group.heading if group.heading is defined and group.heading is not none }}
{% if group.sections is defined %}
{% for section in group.sections %}
{% if section.title is defined and section.title is not none %}
{{ '=== "' + section.title + '"' if section.tab is defined and section.tab else "### " + section.title }}
{% endif %}
{% if section.uri is defined and section.uri is not none %}
{% set output %}
{% include section.uri %}
{% endset %}
{{ nest(output) if section.tab is defined and section.tab else output }}
{% endif %}
{% endfor %}
{% endif %}
{% endif %}
{%- endmacro %}
