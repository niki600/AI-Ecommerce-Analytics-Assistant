import pandas as pd
from pathlib import Path


# --------------------------------------------------
# 1. PATHS
# --------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent.parent

PROCESSED_DIR = BASE_DIR / "data" / "processed"


# --------------------------------------------------
# 2. LOAD ANALYTICAL DATA
# --------------------------------------------------

sales = pd.read_csv(
    PROCESSED_DIR / "sales_analytics.csv"
)

print("=" * 60)
print("PRODUCT & CATEGORY ANALYSIS")
print("=" * 60)

print("\nSales rows:", len(sales))


# --------------------------------------------------
# 3. PRODUCT ANALYSIS
# --------------------------------------------------

print("\n" + "=" * 60)
print("PRODUCT PERFORMANCE")
print("=" * 60)

product_analysis = (
    sales.groupby("product_id")
    .agg(
        revenue=("sales_amount", "sum"),
        units=("order_item_id", "count"),
        orders=("order_id", "nunique")
    )
    .reset_index()
)


# Product AOV
product_analysis["AOV"] = (
    product_analysis["revenue"]
    / product_analysis["orders"]
)


# --------------------------------------------------
# 4. TOP PRODUCTS BY REVENUE
# --------------------------------------------------

print("\nTop 15 Products by Revenue:")

top_products = (
    product_analysis
    .sort_values("revenue", ascending=False)
    .head(15)
)

print(top_products.to_string(index=False))


# --------------------------------------------------
# 5. TOP PRODUCTS BY UNITS
# --------------------------------------------------

print("\n" + "=" * 60)
print("TOP PRODUCTS BY UNITS")
print("=" * 60)

top_products_units = (
    product_analysis
    .sort_values("units", ascending=False)
    .head(15)
)

print(top_products_units.to_string(index=False))


# --------------------------------------------------
# 6. CATEGORY ANALYSIS
# --------------------------------------------------

print("\n" + "=" * 60)
print("CATEGORY PERFORMANCE")
print("=" * 60)

category_analysis = (
    sales.groupby("product_category_name")
    .agg(
        revenue=("sales_amount", "sum"),
        units=("order_item_id", "count"),
        orders=("order_id", "nunique"),
        products=("product_id", "nunique")
    )
    .reset_index()
)


# Category AOV
category_analysis["AOV"] = (
    category_analysis["revenue"]
    / category_analysis["orders"]
)


# --------------------------------------------------
# 7. REVENUE SHARE
# --------------------------------------------------

total_category_revenue = (
    category_analysis["revenue"].sum()
)

category_analysis["revenue_share_pct"] = (
    category_analysis["revenue"]
    / total_category_revenue
    * 100
)


# --------------------------------------------------
# 8. TOP CATEGORIES BY REVENUE
# --------------------------------------------------

print("\nTop 15 Categories by Revenue:")

top_categories = (
    category_analysis
    .sort_values("revenue", ascending=False)
    .head(15)
)

print(top_categories.to_string(index=False))


# --------------------------------------------------
# 9. TOP CATEGORIES BY UNITS
# --------------------------------------------------

print("\n" + "=" * 60)
print("TOP CATEGORIES BY UNITS")
print("=" * 60)

top_categories_units = (
    category_analysis
    .sort_values("units", ascending=False)
    .head(15)
)

print(top_categories_units.to_string(index=False))


# --------------------------------------------------
# 10. HIGH VOLUME / LOW REVENUE CATEGORIES
# --------------------------------------------------

print("\n" + "=" * 60)
print("HIGH VOLUME / LOW REVENUE CATEGORIES")
print("=" * 60)

volume_median = category_analysis["units"].median()
revenue_median = category_analysis["revenue"].median()

high_volume_low_revenue = category_analysis[
    (category_analysis["units"] > volume_median)
    &
    (category_analysis["revenue"] < revenue_median)
].sort_values(
    "units",
    ascending=False
)

print(
    high_volume_low_revenue.head(15)
    .to_string(index=False)
)


# --------------------------------------------------
# 11. HIGH REVENUE / LOW VOLUME CATEGORIES
# --------------------------------------------------

print("\n" + "=" * 60)
print("HIGH REVENUE / LOW VOLUME CATEGORIES")
print("=" * 60)

high_revenue_low_volume = category_analysis[
    (category_analysis["revenue"] > revenue_median)
    &
    (category_analysis["units"] < volume_median)
].sort_values(
    "revenue",
    ascending=False
)

print(
    high_revenue_low_volume.head(15)
    .to_string(index=False)
)


# --------------------------------------------------
# 12. SAVE RESULTS
# --------------------------------------------------

product_analysis.to_csv(
    PROCESSED_DIR / "product_performance_analysis.csv",
    index=False
)

category_analysis.to_csv(
    PROCESSED_DIR / "category_performance_analysis.csv",
    index=False
)

top_products.to_csv(
    PROCESSED_DIR / "top_products_by_revenue.csv",
    index=False
)

top_categories.to_csv(
    PROCESSED_DIR / "top_categories_by_revenue.csv",
    index=False
)


# --------------------------------------------------
# 13. FINAL SUMMARY
# --------------------------------------------------

print("\n" + "=" * 60)
print("PRODUCT & CATEGORY ANALYSIS COMPLETED ✅")
print("=" * 60)

print("\nFiles saved:")
print("- product_performance_analysis.csv")
print("- category_performance_analysis.csv")
print("- top_products_by_revenue.csv")
print("- top_categories_by_revenue.csv")