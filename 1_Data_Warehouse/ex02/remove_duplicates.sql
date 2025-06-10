WITH duplicates AS (
    SELECT
        ctid,
        event_time,
        ROW_NUMBER() OVER (
            PARTITION BY event_type, product_id, price, user_id, user_session
            ORDER BY event_time
        ) AS rn,
        LAG(event_time) OVER (
            PARTITION BY event_type, product_id, price, user_id, user_session
            ORDER BY event_time
        ) AS prev_event_time
    FROM customers
)
DELETE FROM customers
WHERE ctid IN (
    SELECT ctid
    FROM duplicates
    WHERE rn > 1
      AND prev_event_time IS NOT NULL
      AND ABS(EXTRACT(EPOCH FROM (event_time - prev_event_time))) <= 1
);