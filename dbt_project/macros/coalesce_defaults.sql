{% macro coalesce_defaults(
    table_name,
    seed = false
  ) %}
  {%- for col in adapter.get_columns_in_relation(table_name) %}
    {%- set default_value = 0 if col.data_type == "integer" else '1900-01-01' if col.data_type == "date" else 'default' if col.data_type == "text" else '1900-01-01 00:00:00' if col.data_type == "timestamp without time zone" else false if col.data_type == "boolean" 
    else '0' if col.data_type == "numeric"
    else '0.00' if col.data_type == "double precision"
    else 'default' -%}
    {%- if seed == false %}
      COALESCE(
        "{{ col.name }}",
        '{{default_value}}' :: {{ col.data_type }}
      ) AS {{ col.name }}
    {%- endif %}

    {%- if seed == true -%}
    {{ ' distinct ' if loop.first }}
      '{{default_value}}' :: {{ col.data_type }} AS {{ col.name }}
    {% endif %}

    {{ ',' if not loop.last }}
  {%- endfor -%}
{% endmacro %}
