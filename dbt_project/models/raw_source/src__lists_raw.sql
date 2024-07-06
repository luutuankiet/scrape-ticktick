{{ config(
    materialized = 'incremental',
    unique_key = 'list_id'
) }}

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
)
SELECT
    *
FROM
    renamed
