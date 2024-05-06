{{
    config(
        materialized='table',
        schema='report',
        tags=['daily']
    )
}}

select
submit_time::date "submit_date"
,sum(price) "daily_gmv"
FROM {{ref("dw_orders_with_user_profile")}}
GROUP BY 1
ORDER BY 1
