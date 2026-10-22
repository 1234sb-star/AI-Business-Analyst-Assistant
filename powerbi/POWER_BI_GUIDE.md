# Power BI Extension

## Dashboard pages

### Page 1 — Executive Overview
Cards:
- Total Revenue
- Total Orders
- Units Sold
- Average Order Value
- Return Rate

Charts:
- Monthly Revenue
- Revenue by Category
- Revenue by Region
- Order Status

### Page 2 — Customer & Product Analysis
- Top 10 customers by revenue
- Top 10 products by revenue
- Revenue by customer segment
- Average order value by segment

### Page 3 — March Revenue Drop
- Monthly revenue
- February vs March revenue
- Electronics revenue trend
- Revenue by customer
- Region contribution
- Order status

## Connect the CSV
1. Open Power BI Desktop.
2. Get Data → Text/CSV.
3. Select `data/sales_data.csv`.
4. Build the visuals above.
5. Add slicers for Date, Category, Region and Customer Segment.

## DAX measures

```DAX
Total Revenue = SUM(sales_data[revenue])

Total Orders = DISTINCTCOUNT(sales_data[order_id])

Units Sold = SUM(sales_data[quantity])

Average Order Value =
DIVIDE([Total Revenue], [Total Orders])

Returned Orders =
CALCULATE(
    [Total Orders],
    sales_data[order_status] = "Returned"
)

Return Rate =
DIVIDE([Returned Orders], [Total Orders])
```
