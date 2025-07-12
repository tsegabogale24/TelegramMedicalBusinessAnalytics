{{ config(
    materialized = 'table',
    schema = 'staging'
) }}

WITH source AS (
    SELECT
        id,
        channel,
        raw_json
    FROM {{ source('raw', 'telegram_messages') }}
),

renamed_casted AS (
    SELECT
        id::BIGINT AS message_id,
        channel::TEXT AS channel_name,
        (raw_json->>'date')::TIMESTAMP AS message_date,
        (raw_json->>'text') AS message_text,
        (raw_json->>'file_path') AS file_path,
        raw_json
    FROM source
)

SELECT * FROM renamed_casted
