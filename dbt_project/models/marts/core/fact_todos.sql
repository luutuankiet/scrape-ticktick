{# had to hardcode the pre hook cause otherwise the old dummy lookahead dates gonn persist & build up #}
{{ config(
    materialized='incremental',
    unique_key = ['todo_lookahead_skey'],
    incremental_strategy = 'merge',
    on_schema_change='append_new_columns',
    pre_hook = ['{{cleanup_nulls("todo_id")}}']
) }}
WITH source AS (
    SELECT
    DISTINCT

        *
    FROM
        {{ ref('stg_todos_join_lookahead') }}
        where todo_modifiedtime is null
)
SELECT
    *
FROM
    source

{% if is_incremental() %}
  WHERE  todo_modifiedtime >= (select coalesce(max(todo_modifiedtime),'1900-01-01 00:00:00') from {{ this }} )
OR
  todo_modifiedtime IS NULL
{% endif %}

