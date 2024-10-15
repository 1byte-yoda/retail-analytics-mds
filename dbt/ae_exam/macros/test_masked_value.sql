{% test masked_value(model, column_name) %}
    WITH measurements AS (
        SELECT LEN({{ column_name }}) AS txt_length,
               LEN(REPLACE({{ column_name }}, '*', '')) asterisk_count
        FROM {{ model }}
    )

    SELECT *
    FROM measurements
    WHERE asterisk_count > txt_length
{% endtest %}