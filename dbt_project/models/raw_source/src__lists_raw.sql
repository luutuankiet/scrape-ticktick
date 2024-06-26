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
        {{ adapter.quote("id") }} :: text as "list_id",
        {{ adapter.quote("name") }} :: text as "list_name",
        {{ adapter.quote("isowner") }} :: boolean as "list_isowner",
        {{ adapter.quote("color") }} :: text as "list_color",
        {{ adapter.quote("inall") }} :: boolean as "list_inall",
        {{ adapter.quote("sortorder") }} :: bigint as "list_sortorder",
        {{ adapter.quote("sortoption") }} :: text as "list_sortoption", -- json
        {{ adapter.quote("sorttype") }} :: text as "list_sorttype",
        {{ adapter.quote("usercount") }} :: int as "list_usercount",
        {{ adapter.quote("etag") }} :: text as "list_etag",
        {{ adapter.quote("modifiedtime") }} :: timestamp as "list_modifiedtime",
        {{ adapter.quote("closed") }} :: boolean as "list_closed",
        {{ adapter.quote("muted") }} :: boolean as "list_muted",
        {{ adapter.quote("transferred") }} :: text as "list_transferred",
        {{ adapter.quote("groupid") }} :: text as "list_groupid",
        {{ adapter.quote("viewmode") }} :: text as "list_viewmode",
        {{ adapter.quote("notificationoptions") }} :: text as "list_notificationoptions",
        {{ adapter.quote("teamid") }} :: text as "list_teamid",
        {{ adapter.quote("permission") }} :: text as "list_permission",
        {{ adapter.quote("kind") }} :: text as "list_kind",
        {{ adapter.quote("timeline") }} :: text as "list_timeline", --json
        {{ adapter.quote("needaudit") }} :: boolean as "list_needaudit",
        {{ adapter.quote("barcodeneedaudit") }} :: boolean as "list_barcodeneedaudit",
        {{ adapter.quote("opentoteam") }} :: boolean as "list_opentoteam",
        {{ adapter.quote("teammemberpermission") }} :: text as "list_teammemberpermission",
        {{ adapter.quote("source") }} :: text as "list_source"
    FROM
        source
)
SELECT
    *
FROM
    renamed
