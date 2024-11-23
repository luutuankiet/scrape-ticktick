{{ config(
    materialized='incremental',
    unique_key = ['todo_id', 'date_due_lookahead_key'],
    incremental_strategy = 'merge',
    on_schema_change='append_new_columns',
) }}
WITH source AS (
    SELECT
        *
    FROM
        {{ ref('stg_todos') }}
)
SELECT
    *
FROM
    source

{% if is_incremental() %}
  WHERE  todo_modifiedtime >= (select coalesce(max(todo_modifiedtime),'1900-01-01 00:00:00') from {{ this }} )
{% endif %}

