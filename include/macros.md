{% macro image(text, url, align='center') -%}
![Image of {{ text }}]({{ "../../.." + url }}){ align={{ align }} }
{%- endmacro %}

{% macro iterate_images(onu) -%}
{% if onu.images is defined %}
{% for img in onu.images %}
{{ image(img[0], img[1]) }}
{% endfor %}
{% endif %}
{%- endmacro %}
