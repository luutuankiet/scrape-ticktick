{% test assert_not_null_non_lookahead(model, column_name) %}
WITH test1_within_window AS (
    -- buid data points
    SELECT
        'lookahead_dummy' as col
        ,COUNT(*) AS cnt
    FROM
        {{ model }}
    WHERE
        {{ column_name }} IS NULL
),
test1_result AS (
    SELECT
        *
    FROM
        test1_within_window
    WHERE
        cnt >= {{ var('lookahead_window') }} + 5
),
test2_not_null AS (
    SELECT
        {{ column_name }} :: text as col
        ,COUNT(*) AS cnt
    FROM
        {{ model }}
    WHERE
        {{ column_name }} IS NOT NULL
    GROUP BY
        {{ column_name }}
    HAVING
        COUNT({{ column_name }}) > 2
)
SELECT
    *
FROM
    test1_result
UNION ALL
SELECT
    *
FROM
    test2_not_null

{% endtest %}