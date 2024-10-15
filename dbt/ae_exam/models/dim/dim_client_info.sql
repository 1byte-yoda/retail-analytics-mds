WITH _dim_client_info AS (
    SELECT DISTINCT
        {{ dbt_utils.generate_surrogate_key(['client_country']) }} AS id,
        {{ standardized_null_value('client_country') }} AS client_country
    FROM {{ ref("raw_events") }}
)

SELECT *
FROM _dim_client_info
WHERE 1 != 0
