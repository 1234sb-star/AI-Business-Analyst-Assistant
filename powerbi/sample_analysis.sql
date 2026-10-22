-- Monthly revenue
SELECT
    strftime('%Y-%m', order_date) AS month,
    ROUND(SUM(revenue), 2) AS revenue,
    COUNT(DISTINCT order_id) AS orders,
    ROUND(SUM(revenue) / COUNT(DISTINCT order_id), 2) AS average_order_value
FROM sales
GROUP BY month
ORDER BY month;

-- Revenue by category
SELECT
    category,
    ROUND(SUM(revenue), 2) AS revenue
FROM sales
GROUP BY category
ORDER BY revenue DESC;

-- March category comparison
SELECT
    category,
    ROUND(SUM(CASE WHEN strftime('%Y-%m', order_date) = '2026-02' THEN revenue ELSE 0 END), 2) AS feb_revenue,
    ROUND(SUM(CASE WHEN strftime('%Y-%m', order_date) = '2026-03' THEN revenue ELSE 0 END), 2) AS mar_revenue
FROM sales
GROUP BY category
ORDER BY mar_revenue DESC;

-- Top customers
SELECT
    customer_id,
    ROUND(SUM(revenue), 2) AS revenue,
    COUNT(DISTINCT order_id) AS orders
FROM sales
GROUP BY customer_id
ORDER BY revenue DESC
LIMIT 10;

-- Return rate by region
SELECT
    region,
    COUNT(DISTINCT order_id) AS total_orders,
    COUNT(DISTINCT CASE WHEN order_status = 'Returned' THEN order_id END) AS returned_orders,
    ROUND(
        100.0 * COUNT(DISTINCT CASE WHEN order_status = 'Returned' THEN order_id END)
        / COUNT(DISTINCT order_id),
        2
    ) AS return_rate_pct
FROM sales
GROUP BY region
ORDER BY return_rate_pct DESC;
