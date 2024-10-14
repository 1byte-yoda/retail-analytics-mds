WITH _raw_events AS (
    SELECT *
    FROM {{ source("ae_exam", "raw_events") }}
)

SELECT *
FROM _raw_events
WHERE 1 != 0