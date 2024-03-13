WITH source AS (
    SELECT
        *
    FROM
        {{ ref('lvl1_lvl2_progress') }}
),
lvl3_goals AS (
    SELECT
        *
    FROM
        {{ ref('init_duckdb__lvl3') }}
),
ref_seeds AS (
    SELECT
        *
    FROM
        {{ ref('list_goal_mapping') }}
),
new_seeds AS (
    SELECT
        fld_folder_name,
        l_list_name,
        '' AS goal_ids
    FROM
        source
    UNION ALL
        (
            SELECT
                'goal',
                'id',
                '' AS goal_ids
            UNION ALL
            SELECT
                *,
                '' AS goal_ids
            FROM
                lvl3_goals
        )
)
SELECT
    n.fld_folder_name,
    n.l_list_name,
    r.goal_ids
FROM
    new_seeds n
    LEFT JOIN ref_seeds r
    ON r.fld_folder_name = n.fld_folder_name
    AND r.l_list_name = n.l_list_name
