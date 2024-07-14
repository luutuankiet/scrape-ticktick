{{ config(
    materialized = 'incremental',
    unique_key = ['todo_id'],
    on_schema_change='append_new_columns'
) }}

{% set datetime_list = ['todo_createdtime', 'todo_completedtime', 'todo_startdate', 'todo_duedate', 'todo_modifiedtime'] %}
WITH source AS (

    SELECT
        {{ setup_nulls(source('raw_data', 'tasks_raw')) }}
    FROM
        {{ source(
            'raw_data',
            'tasks_raw'
        ) }}
),
renamed AS (
    SELECT
        DISTINCT {{ adapter.quote("id") }} :: text AS "todo_id",
        {{ adapter.quote("completedtime") }} :: TIMESTAMP AS "todo_completedtime",
        {# these dates MUST be converted to ETC #}
        {{ adapter.quote("startdate") }} :: TIMESTAMP + INTERVAL '7 hours' AS "todo_startdate",
        {{ adapter.quote("duedate") }} :: TIMESTAMP + INTERVAL '7 hours' AS "todo_duedate",
        {{ adapter.quote("modifiedtime") }} :: TIMESTAMP + INTERVAL '7 hours' AS "todo_modifiedtime",
        {{ adapter.quote("createdtime") }} :: TIMESTAMP + INTERVAL '7 hours' AS "todo_createdtime",
        {{ adapter.quote("repeatfirstdate") }} :: TIMESTAMP + INTERVAL '7 hours' AS "todo_repeatfirstdate",

        {#                                           #}
        {{ adapter.quote("projectid") }} :: text AS "todo_projectid",
        {{ adapter.quote("sortorder") }} :: bigint AS "todo_sortorder",
        {{ adapter.quote("title") }} :: text AS "todo_title",
        {{ adapter.quote("content") }} :: text AS "todo_content",
        {{ adapter.quote("desc") }} :: text AS "todo_desc",
        {{ adapter.quote("timezone") }} :: text AS "todo_timezone",
        {{ adapter.quote("isfloating") }} :: BOOLEAN AS "todo_isfloating",
        {{ adapter.quote("isallday") }} :: BOOLEAN AS "todo_isallday",
        {{ adapter.quote("reminder") }} :: text AS "todo_reminder",
        {{ adapter.quote("reminders") }} :: text AS "reminders",
        -- array
        {{ adapter.quote("exdate") }} :: text AS "todo_exdate",
        {{ adapter.quote("priority") }} :: INT AS "todo_priority",
        {{ adapter.quote("status") }} :: text AS "todo_status",
        {{ adapter.quote("items") }} :: text AS "todo_items",
        {{ adapter.quote("progress") }} :: FLOAT AS "todo_progress",
        {{ adapter.quote("etag") }} :: text AS "todo_etag",
        {{ adapter.quote("deleted") }} :: BOOLEAN AS "todo_deleted",
        {{ adapter.quote("creator") }} :: INT AS "todo_creator",
        {{ adapter.quote("focussummaries") }} :: text AS "todo_focussummaries",
        {{ adapter.quote("columnid") }} :: text AS "todo_columnid",
        {{ adapter.quote("kind") }} :: text AS "todo_kind",
        {{ adapter.quote("imgmode") }} :: text AS "todo_imgmode",
        {{ adapter.quote("tags") }} :: text AS "todo_tags",
        {{ adapter.quote("repeatfrom") }} :: INT AS "todo_repeatfrom",
        {{ adapter.quote("attachments") }} :: text AS "todo_attachments",
        -- json
        {{ adapter.quote("repeattaskid") }} :: text AS "todo_repeattaskid",
        {{ adapter.quote("commentcount") }} :: FLOAT AS "todo_commentcount",
        {{ adapter.quote("completeduserid") }} :: text AS "todo_completeduserid",
        -- "120295392.0"
        {{ adapter.quote("repeatflag") }} :: text AS "todo_repeatflag",
        {{ adapter.quote("pinnedtime") }} :: TIMESTAMP AS "todo_pinnedtime",
        {{ adapter.quote("childids") }} :: text AS "childids",
        -- array
        {{ adapter.quote("deletedtime") }} :: text AS "todo_deletedtime",
        -- some weird epoc time ? "120295392.0" >>> to_timestamp(1669956236000 / 1000)
        {{ adapter.quote("pomodorosummaries") }} :: text AS "todo_pomodorosummaries",
        -- array
        {{ adapter.quote("parentid") }} :: text AS "todo_parentid",
        {{ adapter.quote("annoyingalert") }} :: text AS "todo_annoyingalert",
        {{ adapter.quote("modifiedtime_humanize") }} :: text AS "todo_modifiedtime_humanize",
        ROW_NUMBER() over(
            PARTITION BY {{ dbt_utils.star(
                from = source(
                    'raw_data',
                    'tasks_raw'
                )
            ) }}
            ORDER BY
                modifiedtime DESC
        ) AS rn
    FROM
        source
    GROUP BY
        {{ dbt_utils.star(
            from = source(
                'raw_data',
                'tasks_raw'
            )
        ) }}
),
refine_dates AS (
    {# create derived fields to parse date from timestamp fields #}
    SELECT
        DISTINCT *,
        {{ parse_date(datetime_list) }}
    FROM
        renamed
    WHERE
        rn = 1
)
SELECT
    *
FROM
    refine_dates
