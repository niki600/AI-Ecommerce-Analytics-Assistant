-- ============================================================
-- ECOMMERCE ANALYTICS PROJECT
-- SQL BUSINESS ANALYSIS
-- ============================================================

-- Database: ecommerce_analytics
-- Tables:
--   dashboard_orders
--   dashboard_sales


-- ============================================================
-- 1. BUSINESS OVERVIEW / KEY PERFORMANCE INDICATORS
-- ============================================================

SELECT
    COUNT(DISTINCT order_id) AS total_orders,
    COUNT(DISTINCT customer_unique_id) AS total_customers,
    ROUND(SUM(revenue), 2) AS total_revenue,
    ROUND(AVG(revenue), 2) AS avg_order_value,
    ROUND(AVG(delivery_days), 2) AS avg_delivery_days,
    ROUND(
        100.0 * SUM(CASE WHEN is_delayed THEN 1 ELSE 0 END)
        / NULLIF(COUNT(*), 0),
        2
    ) AS delay_rate_pct
FROM dashboard_orders;


-- ============================================================
-- 2. MONTHLY REVENUE PERFORMANCE
-- ============================================================

SELECT
    order_year_month,
    COUNT(DISTINCT order_id) AS orders,
    ROUND(SUM(revenue), 2) AS revenue,
    ROUND(AVG(revenue), 2) AS avg_order_value
FROM dashboard_orders
GROUP BY order_year_month
ORDER BY order_year_month;


-- ============================================================
-- 3. MONTHLY REVENUE GROWTH
-- ============================================================

WITH monthly AS (
    SELECT
        order_year_month,
        SUM(revenue) AS revenue
    FROM dashboard_orders
    GROUP BY order_year_month
)
SELECT
    order_year_month,
    ROUND(revenue, 2) AS revenue,
    ROUND(
        100.0 * (
            revenue - LAG(revenue) OVER (ORDER BY order_year_month)
        )
        / NULLIF(LAG(revenue) OVER (ORDER BY order_year_month), 0),
        2
    ) AS revenue_growth_pct
FROM monthly
ORDER BY order_year_month;


-- ============================================================
-- 4. TOP PRODUCT CATEGORIES BY REVENUE
-- ============================================================

SELECT
    product_category_name,
    COUNT(DISTINCT order_id) AS orders,
    SUM(units) AS units,
    ROUND(SUM(revenue), 2) AS revenue
FROM (
    SELECT
        product_category_name,
        order_id,
        revenue,
        1 AS units
    FROM dashboard_sales
) s
GROUP BY product_category_name
ORDER BY revenue DESC
LIMIT 10;


-- ============================================================
-- 5. TOP CATEGORIES BY REVENUE PER ORDER
-- ============================================================

SELECT
    product_category_name,
    COUNT(DISTINCT order_id) AS orders,
    ROUND(SUM(revenue), 2) AS revenue,
    ROUND(
        SUM(revenue)
        / NULLIF(COUNT(DISTINCT order_id), 0),
        2
    ) AS revenue_per_order
FROM dashboard_sales
GROUP BY product_category_name
ORDER BY revenue_per_order DESC
LIMIT 10;


-- ============================================================
-- 6. CATEGORY REVENUE SHARE
-- ============================================================

SELECT
    product_category_name,
    COUNT(DISTINCT order_id) AS orders,
    ROUND(SUM(revenue), 2) AS revenue,
    ROUND(
        100.0 * SUM(revenue)
        / NULLIF(SUM(SUM(revenue)) OVER (), 0),
        2
    ) AS revenue_share_pct
FROM dashboard_sales
GROUP BY product_category_name
ORDER BY revenue DESC
LIMIT 15;


-- ============================================================
-- 7. TOP 10 CATEGORY REVENUE CONTRIBUTION
-- ============================================================

SELECT
    ROUND(
        100.0 * SUM(revenue)
        / NULLIF(
            (SELECT SUM(revenue) FROM dashboard_sales),
            0
        ),
        2
    ) AS top_10_revenue_share_pct
FROM (
    SELECT
        product_category_name,
        SUM(revenue) AS revenue
    FROM dashboard_sales
    GROUP BY product_category_name
    ORDER BY revenue DESC
    LIMIT 10
) t;


-- ============================================================
-- 8. CUSTOMER TYPE PERFORMANCE
-- ============================================================

SELECT
    customer_type,
    COUNT(DISTINCT customer_unique_id) AS customers,
    COUNT(DISTINCT order_id) AS orders,
    ROUND(SUM(revenue), 2) AS total_revenue,
    ROUND(AVG(revenue), 2) AS avg_order_revenue,
    ROUND(
        SUM(revenue)
        / NULLIF(COUNT(DISTINCT customer_unique_id), 0),
        2
    ) AS revenue_per_customer
FROM dashboard_orders
GROUP BY customer_type
ORDER BY revenue_per_customer DESC;


-- ============================================================
-- 9. REPEAT CUSTOMER RATE
-- ============================================================

SELECT
    COUNT(DISTINCT customer_unique_id) AS total_customers,

    COUNT(DISTINCT CASE
        WHEN customer_type = 'Repeat Customer'
        THEN customer_unique_id
    END) AS repeat_customers,

    ROUND(
        100.0 *
        COUNT(DISTINCT CASE
            WHEN customer_type = 'Repeat Customer'
            THEN customer_unique_id
        END)
        / NULLIF(COUNT(DISTINCT customer_unique_id), 0),
        2
    ) AS repeat_customer_rate_pct
FROM dashboard_orders;


-- ============================================================
-- 10. CUSTOMER ORDER FREQUENCY
-- ============================================================

SELECT
    order_count,
    COUNT(*) AS customers
FROM (
    SELECT
        customer_unique_id,
        COUNT(DISTINCT order_id) AS order_count
    FROM dashboard_orders
    GROUP BY customer_unique_id
) c
GROUP BY order_count
ORDER BY order_count;


-- ============================================================
-- 11. CUSTOMER VALUE SEGMENTATION
-- ============================================================

SELECT
    customer_segment,
    COUNT(*) AS customers,
    ROUND(SUM(total_revenue), 2) AS revenue,
    ROUND(AVG(total_revenue), 2) AS avg_customer_revenue
FROM (
    SELECT
        customer_unique_id,
        SUM(revenue) AS total_revenue,
        CASE
            WHEN SUM(revenue) >= 500 THEN 'High Value'
            WHEN SUM(revenue) >= 200 THEN 'Medium Value'
            ELSE 'Low Value'
        END AS customer_segment
    FROM dashboard_orders
    GROUP BY customer_unique_id
) c
GROUP BY customer_segment
ORDER BY revenue DESC;


-- ============================================================
-- 12. STATE-WISE REVENUE PERFORMANCE
-- ============================================================

SELECT
    customer_state,
    COUNT(DISTINCT customer_unique_id) AS customers,
    COUNT(DISTINCT order_id) AS orders,
    ROUND(SUM(revenue), 2) AS total_revenue,
    ROUND(
        AVG(revenue),
        2
    ) AS avg_order_revenue,
    ROUND(
        SUM(revenue)
        / NULLIF(COUNT(DISTINCT customer_unique_id), 0),
        2
    ) AS revenue_per_customer,
    ROUND(
        100.0 * SUM(revenue)
        / NULLIF(SUM(SUM(revenue)) OVER (), 0),
        2
    ) AS revenue_share_pct
FROM dashboard_orders
GROUP BY customer_state
ORDER BY total_revenue DESC;


-- ============================================================
-- 13. TOP CUSTOMERS BY REVENUE
-- ============================================================

SELECT
    customer_unique_id,
    COUNT(DISTINCT order_id) AS orders,
    ROUND(SUM(revenue), 2) AS total_revenue,
    ROUND(AVG(revenue), 2) AS avg_order_value,
    customer_state
FROM dashboard_orders
GROUP BY customer_unique_id, customer_state
ORDER BY total_revenue DESC
LIMIT 20;


-- ============================================================
-- 14. DELIVERY PERFORMANCE
-- ============================================================

SELECT
    delivery_status,
    COUNT(DISTINCT order_id) AS orders,
    ROUND(AVG(delivery_days), 2) AS avg_delivery_days,
    ROUND(AVG(review_score), 2) AS avg_review_score,
    ROUND(
        100.0 * SUM(CASE WHEN is_delayed THEN 1 ELSE 0 END)
        / NULLIF(COUNT(DISTINCT order_id), 0),
        2
    ) AS delay_rate_pct
FROM dashboard_orders
WHERE delivery_status IS NOT NULL
GROUP BY delivery_status
ORDER BY delay_rate_pct DESC;


-- ============================================================
-- 15. STATE-WISE DELIVERY PERFORMANCE
-- ============================================================

SELECT
    customer_state,
    COUNT(DISTINCT order_id) AS orders,
    ROUND(AVG(delivery_days), 2) AS avg_delivery_days,
    SUM(CASE WHEN is_delayed THEN 1 ELSE 0 END) AS delayed_orders,
    ROUND(
        100.0 * SUM(CASE WHEN is_delayed THEN 1 ELSE 0 END)
        / NULLIF(COUNT(DISTINCT order_id), 0),
        2
    ) AS delay_rate_pct
FROM dashboard_orders
WHERE delivery_status IS NOT NULL
GROUP BY customer_state
HAVING COUNT(DISTINCT order_id) >= 500
ORDER BY delay_rate_pct DESC;


-- ============================================================
-- 16. ORDER STATUS PERFORMANCE
-- ============================================================

SELECT
    order_status,
    COUNT(DISTINCT order_id) AS orders,
    ROUND(SUM(revenue), 2) AS revenue,
    ROUND(
        100.0 * COUNT(DISTINCT order_id)
        / NULLIF(
            SUM(COUNT(DISTINCT order_id)) OVER (),
            0
        ),
        2
    ) AS order_share_pct
FROM dashboard_orders
GROUP BY order_status
ORDER BY orders DESC;


-- ============================================================
-- 17. PAYMENT METHOD PERFORMANCE
-- ============================================================

SELECT
    payment_type,
    COUNT(DISTINCT order_id) AS orders,
    ROUND(SUM(total_payment_value), 2) AS payment_value,
    ROUND(AVG(total_payment_value), 2) AS avg_payment,
    ROUND(AVG(payment_installments), 2) AS avg_installments,
    ROUND(
        100.0 * SUM(total_payment_value)
        / NULLIF(SUM(SUM(total_payment_value)) OVER (), 0),
        2
    ) AS payment_share_pct
FROM dashboard_orders
GROUP BY payment_type
ORDER BY payment_value DESC;


-- ============================================================
-- 18. PAYMENT METHOD VS CUSTOMER REVIEWS
-- ============================================================

SELECT
    payment_type,
    COUNT(DISTINCT order_id) AS orders,
    ROUND(AVG(review_score), 2) AS avg_review_score,
    ROUND(AVG(payment_installments), 2) AS avg_installments,
    ROUND(AVG(total_payment_value), 2) AS avg_payment
FROM dashboard_orders
WHERE review_score IS NOT NULL
GROUP BY payment_type
ORDER BY avg_review_score DESC;


-- ============================================================
-- 19. CATEGORY REVIEW PERFORMANCE
-- ============================================================

SELECT
    product_category_name,
    COUNT(DISTINCT order_id) AS orders,
    ROUND(SUM(revenue), 2) AS total_revenue,
    ROUND(AVG(review_score), 2) AS avg_review_score,
    ROUND(
        100.0 * SUM(
            CASE
                WHEN review_score >= 4 THEN 1
                ELSE 0
            END
        )
        / NULLIF(COUNT(review_score), 0),
        2
    ) AS positive_review_rate_pct
FROM dashboard_sales
WHERE product_category_name IS NOT NULL
GROUP BY product_category_name
HAVING COUNT(review_score) >= 100
ORDER BY total_revenue DESC
LIMIT 15;


-- ============================================================
-- 20. REVIEW SCORE DISTRIBUTION
-- ============================================================

SELECT
    review_score,
    COUNT(DISTINCT order_id) AS orders,
    ROUND(SUM(revenue), 2) AS revenue,
    ROUND(
        100.0 * COUNT(DISTINCT order_id)
        / NULLIF(
            SUM(COUNT(DISTINCT order_id)) OVER (),
            0
        ),
        2
    ) AS order_share_pct
FROM dashboard_sales
WHERE review_score IS NOT NULL
GROUP BY review_score
ORDER BY review_score;


-- ============================================================
-- 21. TOP REVENUE CATEGORIES WITH CUSTOMER SATISFACTION
-- ============================================================

SELECT
    product_category_name,
    COUNT(DISTINCT order_id) AS orders,
    ROUND(SUM(revenue), 2) AS revenue,
    ROUND(AVG(review_score), 2) AS avg_review_score
FROM dashboard_sales
WHERE product_category_name IS NOT NULL
  AND review_score IS NOT NULL
GROUP BY product_category_name
HAVING COUNT(review_score) >= 100
ORDER BY revenue DESC
LIMIT 10;


-- ============================================================
-- 22. DELIVERY IMPACT ON CUSTOMER SATISFACTION
-- ============================================================

SELECT
    delivery_status,
    COUNT(DISTINCT order_id) AS orders,
    ROUND(AVG(delivery_days), 2) AS avg_delivery_days,
    ROUND(AVG(review_score), 2) AS avg_review_score
FROM dashboard_orders
WHERE delivery_status IS NOT NULL
GROUP BY delivery_status
ORDER BY avg_review_score DESC;