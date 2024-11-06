WITH source AS (
    SELECT
        *
    FROM
        {{ ref('lvl1_lvl2_progress') }}
),
ref_seeds AS (
    SELECT
        *
    FROM
        {{ ref('list_goal_mapping') }}
),
new_seeds AS (
    SELECT
        folder_name,
        list_name,
        '' AS goals
    FROM
        source
    WHERE folder_name != 'default'
    
)
SELECT
    n.folder_name,
    n.list_name,
    r.goals
FROM
    new_seeds n
    LEFT JOIN ref_seeds r
    ON r.folder_name = n.folder_name
    AND r.list_name = n.list_name
order by 1,2,3