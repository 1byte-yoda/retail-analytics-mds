WITH _raw_events AS (
    SELECT *
    FROM {{ source("ae_exam", "events") }}
)

SELECT *
FROM _raw_events
WHERE 1 != 0
