{# 
  description : this macro turns strings defined in a list to NULLs. useful for raw data transforms.
  usage : SELECT {{ setup_nulls('table_name') }} from table_name 
#}
{% macro setup_nulls(table_name) %}
  {% set replace_list = ["''", "'[]'","'nan'","'None'"] %}
  {% set columns = adapter.get_columns_in_relation(table_name) %}
  {%- for col in columns %}
    case 
      {%- for item in replace_list %}
        when "{{ col.name }}" = {{ item }} then NULL 
      {% endfor %}
      else "{{ col.name }}" 
    end as "{{ col.name }}"
    {% if not loop.last %}, {% endif %}
  {% endfor %}
{% endmacro %}
