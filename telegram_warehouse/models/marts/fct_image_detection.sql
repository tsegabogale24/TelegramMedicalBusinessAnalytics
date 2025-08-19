{{ config(
    materialized='table',
    schema='raw_analytics'
) }}

WITH image_detections_clean AS (
    SELECT
        d.detection_id,
        d.image_id,
        LOWER(TRIM(d.detected_class)) AS detected_class,  -- corrected column name
        d.confidence_score
    FROM {{ ref('stg_image_detections') }} d
    WHERE d.detected_class IS NOT NULL
),

image_info AS (
    SELECT
        i.image_id,
        i.image_date
    FROM {{ ref('stg_telegram_images') }} i
)

SELECT
    d.detection_id,
    d.image_id,
    d.detected_class,
    d.confidence_score,
    i.image_date
FROM image_detections_clean d
LEFT JOIN image_info i
    ON d.image_id = i.image_id
