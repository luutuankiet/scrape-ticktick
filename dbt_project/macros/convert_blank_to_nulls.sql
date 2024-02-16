-- macros/clean_columns.sql
{# description : this macro turns blank strings to NULLs. useful for raw data transforms.#}
{# TODO: update arg as a table to directly parse the table cols instead of having to parse from outside caller #}
{% macro convert_blank_to_null(columns) %}
  {% for col in columns %}
    NULLIF(
      {{ col }},
      ''
    ) AS {{ col }}

    {% if not loop.last %},
    {% endif %}
  {% endfor %}
{% endmacro %}
