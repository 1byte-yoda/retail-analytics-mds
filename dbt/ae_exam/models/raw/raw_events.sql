WITH _raw_events AS (
    SELECT DISTINCT
        *,
        CURRENT_TIMESTAMP() AS insertion_timestamp
    FROM {{ source("ae_exam", "events") }}
)

SELECT *
FROM _raw_events
WHERE 1 != 0
