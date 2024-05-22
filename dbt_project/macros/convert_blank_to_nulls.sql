-- macros/clean_columns.sql
{# description : this macro turns blank strings to NULLs. useful for raw data transforms.#}
{# usage : SELECT {{convert_balnk_to_nulls('table_name')}} from table_name  #}
{% macro convert_blank_to_null(
    table_name
  ) %}
  {%- for col in adapter.get_columns_in_relation(table_name) %}
    NULLIF(
      {{ col }},
      ''
    ) AS {{ col }}

    {% if not loop.last %},
    {% endif %}
  {% endfor %}
{% endmacro %}
