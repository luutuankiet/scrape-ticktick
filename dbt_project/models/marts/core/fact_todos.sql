{{ config(
    materialized='incremental',
    unique_key = ['todo_id'],
    on_schema_change='append_new_columns',
    indexes=[
      {'columns': ['list_key'], 'type': 'hash'},
      {'columns': ['folder_key'], 'type': 'hash'},
      {'columns': ['status_key'], 'type': 'hash'},
      {'columns': ['date_start_key'], 'type': 'hash'},
      {'columns': ['date_due_key'], 'type': 'hash'},
      {'columns': ['date_completed_key'], 'type': 'hash'},
      {'columns': ['date_created_key'], 'type': 'hash'},
      {'columns': ['date_modified_key'], 'type': 'hash'},
      {'columns': ['date_due_lookahead_key'], 'type': 'hash'},
      {'columns': ['todo_key'], 'unique': True},
    ],
    unlogged=True,
    pre_hook="delete from {{this}} where todo_id is null"
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

    {# dont need a coalesce_defaults at fact table cause the nulls FK already hashed at stg fact  #}