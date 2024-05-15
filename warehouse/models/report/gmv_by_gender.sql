{{
    config(
        materialized='table',
        schema="report",
        tags=['daily']
    )
}}


select
user_gender
,sum(dim_price) gmv
,sum(dim_price - dim_coupon) profit
FROM {{ref("dw_flattern_orders_with_user_profile")}}
GROUP BY user_gender
ORDER BY user_gender
