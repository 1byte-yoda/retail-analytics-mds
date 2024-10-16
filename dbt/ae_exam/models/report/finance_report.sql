WITH _finance_report AS (
    SELECT
        fe.product_value
        ,dc.customer_country
        ,fe.transaction_date
    FROM {{ ref("fact_events") }} AS fe
    INNER JOIN {{ ref("dim_customers") }} AS dc ON fe.customer_id = dc.id
)

SELECT
    customer_country
    ,SUM(product_value) AS total_value
FROM _finance_report
WHERE
    1 != 0
    AND transaction_date BETWEEN DATE_TRUNC(MONTH,CURRENT_DATE()) AND LAST_DAY(CURRENT_DATE())
GROUP BY customer_country
