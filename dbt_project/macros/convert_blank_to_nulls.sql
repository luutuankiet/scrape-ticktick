-- macros/clean_columns.sql
{# description : this macro turns blank strings to NULLs. useful for raw data transforms.#}
{# usage : SELECT {{convert_balnk_to_nulls('table_name')}} from table_name  #}
{% macro convert_blank_to_null(
    table_name
  ) %}
  {# {% set relace_list = ["''", "[]"] %} #}
  {% set columns = adapter.get_columns_in_relation(table_name) %}
  {%- for col in columns  %}
    NULLIF(
      {{ col.name }},
      ''
    ) AS {{ col.name }}

    {% if not loop.last %},
    {% endif %}
  {% endfor %}
{% endmacro %}
