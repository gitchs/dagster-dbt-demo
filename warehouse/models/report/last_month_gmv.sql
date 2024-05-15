{{
    config(
        tags=['monthly'],
    )
}}


SELECT
SUM(price - coupon)
FROM {{ref('dw_paid_orders')}}
WHERE 
submit_time BETWEEN DATE_TRUNC('month', NOW()) - interval '1 month'
AND (DATE_TRUNC('month', NOW()) - interval '1 second')
