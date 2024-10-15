WITH _fact_events AS (
    SELECT
        transaction_id,
        purchase_price,
        product_value,
        product_name,
        {{ proxy_date_field('TRANSACTION_DATE') }},
        {{ dbt_utils.generate_surrogate_key(['first_name', 'last_name', 'email']) }} AS customer_id,
        {{ dbt_utils.generate_surrogate_key(['client_country']) }} AS client_info_id
    FROM {{ ref("raw_events") }}
)

SELECT *
FROM _fact_events
WHERE 1 != 0
