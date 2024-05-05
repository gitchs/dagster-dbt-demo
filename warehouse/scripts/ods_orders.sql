CREATE SCHEMA IF NOT EXISTS ods;
DROP TABLE IF EXISTS ods.users;
CREATE TABLE IF NOT EXISTS ods.users(
    id BIGSERIAL NOT NULL PRIMARY KEY
    ,firstname VARCHAR(64) NULL
    ,lastname VARCHAR(64) NULL
    ,phone_ciphertext VARCHAR(64) NOT NULL
    ,email_ciphertext VARCHAR(128) NOT NULL
    ,signup_time TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
    ,gender BOOLEAN
    ,birthday DATE
);
COMMENT ON TABLE ods.users is '交易系统用户表';
COMMENT ON COLUMN ods.users.id IS '交易系统用户ID';
COMMENT ON COLUMN ods.users.firstname IS '名';
COMMENT ON COLUMN ods.users.lastname IS '姓';
COMMENT ON COLUMN ods.users.phone_ciphertext IS '手机号密文';
COMMENT ON COLUMN ods.users.email_ciphertext IS '邮件密文';
COMMENT ON COLUMN ods.users.signup_time IS '注册时间';
COMMENT ON COLUMN ods.users.gender IS '性别, 0/1 ==> 女/男';
COMMENT ON COLUMN ods.users.birthday IS '出生日期';

INSERT INTO ods.users(id, firstname, lastname, phone_ciphertext, email_ciphertext, signup_time, gender, birthday) VALUES
(1, 'f0', 'l0', 'pc0', 'ec0', '2014-01-06 07:08:09', false, '1970-05-04')
,(2, 'f1', 'l1', 'pc1', 'ec1', '2014-02-06 07:08:09', false, '1970-06-04')
,(3, 'f2', 'l2', 'pc2', 'ec2', '2014-03-06 07:08:09', false, '1970-07-04')
,(4, 'f3', 'l3', 'pc3', 'ec3', '2014-04-06 07:08:09', false, '1970-08-04')
;

DROP TABLE IF EXISTS ods.orders;
CREATE TABLE IF NOT EXISTS ods.orders(
    id BIGSERIAL NOT NULL PRIMARY KEY
    ,user_id BIGINT NOT NULL
    ,goods_snapshot JSONB
    ,price NUMERIC(18, 2)
    ,coupon NUMERIC(18, 2)
    ,status smallint NOT NULL
    ,submit_time TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
    ,pay_time TIMESTAMPTZ NULL
);

COMMENT ON TABLE ods.orders IS '交易系统订单表';
COMMENT ON COLUMN ods.orders.id IS '交易订单ID';
COMMENT ON COLUMN ods.orders.user_id IS '发起交易订单用户ID';
COMMENT ON COLUMN ods.orders.goods_snapshot IS '订单交易快照';
COMMENT ON COLUMN ods.orders.price IS '订单交易价格';
COMMENT ON COLUMN ods.orders.coupou IS '订单交易补贴';
COMMENT ON COLUMN ods.orders.status IS '订单交易状态, 0未付款/1已付款/2已发货/3已签收/4确认收货/5退款';


INSERT INTO ods.orders(user_id, goods_snapshot, price, coupon, status, submit_time, pay_time) VALUES
(1, '[{"id": 1, "name": "sku1", "price": 1, "count": 5}]', 5, 0, 0, '2024-04-01 12:00:00', NULL)
,(1, '[{"id": 2, "name": "sku2", "price": 2, "count": 3}, {"id": 3, "name": "sku3", "price": 3, "count": 3}]', 15, 0, 4, '2024-04-01 13:00:00', '2024-04-01 13:01:00')
,(2, '[{"id": 1, "name": "sku1", "price": 1, "count": 5}]', 5, 0, 0, '2024-04-01 12:00:00', NULL)
,(2, '[{"id": 2, "name": "sku2", "price": 2, "count": 3}, {"id": 3, "name": "sku3", "price": 3, "count": 3}]', 15, 0, 2, '2024-04-01 13:00:00', '2024-04-01 13:05:00')
,(3, '[{"id": 1, "name": "sku1", "price": 1, "count": 5}]', 5, 0, 0, '2024-04-01 12:00:00', NULL)
,(3, '[{"id": 2, "name": "sku2", "price": 2, "count": 3}, {"id": 3, "name": "sku3", "price": 3, "count": 3}]', 15, 0, 3, '2024-04-01 13:00:00', '2024-04-01 13:10:00')
,(4, '[{"id": 1, "name": "sku1", "price": 1, "count": 5}]', 5, 0, 0, '2024-04-01 12:00:00', NULL)
,(4, '[{"id": 2, "name": "sku2", "price": 2, "count": 3}, {"id": 3, "name": "sku3", "price": 3, "count": 3}]', 15, 0, 5, '2024-04-01 13:00:00', '2024-04-01 13:15:00')
;
