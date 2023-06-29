/*Look through all tables first*/
use magist;
SELECT * FROM customers;
SELECT * FROM geo;
SELECT * FROM order_reviews;
SELECT * FROM order_payments;
SELECT * FROM order_items;
SELECT * FROM orders;
SELECT * FROM product_category_name_translation;
SELECT * FROM products;
SELECT * FROM sellers;

WITH category AS (
    SELECT
        product_category_name,
        CASE
            WHEN
                product_category_name_english LIKE 'au_%'
                OR product_category_name_english LIKE 'comp__%'
                OR product_category_name_english LIKE 'pc__%'
                OR product_category_name_english LIKE 'm%ic'
                OR product_category_name_english LIKE 'tele__%'
                OR product_category_name_english LIKE 'tab%'
                OR product_category_name_english LIKE 'wat%'
                OR product_category_name_english LIKE 'dvd%'
                OR product_category_name_english LIKE 'fix%'
                OR product_category_name_english LIKE 'ele%'
                OR product_category_name_english LIKE 'sec%'
                OR product_category_name_english LIKE 'sig%'
            THEN 'Apple_Tech'
            ELSE 'Others'
        END AS new_category
    FROM
        product_category_name_translation
),
category_counts AS (
    SELECT
        categories.new_category,
        COUNT(DISTINCT order_items.seller_id) AS total_sellers,
        COUNT(DISTINCT order_items.product_id) AS total_products,
        round(avg(order_items.price),2) as average_price
    FROM
        order_items
        JOIN products ON products.product_id = order_items.product_id
        JOIN category AS categories ON categories.product_category_name = products.product_category_name
    GROUP BY
        categories.new_category
)
SELECT
    new_category,
    total_sellers,
    total_products,
    ROUND((total_sellers / (SELECT COUNT(DISTINCT seller_id) FROM order_items)) * 100, 2) AS seller_percent,
    ROUND((total_products / (SELECT COUNT(DISTINCT product_id) FROM order_items)) * 100, 2) AS product_percent,
    average_price
    
FROM
    category_counts;


   SELECT 
    orders.order_id,
    order_items.product_id,
    category.product_category_name_english,
    category.new_category,
    products.product_weight_g,
    order_items.price,
    order_items.freight_value,
    orders.order_purchase_timestamp,
    orders.order_delivered_carrier_date,
    orders.order_delivered_customer_date,
    order_items.shipping_limit_date,
    orders.order_status,
    orders.delivery_type
FROM
    (SELECT 
        *,
            CASE
                WHEN
                    product_category_name_english LIKE 'au_%'
                        OR product_category_name_english LIKE 'comp__%'
                        OR product_category_name_english LIKE 'home_com_%'
                        OR product_category_name_english LIKE 'home_conf_%'
                        OR product_category_name_english LIKE 'pc__%'
                        OR product_category_name_english LIKE 'm%ic'
                        OR product_category_name_english LIKE 'tele__%'
                        OR product_category_name_english LIKE 'tab%'
                        OR product_category_name_english LIKE 'wat%'
                        OR product_category_name_english LIKE 'dvd%'
                        OR product_category_name_english LIKE 'fix%'
                THEN
                    'Apple_Tech'
                ELSE 'Others'
            END AS new_category
    FROM
        product_category_name_translation) AS category
        JOIN
    products ON category.product_category_name = products.product_category_name
        RIGHT JOIN
    order_items ON order_items.product_id = products.product_id
        JOIN
    (SELECT 
        *,
            CASE
                WHEN TIMESTAMPDIFF(HOUR, order_purchase_timestamp, order_delivered_customer_date) < 24 THEN 'overnight'
                WHEN TIMESTAMPDIFF(HOUR, order_purchase_timestamp, order_delivered_customer_date) BETWEEN 24 AND 48 THEN 'express'
                WHEN TIMESTAMPDIFF(HOUR, order_purchase_timestamp, order_delivered_customer_date) > 48 THEN 'standard'
                ELSE 'n/a'
            END AS delivery_type
    FROM
        orders) AS orders ON order_items.order_id = orders.order_id
WHERE
    new_category = 'Apple_Tech';  
    
    

-- 1) Select the relevant product categories that will be used for further analysis
SELECT 
    *
FROM
    (SELECT 
        product_category_name_english,
            CASE
                WHEN
                    product_category_name_english LIKE 'au_%'
                        OR product_category_name_english LIKE 'comp__%'
                        OR product_category_name_english LIKE 'home_com_%'
                        OR product_category_name_english LIKE 'home_conf_%'
                        OR product_category_name_english LIKE 'pc__%'
                        OR product_category_name_english LIKE 'm%ic'
                        OR product_category_name_english LIKE 'tele__%'
                        OR product_category_name_english LIKE 'tab%'
                        OR product_category_name_english LIKE 'wat%'
                        OR product_category_name_english LIKE 'dvd%'
                        OR product_category_name_english LIKE 'fix%'
                THEN
                    'Apple_Tech'
                ELSE 'Others'
            END AS new_category
    FROM
        product_category_name_translation) AS inner_table
WHERE
    new_category = 'Apple_Tech';
    
-- 2.) Select the products that matches this category
-- I also need their prouct weight as it will help me in calculating shiping cost per unit weight

SELECT * FROM products;

SELECT 
    products.product_id,
    products.product_weight_g,
    category.product_category_name_english,
    category.new_category
FROM
    (SELECT 
        *,
            CASE
                WHEN
                    product_category_name_english LIKE 'au_%'
                        OR product_category_name_english LIKE 'comp__%'
                        OR product_category_name_english LIKE 'home_com_%'
                        OR product_category_name_english LIKE 'home_conf_%'
                        OR product_category_name_english LIKE 'pc__%'
                        OR product_category_name_english LIKE 'm%ic'
                        OR product_category_name_english LIKE 'tele__%'
                        OR product_category_name_english LIKE 'tab%'
                        OR product_category_name_english LIKE 'wat%'
                        OR product_category_name_english LIKE 'dvd%'
                        OR product_category_name_english LIKE 'fix%'
                THEN
                    'Apple_Tech'
                ELSE 'Others'
            END AS new_category
    FROM
        product_category_name_translation) AS category
        JOIN
    products ON category.product_category_name = products.product_category_name
WHERE
    new_category = 'Apple_Tech';

-- cross-checking the work
SELECT 
    *
FROM
    (SELECT 
        *,
            CASE
                WHEN
                    product_category_name_english LIKE 'au_%'
                        OR product_category_name_english LIKE 'comp__%'
                        OR product_category_name_english LIKE 'home_com_%'
                        OR product_category_name_english LIKE 'home_conf_%'
                        OR product_category_name_english LIKE 'pc__%'
                        OR product_category_name_english LIKE 'm%ic'
                        OR product_category_name_english LIKE 'tele__%'
                        OR product_category_name_english LIKE 'tab%'
                        OR product_category_name_english LIKE 'wat%'
                        OR product_category_name_english LIKE 'dvd%'
                        OR product_category_name_english LIKE 'fix%'
                THEN
                    'Apple_Tech'
                ELSE 'Others'
            END AS new_category
    FROM
        product_category_name_translation) AS category
        JOIN
    products ON category.product_category_name = products.product_category_name
WHERE
    new_category = 'Apple_Tech';


-- 3) To check how much orders where made for products in this category
-- select important information that may be needed for further analysis

SELECT * FROM orders;
SELECT * FROM order_items;

 SELECT 
    order_items.product_id,
    category.product_category_name_english,
    category.new_category,
    products.product_weight_g,
    order_items.price,
    order_items.freight_value,
    order_items.shipping_limit_date
FROM
    (SELECT 
        *,
            CASE
                WHEN
                    product_category_name_english LIKE 'au_%'
                        OR product_category_name_english LIKE 'comp__%'
                        OR product_category_name_english LIKE 'home_com_%'
                        OR product_category_name_english LIKE 'home_conf_%'
                        OR product_category_name_english LIKE 'pc__%'
                        OR product_category_name_english LIKE 'm%ic'
                        OR product_category_name_english LIKE 'tele__%'
                        OR product_category_name_english LIKE 'tab%'
                        OR product_category_name_english LIKE 'wat%'
                        OR product_category_name_english LIKE 'dvd%'
                        OR product_category_name_english LIKE 'fix%'
                THEN
                    'Apple_Tech'
                ELSE 'Others'
            END AS new_category
    FROM
        product_category_name_translation) AS category
        JOIN
    products ON category.product_category_name = products.product_category_name
        RIGHT JOIN
    order_items ON order_items.product_id = products.product_id
WHERE
    new_category = 'Apple_Tech';   
    
    

#-- ----------
  


-- to categorize delivery by period from order to delivery date
 
 
 SELECT 
    orders.order_id,
    #order_items.product_id,
    category.product_category_name_english,
    category.new_category,
    products.product_weight_g,
    order_items.price,
    order_items.freight_value,
    order_payments.payment_type,
    order_payments.payment_value,
    order_payments.payment_installments,
    orders.order_purchase_timestamp,
    DATE(orders.order_purchase_timestamp) AS purchase_date,
    orders.order_delivered_carrier_date,
    orders.order_delivered_customer_date,
    DATE(orders.order_delivered_customer_date) AS delivery_date,
    order_items.shipping_limit_date,
    orders.order_status,
    orders.delivery_type,
    order_reviews.review_score,
    order_reviews.rating
FROM
    (SELECT 
        *,
            CASE
                WHEN
                    product_category_name_english LIKE 'au_%'
                        OR product_category_name_english LIKE 'comp__%'
                        OR product_category_name_english LIKE 'home_com_%'
                        OR product_category_name_english LIKE 'home_conf_%'
                        OR product_category_name_english LIKE 'pc__%'
                        OR product_category_name_english LIKE 'm%ic'
                        OR product_category_name_english LIKE 'tele__%'
                        OR product_category_name_english LIKE 'tab%'
                        OR product_category_name_english LIKE 'wat%'
                        OR product_category_name_english LIKE 'dvd%'
                        OR product_category_name_english LIKE 'fix%'
                THEN
                    'Apple_Tech'
                ELSE 'Others'
            END AS new_category
    FROM
        product_category_name_translation) AS category
        JOIN
    products ON category.product_category_name = products.product_category_name
        RIGHT JOIN
    order_items ON order_items.product_id = products.product_id
        JOIN
    (SELECT 
        *,
            CASE
                WHEN TIMESTAMPDIFF(HOUR, order_purchase_timestamp, order_delivered_customer_date) < 24 THEN 'overnight'
                WHEN TIMESTAMPDIFF(HOUR, order_purchase_timestamp, order_delivered_customer_date) BETWEEN 24 AND 48 THEN 'express'
                WHEN TIMESTAMPDIFF(HOUR, order_purchase_timestamp, order_delivered_customer_date) > 48 THEN 'standard'
                ELSE 'n/a'
            END AS delivery_type
    FROM
        orders) AS orders ON order_items.order_id = orders.order_id
        JOIN
    order_payments ON orders.order_id = order_payments.order_id
        LEFT JOIN
    (SELECT 
        *,
            CASE
                WHEN review_score = 5 THEN 'Excellent'
                WHEN review_score = 4 THEN 'Good'
                WHEN review_score = 3 THEN 'Average'
                WHEN review_score = 2 THEN 'Poor'
                WHEN review_score = 1 THEN 'Bad'
                ELSE 'n/a'
            END AS rating
    FROM
        order_reviews) AS order_reviews ON order_payments.order_id = order_reviews.order_id
WHERE
    new_category = 'Apple_Tech';  


SELECT 
    review_id,
    order_id,
    review_score,
    review_creation_date,
    review_answer_timestamp,
    CASE
        WHEN review_score = 5 THEN 'Excellent'
        WHEN review_score = 4 THEN 'Good'
        WHEN review_score = 3 THEN 'Average'
        WHEN review_score = 2 THEN 'Poor'
        WHEN review_score = 1 THEN 'Bad'
        ELSE 'n/a'
    END AS rating
FROM
    order_reviews;


 SELECT 
    orders.order_id,
    category.product_category_name_english,
    category.new_category,
    products.product_weight_g,
    order_items.price,
    order_items.freight_value,
    order_payments.payment_type,
    order_payments.payment_value,
    order_payments.payment_installments,
    orders.order_purchase_timestamp,
    DATE(orders.order_purchase_timestamp) AS purchase_date,
    orders.order_delivered_carrier_date,
    orders.order_delivered_customer_date,
    DATE(orders.order_delivered_customer_date) AS delivery_date,
    orders.order_estimated_delivery_date,
    order_items.shipping_limit_date,
    orders.order_status,
    orders.delivery_type,
    orders.delay_period,
    order_reviews.review_score,
    order_reviews.rating
FROM
    (SELECT 
        *,
            CASE
                WHEN
                    product_category_name_english LIKE 'au_%'
                        OR product_category_name_english LIKE 'comp__%'
                        OR product_category_name_english LIKE 'pc__%'
                        OR product_category_name_english LIKE 'm%ic'
                        OR product_category_name_english LIKE 'tele__%'
                        OR product_category_name_english LIKE 'tab%'
                        OR product_category_name_english LIKE 'wat%'
                        OR product_category_name_english LIKE 'dvd%'
                        OR product_category_name_english LIKE 'fix%'
                        OR product_category_name_english LIKE 'ele%'
                        OR product_category_name_english LIKE 'sec%'
                        OR product_category_name_english LIKE 'sig%'
                THEN
                    'Apple_Tech'
                ELSE 'Others'
            END AS new_category
    FROM
        product_category_name_translation) AS category
        JOIN
    products ON category.product_category_name = products.product_category_name
        RIGHT JOIN
    order_items ON order_items.product_id = products.product_id
        JOIN
    (SELECT 
        *,
            CASE
                WHEN TIMESTAMPDIFF(HOUR, order_purchase_timestamp, order_delivered_customer_date) < 24 THEN 'overnight'
                WHEN TIMESTAMPDIFF(HOUR, order_purchase_timestamp, order_delivered_customer_date) BETWEEN 24 AND 48 THEN 'express'
                WHEN TIMESTAMPDIFF(HOUR, order_purchase_timestamp, order_delivered_customer_date) > 48 THEN 'standard'
                ELSE 'n/a'
            END AS delivery_type,

            CASE
                WHEN date(order_estimated_delivery_date) < date(order_delivered_customer_date) THEN 'Delay'
                WHEN date(order_estimated_delivery_date) = date(order_delivered_customer_date) THEN 'On-time'
                WHEN date(order_estimated_delivery_date) > date(order_delivered_customer_date) THEN 'Early'
               ELSE 'n/a'
            END AS delay_period
    FROM
        orders) AS orders ON order_items.order_id = orders.order_id
        JOIN
    order_payments ON orders.order_id = order_payments.order_id
        LEFT JOIN
    (SELECT 
        *,
            CASE
                WHEN review_score = 5 THEN 'Excellent'
                WHEN review_score = 4 THEN 'Good'
                WHEN review_score = 3 THEN 'Average'
                WHEN review_score = 2 THEN 'Poor'
                WHEN review_score = 1 THEN 'Bad'
                ELSE 'n/a'
            END AS rating
    FROM
        order_reviews) AS order_reviews ON order_payments.order_id = order_reviews.order_id
where orders.delay_period = 'Delay';
