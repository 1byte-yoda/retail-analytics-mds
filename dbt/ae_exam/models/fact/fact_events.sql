{{
    config(materialized='incremental', on_schema_change='sync_all_columns')
}}


WITH _fact_events AS (
    SELECT
        transaction_id
        ,purchase_price
        ,product_value
        ,product_name,
        {{ proxy_date_field('TRANSACTION_DATE') }},
        {{ dbt_utils.generate_surrogate_key(['first_name', 'last_name', 'email']) }} AS customer_id
        ,{{ dbt_utils.generate_surrogate_key(['client_country']) }} AS client_info_id
        ,CURRENT_TIMESTAMP() AS insertion_timestamp
    FROM {{ ref("raw_events") }}
)

SELECT *
FROM _fact_events
WHERE
    1 != 0
    {% if is_incremental() %}
        AND transaction_id > (SELECT MAX(transaction_id) FROM {{ this }})
    {% endif %}
