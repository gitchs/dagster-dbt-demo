{{
    config(
        materialized='view',
        schema='dw',
    )
}}


SELECT
users.*
,DATE_PART('year', AGE(NOW(), birthday::timestamp)) AS "age"
FROM {{source('ods', 'users')}} users
