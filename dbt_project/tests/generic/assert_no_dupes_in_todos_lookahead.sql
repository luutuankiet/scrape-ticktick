{% test assert_no_dupes_in_todos_lookahead(model, column_name) %}
WITH test1_within_window AS (
    -- buid data points
    SELECT
        COUNT(*) AS cnt_lookahead_dates
    FROM
        {{ model }}
    WHERE
        todo_id IS NULL
),
test1_result AS (
    SELECT
        *
    FROM
        test1_within_window
    WHERE
        cnt_lookahead_dates >= {{ var('lookahead_window') }} + 5
),
test2_no_dupes AS (
    SELECT
        1
    FROM
        {{ model }}
    WHERE
        todo_id IS NOT NULL
    GROUP BY
        todo_id
    HAVING
        COUNT(todo_id) > 2
)
SELECT
    *
FROM
    test1_result
UNION ALL
SELECT
    *
FROM
    test2_no_dupes

{% endtest %}