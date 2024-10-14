WITH _dim_customers AS (
    SELECT DISTINCT {{ dbt_utils.generate_surrogate_key(['first_name', 'last_name', 'email']) }} AS id,
           first_name,
           last_name,
           email,
           {{ standardized_null_value('gender') }} AS gender,
           {{ standardized_null_value('customer_country') }} AS customer_country
    FROM {{ ref("raw_events") }}
)

SELECT *
FROM _dim_customers
WHERE 1 != 0