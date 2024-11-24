{% snapshot snp_folders_raw %}
  {{ config(
    target_schema = 'snapshots',
    strategy = 'check',
    unique_key = 'id',
    check_cols = 'all',
    invalidate_hard_deletes = true
  ) }}

  SELECT
    *
  FROM
    {{ source(
      'raw_data',
      'folders_raw'
    ) }}
{% endsnapshot %}
