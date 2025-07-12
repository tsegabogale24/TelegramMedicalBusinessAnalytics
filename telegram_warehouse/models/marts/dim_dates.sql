{{ config(materialized='table', schema='analytics') }}

WITH dates AS (
  SELECT
    date::date AS date,
    EXTRACT(dow FROM date) AS day_of_week,
    EXTRACT(day FROM date) AS day_of_month,
    EXTRACT(month FROM date) AS month,
    EXTRACT(year FROM date) AS year
  FROM generate_series('2020-01-01'::date, CURRENT_DATE, interval '1 day') AS date
)

SELECT * FROM dates
