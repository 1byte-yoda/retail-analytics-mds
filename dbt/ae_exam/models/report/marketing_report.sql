WITH _marketing_report AS (
    SELECT
        fe.transaction_id,
        dc.customer_country,
        transaction_date
    FROM {{ ref("fact_events") }} AS fe
    INNER JOIN {{ ref("dim_customers") }} AS dc ON fe.customer_id = dc.id
)

SELECT
    customer_country,
    COUNT(transaction_id) AS total_transactions
FROM _marketing_report
WHERE transaction_date BETWEEN DATE_TRUNC(MONTH, CURRENT_DATE()) AND LAST_DAY(CURRENT_DATE())
GROUP BY customer_country
