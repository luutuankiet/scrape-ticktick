{# had to hardcode the pre hook cause otherwise the old dummy lookahead dates gonn persist & build up #}

{% macro cleanup_nulls(column_name) %}
    {% if execute %}
        -- Check if the table exists
        {% set table_exists_query %}
            SELECT COUNT(*)
            FROM information_schema.tables
            WHERE table_schema = '{{ this.schema }}'
              AND table_name = '{{ this.table }}'
        {% endset %}

        {% set table_exists_results = run_query(table_exists_query) %}
        {% set table_exists = table_exists_results.rows[0][0] > 0 %}

        -- Run the DELETE only if the table exists
        {% if table_exists %}
            DELETE FROM {{ this }}
            WHERE {{ column_name }} IS NULL;
        {% else %}
            {{ log("Skipping DELETE because the table does not exist.", info=True) }}
            select 1
        {% endif %}
    {% else %}
        -- Dry-run mode: Log the SQL
        {{ log("DELETE FROM " ~ this ~ " WHERE " ~ column_name ~ " IS NULL;", info=True) }}
    {% endif %}
{% endmacro %}
