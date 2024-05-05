{{
    config(
        materialized='view',
        schema='dw',
    )
}}

SELECT
orders.*
,users.gender
,users."age" "age"
,DATE_PART('year', AGE(orders.submit_time, users.birthday::timestamp)) AS "submit_age"
FROM {{source('ods', 'orders')}} orders
LEFT JOIN {{ref('users')}} users
ON orders.user_id = users.id