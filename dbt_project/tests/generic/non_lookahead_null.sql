{% test non_lookahead_null(
    model,
    column_name
) %}
{{ config (
    error_if = "!=0"
) }}

SELECT
    
        {{ column_name }}
    
FROM
    {{ model }}
WHERE
    {{ model }}.lookahead_flag IS FALSE 
    and {{ column_name }} is NULL
    {% endtest %}
