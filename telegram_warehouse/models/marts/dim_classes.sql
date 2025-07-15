-- models/marts/dim_classes.sql

SELECT DISTINCT
    LOWER(TRIM(detected_class)) AS class_name,
    MD5(LOWER(TRIM(detected_class))) AS class_id -- You can also use surrogate int ids if preferred
FROM {{ ref('stg_image_detections') }}
WHERE detected_class IS NOT NULL
