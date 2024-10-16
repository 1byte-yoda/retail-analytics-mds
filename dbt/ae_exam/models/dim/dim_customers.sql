WITH _dim_customers AS (
    SELECT DISTINCT
        first_name
        ,last_name
        ,email
        ,gender
        ,customer_country
    FROM {{ ref("raw_events") }}
)

SELECT
    {{ dbt_utils.generate_surrogate_key(['first_name', 'last_name', 'email']) }} AS id,
    {{ mask_value('first_name') }} AS first_name,
    {{ mask_value('last_name') }} AS last_name,
    {{ mask_value('email') }} AS email
    ,CASE
        WHEN {{ standardized_null_value('gender') }} NOT IN ('Male','Female') THEN 'Others'
        ELSE {{ standardized_null_value('gender') }}
    END AS gender,
    {{ standardized_null_value('customer_country') }} AS customer_country
    ,CURRENT_TIMESTAMP() AS insertion_timestamp
FROM _dim_customers
WHERE 1 != 0
