WITH _finance_report AS (
    SELECT fe.product_value,
           dc.customer_country,
           CURRENT_DATE() AS transaction_date
    FROM {{ ref("fact_events") }} AS fe
    JOIN {{ ref("dim_customers") }} AS dc ON dc.id = fe.customer_id
)

SELECT CUSTOMER_COUNTRY,
       SUM(PRODUCT_VALUE) AS TOTAL_VALUE
FROM _finance_report
WHERE TRANSACTION_DATE BETWEEN DATE_TRUNC(month, CURRENT_DATE()) AND LAST_DAY(CURRENT_DATE())
GROUP BY CUSTOMER_COUNTRY