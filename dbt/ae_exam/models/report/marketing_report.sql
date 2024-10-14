WITH _marketing_report AS (
    SELECT fe.transaction_id,
           dc.customer_country,
           transaction_date
    FROM {{ ref("fact_events") }} AS fe
    JOIN {{ ref("dim_customers") }} AS dc ON dc.id = fe.customer_id
)

SELECT CUSTOMER_COUNTRY,
       COUNT(transaction_id) AS TOTAL_TRANSACTIONS
FROM _marketing_report
WHERE TRANSACTION_DATE BETWEEN DATE_TRUNC(month, CURRENT_DATE()) AND LAST_DAY(CURRENT_DATE())
GROUP BY CUSTOMER_COUNTRY
