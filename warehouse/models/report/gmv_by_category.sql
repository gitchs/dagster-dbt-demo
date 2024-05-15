{{
    config(
        materialized='table',
        schema='report',
        tags=['daily']
    )
}}

SELECT
category
,sum(dim_price) gmv
,sum(dim_price - dim_coupon) profit
FROM {{ref("dw_flattern_orders_with_user_profile")}}
GROUP BY category
ORDER BY gmv DESC
