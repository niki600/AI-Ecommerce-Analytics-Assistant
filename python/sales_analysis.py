import pandas as pd
from pathlib import Path


# --------------------------------------------------
# 1. PATHS
# --------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent.parent

DATA_DIR = BASE_DIR / "data"
PROCESSED_DIR = DATA_DIR / "processed"


# --------------------------------------------------
# 2. LOAD ANALYTICAL DATA
# --------------------------------------------------

sales = pd.read_csv(
    PROCESSED_DIR / "sales_analytics.csv"
)

print("=" * 60)
print("E-COMMERCE SALES ANALYSIS")
print("=" * 60)

print("\nSales rows:", len(sales))


# --------------------------------------------------
# 3. CONVERT DATE
# --------------------------------------------------

sales["order_purchase_timestamp"] = pd.to_datetime(
    sales["order_purchase_timestamp"],
    errors="coerce"
)


# --------------------------------------------------
# 4. BASIC SALES KPIs
# --------------------------------------------------

total_revenue = sales["sales_amount"].sum()

total_freight = sales["freight_cost"].sum()

total_units = sales["order_item_id"].count()

total_orders = sales["order_id"].nunique()

total_customers = sales["customer_unique_id"].nunique()

average_order_value = (
    total_revenue / total_orders
)


print("\n" + "=" * 60)
print("KEY SALES KPIs")
print("=" * 60)

print(f"\nTotal Revenue       : {total_revenue:,.2f}")
print(f"Total Freight Cost  : {total_freight:,.2f}")
print(f"Total Units Sold    : {total_units:,}")
print(f"Total Orders        : {total_orders:,}")
print(f"Total Customers     : {total_customers:,}")
print(f"Average Order Value : {average_order_value:,.2f}")


# --------------------------------------------------
# 5. REVENUE BY ORDER STATUS
# --------------------------------------------------

print("\n" + "=" * 60)
print("REVENUE BY ORDER STATUS")
print("=" * 60)

status_revenue = (
    sales
    .groupby("order_status")
    .agg(
        revenue=("sales_amount", "sum"),
        orders=("order_id", "nunique"),
        units=("order_item_id", "count")
    )
    .sort_values(
        "revenue",
        ascending=False
    )
)

print(status_revenue)


# --------------------------------------------------
# 6. MONTHLY SALES
# --------------------------------------------------

print("\n" + "=" * 60)
print("MONTHLY SALES")
print("=" * 60)

monthly_sales = (
    sales
    .groupby("order_year_month")
    .agg(
        revenue=("sales_amount", "sum"),
        orders=("order_id", "nunique"),
        units=("order_item_id", "count")
    )
    .reset_index()
)

monthly_sales["AOV"] = (
    monthly_sales["revenue"]
    / monthly_sales["orders"]
)

print(monthly_sales)


# --------------------------------------------------
# 7. MONTH-OVER-MONTH GROWTH
# --------------------------------------------------

monthly_sales["previous_month_revenue"] = (
    monthly_sales["revenue"].shift(1)
)

monthly_sales["mom_growth_pct"] = (
    (
        monthly_sales["revenue"]
        - monthly_sales["previous_month_revenue"]
    )
    / monthly_sales["previous_month_revenue"]
) * 100

print("\n" + "=" * 60)
print("MONTH-OVER-MONTH GROWTH")
print("=" * 60)

print(
    monthly_sales[
        [
            "order_year_month",
            "revenue",
            "mom_growth_pct"
        ]
    ]
)


# --------------------------------------------------
# 8. CATEGORY PERFORMANCE
# --------------------------------------------------

print("\n" + "=" * 60)
print("CATEGORY PERFORMANCE")
print("=" * 60)

category_sales = (
    sales
    .groupby("product_category_name")
    .agg(
        revenue=("sales_amount", "sum"),
        units=("order_item_id", "count"),
        orders=("order_id", "nunique")
    )
    .sort_values(
        "revenue",
        ascending=False
    )
)

category_sales["revenue_share_pct"] = (
    category_sales["revenue"]
    / total_revenue
) * 100

print("\nTop 15 Categories:")

print(
    category_sales
    .head(15)
)


# --------------------------------------------------
# 9. TOP PRODUCTS
# --------------------------------------------------

print("\n" + "=" * 60)
print("TOP PRODUCTS")
print("=" * 60)

product_sales = (
    sales
    .groupby("product_id")
    .agg(
        revenue=("sales_amount", "sum"),
        units=("order_item_id", "count"),
        orders=("order_id", "nunique")
    )
    .sort_values(
        "revenue",
        ascending=False
    )
)

print("\nTop 15 Products:")

print(
    product_sales.head(15)
)


# --------------------------------------------------
# 10. REGIONAL PERFORMANCE
# --------------------------------------------------

print("\n" + "=" * 60)
print("REGIONAL PERFORMANCE")
print("=" * 60)

regional_sales = (
    sales
    .groupby("customer_state")
    .agg(
        revenue=("sales_amount", "sum"),
        orders=("order_id", "nunique"),
        customers=("customer_unique_id", "nunique")
    )
    .sort_values(
        "revenue",
        ascending=False
    )
)

regional_sales["AOV"] = (
    regional_sales["revenue"]
    / regional_sales["orders"]
)

print("\nTop 15 States:")

print(
    regional_sales.head(15)
)


# --------------------------------------------------
# 11. SAVE ANALYTICS OUTPUTS
# --------------------------------------------------

print("\n" + "=" * 60)
print("SAVING ANALYTICS RESULTS")
print("=" * 60)


monthly_sales.to_csv(
    PROCESSED_DIR / "monthly_sales_analysis.csv",
    index=False
)

category_sales.to_csv(
    PROCESSED_DIR / "category_sales_analysis.csv"
)

product_sales.to_csv(
    PROCESSED_DIR / "product_sales_analysis.csv"
)

regional_sales.to_csv(
    PROCESSED_DIR / "regional_sales_analysis.csv"
)

status_revenue.to_csv(
    PROCESSED_DIR / "order_status_analysis.csv"
)


print("\nAnalytics files saved ✅")

print(
    "- monthly_sales_analysis.csv"
)

print(
    "- category_sales_analysis.csv"
)

print(
    "- product_sales_analysis.csv"
)

print(
    "- regional_sales_analysis.csv"
)

print(
    "- order_status_analysis.csv"
)


print("\n" + "=" * 60)
print("SALES ANALYSIS COMPLETED ✅")
print("=" * 60)