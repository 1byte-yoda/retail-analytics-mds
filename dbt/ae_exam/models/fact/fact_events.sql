{{
    config(materialized='incremental', on_schema_change='sync_all_columns')
}}


WITH _fact_events AS (
    SELECT
        transaction_id
        ,purchase_price
        ,product_value
        ,product_name
        ,{{ proxy_date_field('TRANSACTION_DATE') }}
        ,{{ dbt_utils.generate_surrogate_key(['first_name', 'last_name', 'email']) }} AS customer_id
        ,{{ dbt_utils.generate_surrogate_key(['client_country']) }} AS client_info_id
        ,CURRENT_TIMESTAMP() AS insertion_timestamp
    FROM {{ ref("raw_events") }}
)

SELECT fe.*
FROM _fact_events AS fe
WHERE
    1 != 0
    {% if is_incremental() %}
        AND fe.transaction_id > (SELECT MAX(t.transaction_id) AS max_id FROM {{ this }} AS t)
    {% endif %}
