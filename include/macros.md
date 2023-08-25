{% macro iterate_credentials_heading(onu, lvl='##' ) -%}
{{ lvl }} Login Credentials

{% for cred in onu.credentials %}
{{ credentials(cred.type, cred.credentials) }}
{% endfor %}
{%- endmacro %}

{% macro iterate_credentials(onu) -%}
    {% for cred in onu.credentials %}
    {{ credentials(cred.type, cred.credentials) }}
    {% endfor %}
{%- endmacro %}

{% macro image(text, url, align='center') -%}
![Image of {{ text }}]({{ url }}){ align={{ align }} }
{%- endmacro %}

{% macro iterate_images(onu) -%}
{% if onu.images is defined %}
{% for img in onu.images %}
{{ image(img[0], img[1]) }}
{% endfor %}
{% endif %}
{%- endmacro %}
