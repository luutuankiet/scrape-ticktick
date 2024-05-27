{{
  config(
    materialized = 'view',
    )
}}
select 
{{dbt_date.today()}}
as today