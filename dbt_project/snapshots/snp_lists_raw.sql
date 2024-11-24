{% snapshot snp_lists_raw %}
  {{ config(
    target_schema = 'snapshots',
    strategy = 'timestamp',
    unique_key = 'id',
    updated_at = 'modifiedtime',
    invalidate_hard_deletes = true
  ) }}

  SELECT
    {{ dbt_utils.star(source('raw_data', 'lists_raw'), except = ['modifiedtime']) }},
    modifiedtime :: TIMESTAMP AS "modifiedtime"
  FROM
    {{ source(
      'raw_data',
      'lists_raw'
    ) }}
{% endsnapshot %}
