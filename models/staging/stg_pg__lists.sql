WITH source AS (
    SELECT *
    FROM
        {{ source (
            'raw_data',
            'raw_data'
        ) }}
),

stg_lists AS (
    SELECT DISTINCT
        list_id,
        list_name::text AS list_name,
        isactive::boolean AS is_active,
        created_time::timestamp AS created_time
    FROM
        (
            SELECT
                "List Name" AS list_name,
                created_time,
                ROW_NUMBER() OVER (
                    ORDER BY
                        created_time ASC
                ) AS list_id,
                CASE
                    WHEN "List Name" LIKE '!%' THEN 0
                    ELSE 1
                END AS isactive
            FROM
                (
                    SELECT
                        "List Name",
                        MIN("Created Time") AS created_time
                    FROM
                        source
                    GROUP BY
                        "List Name"
                ) AS p1
        ) AS p2
)

SELECT
    {{ dbt_utils.generate_surrogate_key(['list_id']) }} AS list_key,
    *
FROM
    stg_lists
