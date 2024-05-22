{%- macro star_cte(select_columns, cte_name = '', except=[]) -%}
    
    {%- set include_cols = [] -%}
    {%- set nsp = namespace(is_in_brackets = False) %} {# "Move the variable's scope to be global" #}

    {%- for col in select_columns.split(',') -%}
        {%- if ')' in col %} {# "Argments to functions shouldn't be treated as column names" #}
            {%- set nsp.is_in_brackets = False %}
        {%- elif '(' in col %}
            {%- set nsp.is_in_brackets = True %}
        {%- endif %}

        {%- set col_tidied = col.strip().split(' ') | last -%}

        {%- if col_tidied not in except and not nsp.is_in_brackets -%}
            {%- set _ = include_cols.append(col_tidied) -%}

        {%- endif -%}
    {%- endfor -%}

    {% for col in include_cols %}
        {% if cte_name | length > 0 %}
            {{- cte_name -}} .
        {%- endif -%}
        {{- col -}}
        {{- ", " if not loop.last }}
    {%- endfor -%}

{%- endmacro -%}