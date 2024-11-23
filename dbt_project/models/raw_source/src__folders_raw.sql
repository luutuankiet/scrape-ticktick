{{ config(
    materialized = 'table'
) }}
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
        {{ adapter.quote("id") }} :: text AS "folder_id",
        {{ adapter.quote("etag") }} :: text AS "folder_etag",
        {{ adapter.quote("name") }} :: text AS "folder_name",
        {{ adapter.quote("showall") }} :: boolean AS "folder_showall",
        {{ adapter.quote("sortorder") }} :: bigint AS "folder_sortorder",
        {{ adapter.quote("viewmode") }} :: text AS "folder_viewmode",
        {{ adapter.quote("deleted") }} :: boolean AS "folder_deleted",
        {{ adapter.quote("userid") }} :: int AS "folder_userid",
        {{ adapter.quote("sorttype") }} :: text AS "folder_sorttype",
        {{ adapter.quote("sortoption") }} :: text AS "folder_sortoption",
        {{ adapter.quote("teamid") }} :: text AS "folder_teamid",
        {{ adapter.quote("timeline") }} :: text AS "folder_timeline"
    FROM
        source
)
SELECT
    *
FROM
    renamed