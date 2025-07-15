{{ config(materialized='view') }}

SELECT
    id AS detection_id,
    image_id,
    TRIM(LOWER(detected_class)) AS detected_class,
    ROUND(confidence_score::numeric, 4) AS confidence_score
FROM {{ source('raw', 'image_detections') }}
