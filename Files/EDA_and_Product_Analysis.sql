

-- Basic Analysis done before EDA on raw given tables to get basic insights like
-- Rows and Columns in each tables
-- Blank / missing records
-- DATABASE EXPLORATION
-- DATA DICTIONARY
-- DIMENSION EXPLORATION
-- DATA INCONSISTENCY



---------------------  1.  DATABASE EXPLORATION      -------------------

-- EXPLORE ALL OBJECTS IN THE DATABASE
SELECT * FROM INFORMATION_SCHEMA.TABLES

--EXPLORE ALL COLUMNS IN THE DATABASE
SELECT * FROM INFORMATION_SCHEMA.COLUMNS


-- DATA DICTIONARY
SELECT 
    t.name AS TableName,
    c.name AS ColumnName,
    ty.name AS DataType,
    c.max_length AS MaxLength,
    c.is_nullable AS IsNullable
FROM sys.tables AS t
JOIN sys.columns AS c ON t.object_id = c.object_id
JOIN sys.types AS ty ON c.user_type_id = ty.user_type_id
ORDER BY t.name, c.column_id;


-- EXPLORE TOTAL NO OF ROWS IN EACH TABLE

SELECT 
    sch.name AS SchemaName,
    t.name AS TableName,
    p.rows AS Table_RowCount
FROM 
    sys.tables AS t
INNER JOIN 
    sys.schemas AS sch ON t.schema_id = sch.schema_id
INNER JOIN 
    sys.partitions AS p ON t.object_id = p.object_id
WHERE 
    p.index_id IN (0, 1) -- 0 = heap, 1 = clustered index
ORDER BY 
    p.rows DESC;




-------------------------   ITEMWISE OVERALL INFO CHECK      ---------------------



-- Order itemwise info from all tables 
-- 40025
-- simple joining of all the given tables through corresponding foreign keys and
-- first pageview information from website_pageview.
-- no new columns created

SELECT 
    -- Order Info
    o.order_id,
    o.created_at AS order_datetime,
    o.user_id,
    o.website_session_id,
    o.primary_product_id,
    o.items_purchased,
    o.price_usd AS order_total_usd,
    o.cogs_usd AS order_cogs_usd,

    -- Order Item Info
    oi.order_item_id,
    oi.created_at AS order_item_datetime,
    oi.product_id,
    oi.is_primary_item,
    oi.price_usd AS item_price_usd,
    oi.cogs_usd AS item_cogs_usd,

    -- Product Info
    p.product_name,
    p.created_at AS product_launch_date,

    -- Refund Info
    rf.order_item_refund_id,
    rf.refund_amount_usd,
    rf.created_at AS refund_datetime,

    -- Website Session Info
    ws.created_at AS session_datetime,
    ws.user_id AS session_user_id,
    ws.is_repeat_session,
    ws.utm_source,
    ws.utm_campaign,
    ws.utm_content,
    ws.device_type,
    ws.http_referer,

    -- Entry Page (first pageview in session)
    entry_pages.pageview_url AS entry_page_url,
    entry_pages.created_at AS entry_page_time

FROM orders o
JOIN order_items oi ON o.order_id = oi.order_id
LEFT JOIN order_item_refunds rf ON oi.order_item_id = rf.order_item_id
LEFT JOIN products p ON oi.product_id = p.product_id
LEFT JOIN website_sessions ws ON o.website_session_id = ws.website_session_id

-- Entry page extraction using ROW_NUMBER
LEFT JOIN (
    SELECT website_session_id, pageview_url, created_at
    FROM (
        SELECT *,
               ROW_NUMBER() OVER (PARTITION BY website_session_id ORDER BY created_at) AS rn
        FROM website_pageviews
    ) ranked
    WHERE rn = 1
) entry_pages ON ws.website_session_id = entry_pages.website_session_id






--------------------------- ALL TABLE DATA CHECK   ----------------------------

-- Simple join to check all the data from all the rows of all the tables
-- 1242108
-- simple joining of all the given tables through corresponding foreign keys
-- no new columns created


SELECT
    -- Session-level info
    ws.website_session_id,
    ws.created_at AS session_created_at,
    ws.user_id AS session_user_id,
    ws.device_type,
    ws.utm_source,
    ws.utm_campaign,
    ws.utm_content,
    ws.http_referer,

    -- Pageview-level info
    wp.website_pageview_id,
    wp.created_at AS pageview_time,
    wp.pageview_url,

    -- Order-level info
    o.order_id,
    o.created_at AS order_created_at,
    o.user_id AS order_user_id,
    o.primary_product_id,
    o.items_purchased,
    o.price_usd AS order_revenue,
    o.cogs_usd AS order_cogs,

    -- Order item-level info
    oi.order_item_id,
    oi.product_id,
    oi.is_primary_item,
    oi.price_usd AS item_price_usd,
    oi.cogs_usd AS item_cogs_usd,
    oi.created_at AS item_created_at,

    -- Product-level info
    p.product_name,
    p.created_at AS product_launch_date,

    -- Refund-level info
    r.order_item_refund_id,
    r.created_at AS refund_created_at,
    r.refund_amount_usd

FROM website_sessions ws

-- Join pageviews (many per session)
LEFT JOIN website_pageviews wp
    ON ws.website_session_id = wp.website_session_id

-- Join orders (zero or one per session)
LEFT JOIN orders o
    ON ws.website_session_id = o.website_session_id

-- Join order_items (many per order)
LEFT JOIN order_items oi
    ON o.order_id = oi.order_id

-- Join products
LEFT JOIN products p
    ON oi.product_id = p.product_id

-- Join refunds (some items may be refunded)
LEFT JOIN order_item_refunds r
    ON oi.order_item_id = r.order_item_id

-------------------------------------------------------------------------------------------------------------------




-- EDA done for some KPI Calculations
-- Product Analysis done as required


-------------------------     Basic EDA      ---------------------


-- 1. Site Traffic Breakdown

SELECT utm_source, COUNT(*) AS session_count
FROM website_sessions
GROUP BY utm_source;


-- 2. Average Web Session Volume (By Hour / Day)

SELECT DATEPART(hour, created_at) AS hour, COUNT(*) AS session_count
FROM website_sessions
GROUP BY DATEPART(hour, created_at)
ORDER BY hour;


-- 3. Seasonality Trends

SELECT FORMAT(created_at, 'yyyy-MM') AS month, COUNT(*) AS orders
FROM orders
GROUP BY FORMAT(created_at, 'yyyy-MM')
ORDER BY month;


-- 4. Sales Trends

SELECT FORMAT(created_at, 'yyyy-MM') AS month, SUM(price_usd) AS revenue
FROM orders
GROUP BY FORMAT(created_at, 'yyyy-MM')
ORDER BY month;



-- 5. Top Traffic Sources

SELECT utm_source, COUNT(*) AS sessions
FROM website_sessions
GROUP BY utm_source
ORDER BY sessions DESC;


-- 6. Product-Level Analysis

SELECT product_id, COUNT(*) AS units_sold, SUM(price_usd) AS revenue
FROM order_items
GROUP BY product_id;


-- 7. Cross-Sell Analysis
-- 7712
SELECT order_id, COUNT(DISTINCT product_id) AS unique_products
FROM order_items
GROUP BY order_id
HAVING COUNT(DISTINCT product_id) > 1
ORDER BY unique_products DESC;


-- 8. Product Refund Rate

SELECT product_id,
       SUM(CASE WHEN r.refund_amount_usd IS NOT NULL THEN 1 ELSE 0 END) * 1.0 /
       COUNT(*) AS refund_rate
FROM order_items oi
LEFT JOIN order_item_refunds r ON oi.order_item_id = r.order_item_id
GROUP BY product_id;




-------------------------   Product Analysis      ---------------------



-- 1. Analyzing Product Sales & Product Launches

--  KPI: Total Orders, Revenue, Orders Before vs After Launch

SELECT 
    p.product_id,
    p.product_name,
    p.created_at AS launch_date,
    COUNT(DISTINCT o.order_id) AS total_orders,
    SUM(oi.price_usd) AS total_revenue
    -- Orders before and after launch
    -- SUM(CASE WHEN o.created_at < p.created_at THEN 1 ELSE 0 END) AS orders_before_launch,
    -- SUM(CASE WHEN o.created_at >= p.created_at THEN 1 ELSE 0 END) AS orders_after_launch
FROM products p
JOIN order_items oi ON p.product_id = oi.product_id
JOIN orders o ON oi.order_id = o.order_id
GROUP BY p.product_id, p.product_name, p.created_at;



-- 2. Product-Level Website Pathing & Conversion Funnels

-- KPI: Sessions viewing product pages -> resulting in orders

SELECT 
    wp.pageview_url,
    COUNT(DISTINCT ws.website_session_id) AS sessions_viewing_product,
    COUNT(DISTINCT o.order_id) AS conversions_from_product_view,
    CAST(COUNT(DISTINCT o.order_id) * 100.0 / NULLIF(COUNT(DISTINCT ws.website_session_id), 0) AS DECIMAL(5,2)) AS conversion_rate_pct
FROM website_pageviews wp
JOIN website_sessions ws ON wp.website_session_id = ws.website_session_id
LEFT JOIN orders o ON ws.website_session_id = o.website_session_id
WHERE wp.pageview_url LIKE '/the%'
GROUP BY wp.pageview_url;



-- 3. Cross-Selling & Product Portfolio Analysis

-- KPI: Products frequently bought together (same order ID)


SELECT 
    oi1.product_id AS product_1,
    oi2.product_id AS product_2,
    COUNT(*) AS times_bought_together
FROM order_items oi1
JOIN order_items oi2 ON oi1.order_id = oi2.order_id AND oi1.product_id < oi2.product_id
GROUP BY oi1.product_id, oi2.product_id
ORDER BY times_bought_together DESC;



SELECT 
    p1.product_name AS product_1_name,
    p2.product_name AS product_2_name,
    COUNT(*) AS times_bought_together
FROM order_items oi1
JOIN order_items oi2 
    ON oi1.order_id = oi2.order_id 
    AND oi1.product_id < oi2.product_id
JOIN products p1 
    ON oi1.product_id = p1.product_id
JOIN products p2 
    ON oi2.product_id = p2.product_id
GROUP BY 
    p1.product_name,
    p2.product_name
ORDER BY 
    times_bought_together DESC;









-- 4. Product Refund Rates

-- KPI: Refund count, rate, and total refund amount per product


SELECT 
    p.product_id,
    p.product_name,
    COUNT(DISTINCT r.order_item_refund_id) AS refund_count,
    SUM(r.refund_amount_usd) AS total_refunded,
    COUNT(DISTINCT oi.order_item_id) AS items_sold,
    CAST(SUM(r.refund_amount_usd) * 100.0 / NULLIF(SUM(oi.price_usd), 0) AS DECIMAL(5,2)) AS refund_rate_pct
FROM products p
JOIN order_items oi ON p.product_id = oi.product_id
LEFT JOIN order_item_refunds r ON oi.order_item_id = r.order_item_id
GROUP BY p.product_id, p.product_name;



--  Website Behavior & Funnel Analysis

-- 5. Building Conversion Funnels

-- KPI: Count of sessions by key funnel steps (home ? landing ? product listing ? product ? cart ? shipping ? checkout ? thankyou)

SELECT 
    step,
    COUNT(DISTINCT website_session_id) AS sessions
FROM (
    SELECT 
        website_session_id,
        CASE 
            WHEN pageview_url = '/home' THEN 'Home'
            WHEN pageview_url IN ('/lander-1', '/lander-2', '/lander-3', '/lander-4', '/lander-5') THEN 'Landing Page'
            WHEN pageview_url IN (
                '/the-original-mr-fuzzy',
                '/the-forever-love-bear',
                '/the-birthday-sugar-panda',
                '/the-hudson-river-mini-bear'
            ) THEN 'Product Page'
            WHEN pageview_url = '/products' THEN 'Product Listing Page'
            WHEN pageview_url = '/cart' THEN 'Cart'
            WHEN pageview_url = '/shipping' THEN 'Shipping'
            WHEN pageview_url IN ('/billing', '/billing-2') THEN 'Checkout'
            WHEN pageview_url = '/thank-you-for-your-order' THEN 'Thank You (Conversion)'
        END AS step
    FROM website_pageviews
) page_steps
WHERE step IS NOT NULL
GROUP BY step
ORDER BY 
    CASE step 
        WHEN 'Home' THEN 1
        WHEN 'Landing Page' THEN 2
        WHEN 'Product Listing Page' THEN 3
        WHEN 'Product Page' THEN 4
        WHEN 'Cart' THEN 5
        WHEN 'Shipping' THEN 6
        WHEN 'Checkout' THEN 7
        WHEN 'Thank You (Conversion)' THEN 8
    END;





-- 6. Most and Least Viewed Pages

-- KPI: Pageview frequency (Top & Bottom)

SELECT 
    pageview_url,
    COUNT(*) AS view_count
FROM website_pageviews
GROUP BY pageview_url
ORDER BY view_count DESC; 





-- 7. Customer Path Before Purchase

-- KPI: Most common path leading to order

SELECT 
    session_path,
    COUNT(*) AS session_count
FROM (
    SELECT 
        wp.website_session_id,
        STRING_AGG(wp.pageview_url, ' + ') 
            WITHIN GROUP (ORDER BY wp.created_at) AS session_path
    FROM website_pageviews wp
    INNER JOIN orders o 
        ON wp.website_session_id = o.website_session_id
    WHERE wp.pageview_url IN (
        '/home',
        '/lander-1', '/lander-2', '/lander-3', '/lander-4', '/lander-5',
        '/products',
        '/cart',
        '/shipping',
        '/billing', '/billing-2',
        '/thank-you-for-your-order',
        '/the-original-mr-fuzzy',
        '/the-forever-love-bear',
        '/the-birthday-sugar-panda',
        '/the-hudson-river-mini-bear'
    )
    GROUP BY wp.website_session_id
) AS session_paths
GROUP BY session_path
ORDER BY session_count DESC;




-- 8. Pages Contributing to More Orders

-- KPI: Pageviews that are part of converted sessions

SELECT 
    wp.pageview_url,
    COUNT(DISTINCT o.order_id) AS orders_linked_to_page
FROM website_pageviews wp
JOIN orders o ON wp.website_session_id = o.website_session_id
GROUP BY wp.pageview_url
ORDER BY orders_linked_to_page DESC;



SELECT * FROM orders
WHERE items_purchased = 2




