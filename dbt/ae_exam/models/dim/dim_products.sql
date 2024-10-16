WITH _dim_products AS (
    SELECT DISTINCT
        product_name
    FROM {{ ref("raw_events") }}
)

SELECT
    {{ dbt_utils.generate_surrogate_key(['product_name']) }} AS id
    ,product_name
    ,CURRENT_TIMESTAMP() AS insertion_timestamp
FROM _dim_products
WHERE 1 != 0
