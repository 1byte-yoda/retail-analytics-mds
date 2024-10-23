{% macro mask_value(column_name) %}
    CASE
        WHEN POSITION('@' IN {{ column_name }}) > 0 THEN
            CONCAT(
               LEFT({{ column_name }}, 1),
               REPEAT('*', POSITION('@' IN {{ column_name }}) - 2),
               '@',
               LEFT(SUBSTRING({{ column_name }}, POSITION('@' IN {{ column_name }}) + 1), 1),
               REPEAT('*', LENGTH(SUBSTRING({{ column_name }}, POSITION('@' IN {{ column_name }}) + 1)) - POSITION('.' IN SUBSTRING({{ column_name }}, POSITION('@' IN {{ column_name }}) + 1))),
               SUBSTRING(SUBSTRING({{ column_name }}, POSITION('@' IN {{ column_name }}) + 1), POSITION('.' IN SUBSTRING({{ column_name }}, POSITION('@' IN {{ column_name }}) + 1)))
            )
        ELSE
            CONCAT(
               LEFT({{ column_name }}, 2),
               REPEAT('*', LENGTH( {{column_name}} ) - 3),
               RIGHT({{ column_name }}, 1)
            )
    END
{% endmacro %}