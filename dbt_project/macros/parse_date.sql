{%- macro parse_date(select_columns) -%}
{# macro to parse date from timestamp fields #}
    {% set select_columns = select_columns | map("lower") | list %}
    {% for col in select_columns %}
        LEFT(
            "{{col}}" :: text,
            10
        )::date AS "{{col}}_derived_date" {{ ", " if not loop.last }}
    {%- endfor -%}
{%- endmacro -%}
