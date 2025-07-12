{{ config(materialized='table', schema='analytics') }}

WITH msg AS (
    SELECT * FROM {{ ref('stg_telegram_messages') }}
)

SELECT
    msg.message_id,  -- or msg.id if that’s the correct column
    msg.channel_name,
    msg.message_date,
    LENGTH(msg.message_text) AS message_length,
    CASE WHEN msg.file_path IS NOT NULL THEN TRUE ELSE FALSE END AS has_image
FROM msg
