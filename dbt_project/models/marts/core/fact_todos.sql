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