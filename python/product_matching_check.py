import pandas as pd
from pathlib import Path


# --------------------------------------------------
# 1. PATHS
# --------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent.parent

DATA_DIR = BASE_DIR / "data"
PROCESSED_DIR = DATA_DIR / "processed"


# --------------------------------------------------
# 2. LOAD DATA
# --------------------------------------------------

sales = pd.read_csv(
    PROCESSED_DIR / "sales_base.csv"
)

products = pd.read_csv(
    PROCESSED_DIR / "products_cleaned.csv"
)


print("=" * 60)
print("PRODUCT MATCHING VALIDATION")
print("=" * 60)


# --------------------------------------------------
# 3. UNIQUE PRODUCT IDs
# --------------------------------------------------

sales_products = set(
    sales["product_id"].dropna().unique()
)

master_products = set(
    products["product_id"].dropna().unique()
)


print("\nUnique product IDs in sales:",
      len(sales_products))

print("Unique product IDs in products:",
      len(master_products))


# --------------------------------------------------
# 4. FIND UNMATCHED PRODUCT IDs
# --------------------------------------------------

unmatched_products = sales_products - master_products

print("\nUnmatched product IDs:",
      len(unmatched_products))


# --------------------------------------------------
# 5. FIND UNMATCHED SALES ROWS
# --------------------------------------------------

unmatched_sales = sales[
    sales["product_id"].isin(unmatched_products)
].copy()


print("\nUnmatched sales rows:",
      len(unmatched_sales))


# --------------------------------------------------
# 6. ORDER STATUS OF UNMATCHED ROWS
# --------------------------------------------------

print("\n" + "=" * 60)
print("ORDER STATUS OF UNMATCHED PRODUCTS")
print("=" * 60)

print(
    unmatched_sales["order_status"]
    .value_counts()
)


# --------------------------------------------------
# 7. TOP UNMATCHED PRODUCT IDs
# --------------------------------------------------

print("\n" + "=" * 60)
print("TOP UNMATCHED PRODUCT IDs")
print("=" * 60)

print(
    unmatched_sales["product_id"]
    .value_counts()
    .head(20)
)


# --------------------------------------------------
# 8. SAMPLE UNMATCHED RECORDS
# --------------------------------------------------

print("\n" + "=" * 60)
print("SAMPLE UNMATCHED SALES RECORDS")
print("=" * 60)

columns_to_show = [
    "order_id",
    "customer_id",
    "order_status",
    "order_purchase_timestamp",
    "product_id",
    "price",
    "freight_value"
]

print(
    unmatched_sales[
        columns_to_show
    ].head(20).to_string(index=False)
)


# --------------------------------------------------
# 9. TOTAL SALES VALUE OF UNMATCHED ROWS
# --------------------------------------------------

unmatched_sales_value = (
    unmatched_sales["price"].sum()
)

print("\nTotal price of unmatched sales rows:",
      round(unmatched_sales_value, 2))


# --------------------------------------------------
# 10. FINAL SUMMARY
# --------------------------------------------------

print("\n" + "=" * 60)
print("PRODUCT MATCHING VALIDATION COMPLETED")
print("=" * 60)