WITH source AS (
    SELECT
        {{ setup_nulls(
            source(
                'raw_data',
                'lists_raw'
            )
        ) }}
    FROM
        {{ source(
            'raw_data',
            'lists_raw'
        ) }}
),
renamed AS (
    SELECT
        {{ adapter.quote("id") }},
        {{ adapter.quote("name") }},
        {{ adapter.quote("isowner") }},
        {{ adapter.quote("color") }},
        {{ adapter.quote("inall") }},
        {{ adapter.quote("sortorder") }},
        {{ adapter.quote("sortoption") }},
        {{ adapter.quote("sorttype") }},
        {{ adapter.quote("usercount") }},
        {{ adapter.quote("etag") }},
        {{ adapter.quote("modifiedtime") }},
        {{ adapter.quote("closed") }},
        {{ adapter.quote("muted") }},
        {{ adapter.quote("transferred") }},
        {{ adapter.quote("groupid") }},
        {{ adapter.quote("viewmode") }},
        {{ adapter.quote("notificationoptions") }},
        {{ adapter.quote("teamid") }},
        {{ adapter.quote("permission") }},
        {{ adapter.quote("kind") }},
        {{ adapter.quote("timeline") }},
        {{ adapter.quote("needaudit") }},
        {{ adapter.quote("barcodeneedaudit") }},
        {{ adapter.quote("opentoteam") }},
        {{ adapter.quote("teammemberpermission") }},
        {{ adapter.quote("source") }}
    FROM
        source
)
SELECT
    *
FROM
    renamed
