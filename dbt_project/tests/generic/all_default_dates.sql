{% test all_default_dates(
    model,
    column_name
) %}
{{ config (
    error_if = "=1",
    warn_if = "<3"
) }}

WITH default_pool AS (

    SELECT
        "{{ column_name }}" AS default_dates
    FROM
        {{ model }}
    WHERE
        "{{ column_name }}" :: text LIKE '%1900%'
),
total_pool AS (
    SELECT
        "{{ column_name }}" AS default_dates
    FROM
        {{ model }}
)
SELECT
    *
FROM
    total_pool
EXCEPT
SELECT
    *
FROM
    default_pool {% endtest %}
