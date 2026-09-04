import pandas as pd
from pathlib import Path


# --------------------------------------------------
# 1. FOLDERS
# --------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
PROCESSED_DIR = DATA_DIR / "processed"

PROCESSED_DIR.mkdir(exist_ok=True)


# --------------------------------------------------
# 2. LOAD DATA
# --------------------------------------------------

orders = pd.read_csv(
    DATA_DIR / "olist_orders_dataset.csv"
)

products = pd.read_csv(
    DATA_DIR / "olist_products_dataset.csv"
)

reviews = pd.read_csv(
    DATA_DIR / "olist_order_reviews_dataset.csv"
)

geolocation = pd.read_csv(
    DATA_DIR / "olist_geolocation_dataset.csv"
)
customers = pd.read_csv(
    DATA_DIR / "olist_customers_dataset.csv"
)

print("=" * 60)
print("E-COMMERCE DATA CLEANING")
print("=" * 60)


# --------------------------------------------------
# 3. CONVERT DATE COLUMNS
# --------------------------------------------------

print("\nConverting date columns...")

order_date_columns = [
    "order_purchase_timestamp",
    "order_approved_at",
    "order_delivered_carrier_date",
    "order_delivered_customer_date",
    "order_estimated_delivery_date"
]

for column in order_date_columns:
    orders[column] = pd.to_datetime(
        orders[column],
        errors="coerce"
    )

print("Order date conversion completed ✅")


# --------------------------------------------------
# 4. PRODUCT DATA CLEANING
# --------------------------------------------------

print("\nCleaning product data...")

# Missing category ko Unknown mark karenge
products["product_category_name"] = (
    products["product_category_name"]
    .fillna("unknown")
)

print("Missing product categories handled ✅")


# --------------------------------------------------
# 5. REVIEW DATA CLEANING
# --------------------------------------------------

print("\nCleaning review data...")

# Comments missing hona valid hai.
# Isliye unhe blank string se represent karenge.

reviews["review_comment_title"] = (
    reviews["review_comment_title"]
    .fillna("")
)

reviews["review_comment_message"] = (
    reviews["review_comment_message"]
    .fillna("")
)

print("Missing review comments handled ✅")


# --------------------------------------------------
# 6. GEOLOCATION CLEANING
# --------------------------------------------------

print("\nCleaning geolocation data...")

# Exact duplicate rows remove karenge.
geolocation = geolocation.drop_duplicates()

print(
    f"Geolocation rows after removing exact duplicates: "
    f"{len(geolocation):,}"
)


# --------------------------------------------------
# 7. REMOVE EXACT DUPLICATES
# --------------------------------------------------

print("\nChecking exact duplicates...")

orders_before = len(orders)
products_before = len(products)
reviews_before = len(reviews)

orders = orders.drop_duplicates()
products = products.drop_duplicates()
reviews = reviews.drop_duplicates()

print(
    f"Orders duplicates removed: "
    f"{orders_before - len(orders)}"
)

print(
    f"Products duplicates removed: "
    f"{products_before - len(products)}"
)

print(
    f"Reviews duplicates removed: "
    f"{reviews_before - len(reviews)}"
)


# --------------------------------------------------
# 8. SAVE CLEANED DATA
# --------------------------------------------------

print("\nSaving cleaned datasets...")

orders.to_csv(
    PROCESSED_DIR / "orders_cleaned.csv",
    index=False
)

products.to_csv(
    PROCESSED_DIR / "products_cleaned.csv",
    index=False
)

reviews.to_csv(
    PROCESSED_DIR / "reviews_cleaned.csv",
    index=False
)

geolocation.to_csv(
    PROCESSED_DIR / "geolocation_cleaned.csv",
    index=False
)

customers.to_csv(
    PROCESSED_DIR / "customers_cleaned.csv",
    index=False
)

# --------------------------------------------------
# 9. FINAL SUMMARY
# --------------------------------------------------

print("\n" + "=" * 60)
print("CLEANING SUMMARY")
print("=" * 60)

print(f"Orders cleaned       : {len(orders):,}")
print(f"Products cleaned     : {len(products):,}")
print(f"Reviews cleaned      : {len(reviews):,}")
print(f"Geolocation cleaned  : {len(geolocation):,}")
print(f"Customers cleaned    : {len(customers):,}")

print("\nCleaned files saved in:")
print(PROCESSED_DIR)

print("\nDATA CLEANING COMPLETED ✅")
print("=" * 60)