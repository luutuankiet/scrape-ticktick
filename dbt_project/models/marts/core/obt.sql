{{
  config(
    materialized = 'view'
    )
}}
WITH f_todos AS (
    SELECT
        *
    FROM
        {{ ref('fact_todos') }}
),
d_lists AS (
    SELECT
        *
    FROM
        {{ ref('dim_lists') }}
),
d_folders AS (
    SELECT
        *
    FROM
        {{ ref('dim_folders') }}
),
d_statuses AS (
    SELECT
        *
    FROM
        {{ ref('dim_statuses') }}
),
d_start_dates AS (
    SELECT
        *
    FROM
        {{ ref('dim_dates') }}
),
d_due_dates AS (
    SELECT
        *
    FROM
        {{ ref('dim_dates') }}
),
d_created_dates AS (
    SELECT
        *
    FROM
        {{ ref('dim_dates') }}
),
d_completed_dates AS (
    SELECT
        *
    FROM
        {{ ref('dim_dates') }}
)
SELECT
    {{ dbt_utils.star(
        from = ref('fact_todos'),
        relation_alias = 'f_todos',
        except = [ 'list_key', 'folder_key','status_key','todo_key','date_start_key','date_due_key','date_completed_key', 'date_created_key','list_id','folder_id','status_id' ]
    ) }},
    {{ dbt_utils.star(
        from = ref('dim_lists'),
        relation_alias = 'd_lists',
        except = [ 'list_key' ]
    ) }},
    {{ dbt_utils.star(
        from = ref('dim_folders'),
        relation_alias = 'd_folders',
        except = [ 'folder_key' ]
    ) }},
    {{ dbt_utils.star(
        from = ref('dim_statuses'),
        relation_alias = 'd_statuses',
        except = [ 'status_key' ]
    ) }},
    -- dates roleplay
    {{ dbt_utils.star(
        from = ref('dim_dates'),
        relation_alias = 'd_start_dates',
        prefix = 'start_',
        except = [ 'date_key' ]
    ) }},
    {{ dbt_utils.star(
        from = ref('dim_dates'),
        relation_alias = 'd_due_dates',
        prefix = 'due_',
        except = [ 'date_key' ]
    ) }},
    {{ dbt_utils.star(
        from = ref('dim_dates'),
        relation_alias = 'd_completed_dates',
        prefix = 'completed_',
        except = [ 'date_key' ]
    ) }},
    {{ dbt_utils.star(
        from = ref('dim_dates'),
        relation_alias = 'd_created_dates',
        prefix = 'created_',
        except = [ 'date_key' ]
    ) }}
FROM
    f_todos
    LEFT JOIN d_lists
    ON f_todos.list_key = d_lists.list_key
    LEFT JOIN d_folders
    ON f_todos.folder_key = d_folders.folder_key
    LEFT JOIN d_statuses
    ON f_todos.status_key = d_statuses.status_key
    LEFT JOIN d_start_dates
    ON f_todos.date_start_key = d_start_dates.date_key
    LEFT JOIN d_due_dates
    ON f_todos.date_due_key = d_due_dates.date_key
    LEFT JOIN d_completed_dates
    ON f_todos.date_completed_key = d_completed_dates.date_key
    LEFT JOIN d_created_dates
    ON f_todos.date_created_key = d_created_dates.date_key
