{{ config(
    materialized = 'table'
) }}

WITH raw_source_active AS (
    {# direct pull from tick api. contains current data. #}

    SELECT
        {{ dbt_utils.star(
            from = source(
                'raw_data',
                'lists_raw'
            ),
            except = ['modifiedtime']
        ) }},
        -- gotta explicitly handle this cauaes snap's data casted as timestamp
        modifiedtime :: text AS modifiedtime,
        ROW_NUMBER() over (
            PARTITION BY id
            ORDER BY
                modifiedtime DESC
        ) AS rn
    FROM
        {{ source(
            'raw_data',
            'lists_raw'
        ) }}
),
source_active AS (
    {# to handle de dupes #}
    SELECT
        *
    FROM
        raw_source_active
    WHERE
        rn = 1
),
source_snp AS (
    {# pulls the deleted portion of the data that is gone from tick api. #}
    SELECT
        {{dbt_utils.star(
            from=source('raw_data','lists_raw'),
            except=['modifiedtime']
        )}},
        -- gotta explicitly handle this cauaes snap's data casted as timestamp
        modifiedtime :: text as modifiedtime
    FROM
        {{ ref(
            'snp_lists_raw',
        ) }}
    WHERE dbt_valid_to is not null
    and id not in (
        select distinct id from source_active
        ) -- filters out those deleted with same id but diff etag, in which we favors the active data.
),

source as (
    select 
        {{ setup_nulls(source('raw_data', 'lists_raw')) }}
        from source_active
    UNION ALL
    select 
        {{ setup_nulls(source('raw_data', 'lists_raw')) }}
        from source_snp
),

renamed AS (
    SELECT
        {{ adapter.quote("id") }} :: text AS "list_id",
        {{ adapter.quote("name") }} :: text AS "list_name",
        {{ adapter.quote("isowner") }} :: BOOLEAN AS "list_isowner",
        {{ adapter.quote("color") }} :: text AS "list_color",
        {{ adapter.quote("inall") }} :: BOOLEAN AS "list_inall",
        {{ adapter.quote("sortorder") }} :: bigint AS "list_sortorder",
        {{ adapter.quote("sortoption") }} :: text AS "list_sortoption",
        -- json
        {{ adapter.quote("sorttype") }} :: text AS "list_sorttype",
        {{ adapter.quote("usercount") }} :: INT AS "list_usercount",
        {{ adapter.quote("etag") }} :: text AS "list_etag",
        {{ adapter.quote("modifiedtime") }} :: TIMESTAMP AS "list_modifiedtime",
        {{ adapter.quote("closed") }} :: BOOLEAN AS "list_closed",
        {{ adapter.quote("muted") }} :: BOOLEAN AS "list_muted",
        {{ adapter.quote("transferred") }} :: text AS "list_transferred",
        {{ adapter.quote("groupid") }} :: text AS "list_groupid",
        {{ adapter.quote("viewmode") }} :: text AS "list_viewmode",
        {{ adapter.quote("notificationoptions") }} :: text AS "list_notificationoptions",
        {{ adapter.quote("teamid") }} :: text AS "list_teamid",
        {{ adapter.quote("permission") }} :: text AS "list_permission",
        {{ adapter.quote("kind") }} :: text AS "list_kind",
        {{ adapter.quote("timeline") }} :: text AS "list_timeline",
        --json
        {{ adapter.quote("needaudit") }} :: BOOLEAN AS "list_needaudit",
        {{ adapter.quote("barcodeneedaudit") }} :: BOOLEAN AS "list_barcodeneedaudit",
        {{ adapter.quote("opentoteam") }} :: BOOLEAN AS "list_opentoteam",
        {{ adapter.quote("teammemberpermission") }} :: text AS "list_teammemberpermission",
        {{ adapter.quote("source") }} :: text AS "list_source"
    FROM
        source
    UNION
    SELECT
        'inbox120295392' :: text AS "list_id",
        'Inbox' :: text AS "list_name",
        '1' :: BOOLEAN AS "list_isowner",
        '' :: text AS "list_color",
        '1' :: BOOLEAN AS "list_inall",
        0 :: bigint AS "list_sortorder",
        '' :: text AS "list_sortoption",
        '' :: text AS "list_sorttype",
        1 :: INT AS "list_usercount",
        '' :: text AS "list_etag",
        '1900-01-01' :: TIMESTAMP AS "list_modifiedtime",
        '0' :: BOOLEAN AS "list_closed",
        '0' :: BOOLEAN AS "list_muted",
        '' :: text AS "list_transferred",
        '' :: text AS "list_groupid",
        '' :: text AS "list_viewmode",
        '' :: text AS "list_notificationoptions",
        '' :: text AS "list_teamid",
        '' :: text AS "list_permission",
        '' :: text AS "list_kind",
        '' :: text AS "list_timeline",
        '0' :: BOOLEAN AS "list_needaudit",
        '0' :: BOOLEAN AS "list_barcodeneedaudit",
        '0' :: BOOLEAN AS "list_opentoteam",
        '' :: text AS "list_teammemberpermission",
        '' :: text AS "list_source"
)
SELECT
    *
FROM
    renamed
