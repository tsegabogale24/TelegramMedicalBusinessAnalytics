{{ config(materialized='table', schema='analytics') }}

SELECT DISTINCT
    channel_name,
    -- Add other channel-related fields if available
    channel_name AS channel_key  -- surrogate key can be channel_name or a hash
FROM {{ ref('stg_telegram_messages') }}

