{% macro proxy_date_field(column) %}
{% if "{{ column }}" in ref("raw_events").columns %}
    {{ column }}
{% else %}
    CURRENT_DATE() AS "{{ column }}"
{% endif %}
{% endmacro %}