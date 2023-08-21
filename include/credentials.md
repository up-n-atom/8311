{% macro credentials(type, username, password) -%}
=== "{{ type }}"
    | Username       | Password       |
    | -------------- | -------------- |
    | {{ username }} | {{ password }} |
{%- endmacro %}
