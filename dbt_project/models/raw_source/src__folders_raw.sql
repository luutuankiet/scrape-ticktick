{{ config(
    materialized = 'table'
) }}
WITH source_active AS (
    {# direct pull from tick api. contains current data. #}

    SELECT
        *
    FROM
        {{ source(
            'raw_data',
            'folders_raw'
        ) }}
),
source_snp AS (
    {# pulls the deleted portion of the data that is gone from tick api. #}
    SELECT
        *
    FROM
        {{ ref(
            'snp_folders_raw',
        ) }}
    WHERE dbt_valid_to is not null
),

source as (
    select 
        {{ setup_nulls(source('raw_data', 'folders_raw')) }}
        from source_active
    UNION ALL
    select 
        {{ setup_nulls(source('raw_data', 'folders_raw')) }}
        from source_snp
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