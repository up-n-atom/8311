{% macro credentials(type, username, password) -%}
=== "{{ type }}"
    | Username       | Password       |
    | -------------- | -------------- |
    | {{ username }} | {{ password }} |
{%- endmacro %}

{% macro iterate_credentials_heading(onu) -%}
## Login Credentials

{% for cred in onu.credentials %}
{{ credentials(cred.type, cred.username, cred.password) }}
{% endfor %}
{%- endmacro %}

{% macro iterate_credentials(onu) -%}
    {% for cred in onu.credentials %}
    {{ credentials(cred.type, cred.username, cred.password) }}
    {% endfor %}
{%- endmacro %}