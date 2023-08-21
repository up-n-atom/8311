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