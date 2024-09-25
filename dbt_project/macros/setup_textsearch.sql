{% macro setup_textsearch() %}
  {% set sql %}
{# drop the index #}
  DROP INDEX IF EXISTS {{ env_var("TARGET_SCHEMA",'dev') }}.idx_search;

{# drop the func #}
  DROP FUNCTION IF EXISTS {{ env_var("TARGET_SCHEMA",'dev') }}.search_gtd;

ALTER TABLE
  {{ ref('fact_todos') }} DROP  search CASCADE;


ALTER TABLE
  {{ ref('fact_todos') }}
  --add the search index
ADD
  search tsvector generated always AS (
    setweight(to_tsvector('english', todo_title), 'A') || ' ' || setweight(to_tsvector('english', todo_content), 'A') || ' ' || setweight(to_tsvector('english', todo_list_name), 'B') || ' ' || setweight(to_tsvector('english', todo_folder_name), 'B') || ' ' || setweight(to_tsvector('simple', todo_tags), 'C') :: tsvector
  ) STORED;
-- add the index
  CREATE INDEX idx_search
  ON {{ ref('fact_todos') }} USING gin(search);
-- create the func
  CREATE
  OR REPLACE FUNCTION {{ env_var("TARGET_SCHEMA",'dev') }}.search_gtd (
    term text
  ) returns TABLE (
    todo_title text,
    todo_content text,
    todo_list_name text,
    todo_folder_name text,
    todo_tags text,
    link text,
    todo_duedate text,
    RANK REAL -- 'REAL' can be used, but 'NUMERIC' is often preferred for precision
  ) AS $$
SELECT
  todo_title,
  todo_content,
  todo_list_name,
  todo_folder_name,
  todo_tags,
  'ticktick://ticktick.com/webapp/#p/' || list_id || '/tasks/' || todo_id AS link,
  todo_duedate,
  ts_rank(search, websearch_to_tsquery('english', term)) + ts_rank(search, websearch_to_tsquery('simple', term)) AS RANK
FROM
  {{ ref('fact_todos') }}
WHERE
  (search @@ websearch_to_tsquery('english', term)
  OR search @@ websearch_to_tsquery('simple', term))
  AND todo_status = '0'
ORDER BY
  RANK DESC;$$ LANGUAGE SQL;
{% endset %}
  {% do run_query(sql) %}
  {% do log(
    "search column set up for fact_todos",
    info = True
  ) %}
{% endmacro %}
