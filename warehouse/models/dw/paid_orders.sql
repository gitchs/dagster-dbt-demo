{{
    config(
        materialized='view',
        schema='dw',
    )
}}

SELECT * FROM {{ref('order_with_user_profile')}}
WHERE
status BETWEEN 1 AND 4 -- status map: 0未付款/1已付款/2已发货/3已签收/4确认收货/5退款
