{{
    config(
        materialized='table',
        schema='dw',
    )
}}

select 
flattern_orders.*
,dim_goods.category
,dim_goods.name
,dim_goods.price AS dim_price
,dim_goods.profit AS dim_profit
,dim_goods.price - dim_goods.profit AS dim_coupon
from (
    select 
        orders.id
        ,orders.user_id
        ,orders.price
        ,orders.coupon
        ,json_array_elements(orders.goods_snapshot::json)::text::bigint good_id
        ,orders.user_gender
        ,orders.user_age
        ,orders.user_submit_age
    FROM {{ref('dw_orders_with_user_profile')}} orders
) flattern_orders
LEFT JOIN {{ref('goods')}} dim_goods
ON dim_goods.id = flattern_orders.good_id