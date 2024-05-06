{{
    config(
        materialized='table',
        schema='report'
    )
}}

/*
2024年营收
*/

SELECT
SUM(price - coupon)
FROM {{ref("paid_orders")}}
WHERE submit_time BETWEEN '2024-01-01 00:00:00' AND '2024-12-31 23:59:59'