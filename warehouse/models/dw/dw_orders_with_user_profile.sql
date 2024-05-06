{{
    config(
        materialized='view',
        schema='dw',
    )
}}

SELECT
orders.*
,users.gender "user_gender"
,users."age" "user_age"
,DATE_PART('year', AGE(orders.submit_time, users.birthday::timestamp)) "user_submit_age"
FROM {{source('ods', 'orders')}} orders
LEFT JOIN {{ref('dw_users')}} users
ON orders.user_id = users.id