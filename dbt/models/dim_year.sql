{{ config(materialized = 'table') }}

WITH date_series AS
(
SELECT
  *
FROM
  UNNEST(GENERATE_TIMESTAMP_ARRAY('2011-01-01', '2023-01-01', INTERVAL 1 DAY)) AS date
)
SELECT DISTINCT
    EXTRACT(YEAR FROM date) AS year
FROM date_series