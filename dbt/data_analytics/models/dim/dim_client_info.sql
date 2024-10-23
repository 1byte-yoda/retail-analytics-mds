WITH _dim_client_info AS (
    SELECT DISTINCT client_country
    FROM {{ ref("raw_events") }}
)

SELECT
    {{ dbt_utils.generate_surrogate_key(['client_country']) }} AS id
    ,{{ standardized_null_value('client_country') }} AS client_country
    ,CURRENT_TIMESTAMP() AS insertion_timestamp
FROM _dim_client_info
WHERE
    1 != 0
    {% if is_incremental() %}
        AND {{ dbt_utils.generate_surrogate_key(['client_country']) }} NOT IN (
            SELECT DISTINCT t.id
            FROM {{ this }} AS t
        )
    {% endif %}
