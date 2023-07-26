# Enhancing Sales Strategy: Analyzing ENIAC Sales Impact of Discounts using Python

## Description:
Welcome to my project where I present an in-depth analysis of ENIAC sales data to unlock valuable insights into the impact of discounts
and product categories on quarterly and monthly revenue, as well as order patterns. Leveraging the power of Python, this project is divided
into two notebooks, each serving a specific purpose to ensure a comprehensive and data-driven approach.

### * MyFuntions Notebook: Crafting Analytical Functions
In this notebook, I've crafted custom Python functions designed to preprocess and analyze the ENIAC sales dataset. These functions categorize 
discounts into different tiers, enabling a detailed assessment of their effects on quarterly revenue, orders, and monthly trends. Additionally, 
the product categorization method efficiently groups products into ten meaningful categories based on their name, description, and type code.

### * DataAnalysis Notebook: Unveiling Insights and Visualizations
The second notebook dives into the heart of the analysis, using the functions developed in the first notebook. I thoroughly explore the relationship 
between discounts and sales performance, identifying trends that emerge during different quarters and months. By delving into the impact of product 
categories on sales, I provide valuable recommendations to optimize future sales strategies. Using data visualization libraries like Matplotlib and Seaborn, 
I present visually appealing charts and graphs to convey complex information in a clear and intuitive manner.

## Here’s a description of each table and its columns:

+ orders.csv – Every row in this file represents an order.

> + order_id – a unique identifier for each order
> + created_date – a timestamp for when the order was created
> + total_paid – the total amount paid by the customer for this order, in euros
state
> + “Shopping basket” – products have been placed in the shopping basket
> + “Place Order” – the order has been placed, but is awaiting shipment details
> + “Pending” – the order is awaiting payment confirmation
> + “Completed” – the order has been placed and paid, and the transaction is completed.
> + “Cancelled” – the order has been cancelled and the payment returned to the customer.


+ orderlines.csv – Every row represents each one of the different products involved in an order.


> + id – a unique identifier for each row in this file
> + id_order – corresponds to orders.order_id
> + product_id – an old identifier for each product, nowadays not in use
> + product_quantity – how many units of that product were purchased on that order
> + sku – stock keeping unit: a unique identifier for each product
> + unit_price – the unitary price (in euros) of each product at the moment of placing that order
> + date – timestamp for the processing of that product

+ products.csv


> + sku – stock keeping unit: a unique identifier for each product
name – product name
> + desc – product description
> + in_stock – whether or not the product was in stock at the moment of the data extraction
> + type – a numerical code for product type
> + promo_price – promotional price, in euros

+ brands.csv


> + short – the 3-character code by which the brand can be identified in the first 3 characters of products.sku
> + long – brand name
