{{
  config(
    materialized = 'view',
    )
}}
{% set today_offset_1 = (modules.datetime.datetime.now() - modules.datetime.timedelta(days=1)).strftime("%Y-%m-%d")%}
{% set today_lookahead = (modules.datetime.datetime.now() + modules.datetime.timedelta(days=var('lookahead_window'))).strftime("%Y-%m-%d")%}
WITH source AS (
    SELECT
        *
    FROM
        {{ ref(
            'date_seed'
        ) }}

        where 
        date_id::date >= '{{today_offset_1}}'::date
        and
        date_id::date <= '{{today_lookahead}}'::date
)
SELECT
    {{ dbt_utils.generate_surrogate_key(['date_id']) }} AS date_key,*
FROM
    source
