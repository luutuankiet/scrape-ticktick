{% test all_default_dates(
    model,
    column_name
) %}
WITH cte AS (
    SELECT
        DISTINCT {{ column_name }} AS default_dates
    FROM
        {{ model }}
),
test_case AS (
    SELECT
        default_dates,
        DENSE_RANK() over (
            ORDER BY
                default_dates
        ) AS rnk
    FROM
        cte
),
results AS(
    SELECT
        CASE
            WHEN exists (
                SELECT
                    default_dates
                FROM
                    test_case
                WHERE
                    rnk > 1
            ) THEN 'fail'
            ELSE NULL
        END
)
SELECT
    *
FROM
    results {% endtest %}
