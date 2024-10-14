{% macro standardized_null_value(column_name) %}

CASE
    WHEN {{ column_name }} IS NULL THEN 'Not Available'
    ELSE {{ column_name }}
END

{% endmacro %}