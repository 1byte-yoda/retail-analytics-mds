{{
    config(
        materialized='incremental',
        on_schema_change='sync_all_columns',
        cluster_by=['customer_country']
    )
}}


WITH _fact_events AS (
    SELECT
        transaction_id
        ,purchase_price
        ,product_value
        ,{{ dbt_utils.generate_surrogate_key(['product_name']) }} AS product_id
        ,{{ proxy_date_field('TRANSACTION_DATE') }}
        ,{{ dbt_utils.generate_surrogate_key(['first_name', 'last_name', 'email']) }} AS customer_id
        ,{{ dbt_utils.generate_surrogate_key(['client_country']) }} AS client_info_id
        ,{{ standardized_null_value('customer_country') }} AS customer_country
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
