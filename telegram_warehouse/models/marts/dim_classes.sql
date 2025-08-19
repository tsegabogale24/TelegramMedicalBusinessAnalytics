{{ config(
    materialized='table',
    schema='analytics'
) }}

SELECT DISTINCT
    LOWER(TRIM(detected_class)) AS class_name,
    MD5(LOWER(TRIM(detected_class))) AS class_id  -- Or use surrogate int IDs if preferred
FROM {{ ref('stg_image_detections') }}
WHERE detected_class IS NOT NULL

