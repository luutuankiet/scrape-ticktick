{% macro coalesce_defaults(
    table_name,
    seed = false
  ) %}
  {%- for col in adapter.get_columns_in_relation(table_name) %}
    {%- set default_value = 0 if col.data_type.lower() in ["integer","numeric","bigint"] 
    else '1900-01-01' if col.data_type.lower() in "date" 
    else 'default' if col.data_type.lower() in ["text","string"] 
    else '1900-01-01 00:00:00' if col.data_type.lower() in "timestamp without time zone" 
    else '1900-01-01 00:00.000+0000' if col.data_type.lower() in "timestamp" 
    else 'false' if col.data_type.lower() in "boolean" 
    else '0' if col.data_type.lower() in "numeric" 
    else '0.00' if col.data_type.lower() in ["double precision","float"] 
    else 'default' -%}

    {%- if seed == false %}
      COALESCE(
        "{{ col.name }}",
        '{{default_value}}' :: {{ col.data_type }}
      ) AS {{ col.name }}
    {%- endif %}

    {%- if seed == true -%}
      {% if loop.first %}
         distinct NULL AS {{ col.name }}
      {% endif %}

      {% if not loop.first %}
        '{{default_value}}' :: {{ col.data_type }} AS {{ col.name }}
      {% endif %}
    {% endif %}

    {{ ',' if not loop.last }}
  {%- endfor -%}
{% endmacro %}
