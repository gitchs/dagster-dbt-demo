{{
    config(
        materialized='view',
        schema='dw',
    )
}}

SELECT * FROM {{ref('dw_orders_with_user_profile')}}
WHERE
status BETWEEN 1 AND 4
