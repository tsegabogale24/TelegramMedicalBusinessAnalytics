SELECT
    d.detection_id,
    d.image_id,
    c.class_id,
    d.confidence_score,
     
    i.image_date
FROM {{ ref('stg_image_detections') }} d
LEFT JOIN {{ ref('dim_classes') }} c
  ON LOWER(TRIM(d.detected_class)) = c.class_name
LEFT JOIN {{ ref('stg_telegram_images') }} i
  ON d.image_id = i.image_id
