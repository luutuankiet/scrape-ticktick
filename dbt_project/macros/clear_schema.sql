{% macro clear_schema(schema_name) %}
{% set drop_schema_command = "DROP SCHEMA IF EXISTS " ~ schema_name ~ " CASCADE;" %}
{% do run_query(drop_schema_command) %}
{% endmacro %}