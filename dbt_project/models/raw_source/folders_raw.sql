WITH source AS (
    SELECT
        {{ setup_nulls(
            source(
                'raw_data',
                'folders_raw'
            )
        ) }}
    FROM
        {{ source(
            'raw_data',
            'folders_raw'
        ) }}
),
renamed AS (
    SELECT
        {{ adapter.quote("id") }},
        {{ adapter.quote("etag") }},
        {{ adapter.quote("name") }},
        {{ adapter.quote("showall") }},
        {{ adapter.quote("sortorder") }},
        {{ adapter.quote("viewmode") }},
        {{ adapter.quote("deleted") }},
        {{ adapter.quote("userid") }},
        {{ adapter.quote("sorttype") }},
        {{ adapter.quote("sortoption") }},
        {{ adapter.quote("teamid") }},
        {{ adapter.quote("timeline") }}
    FROM
        source
)
SELECT
    *
FROM
    renamed
