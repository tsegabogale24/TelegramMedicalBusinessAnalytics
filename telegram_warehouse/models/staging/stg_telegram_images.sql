{{ config(
    materialized = 'table',
    schema = 'staging'
) }}

WITH source AS (
    SELECT
        id,
        channel,
        date,
        file_path,
        width,
        height,
        file_size_kb,
        format,
        mode
    FROM {{ source('raw', 'telegram_images') }}
),

renamed_casted AS (
    SELECT
        id::BIGINT AS image_id,
        channel::TEXT AS channel_name,
        date::TIMESTAMP AS image_date,
        file_path::TEXT AS image_path,
        width::INT,
        height::INT,
        file_size_kb::FLOAT,
        format::TEXT AS image_format,
        mode::TEXT AS color_mode
    FROM source
)

SELECT * FROM renamed_casted
