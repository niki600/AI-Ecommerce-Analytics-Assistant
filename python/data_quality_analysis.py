import pandas as pd
from pathlib import Path


# --------------------------------------------------
# 1. DATA FOLDER PATH
# --------------------------------------------------

DATA_DIR = Path(__file__).resolve().parent.parent / "data"


# --------------------------------------------------
# 2. LOAD DATA
# --------------------------------------------------

orders = pd.read_csv(DATA_DIR / "olist_orders_dataset.csv")
products = pd.read_csv(DATA_DIR / "olist_products_dataset.csv")
geolocation = pd.read_csv(DATA_DIR / "olist_geolocation_dataset.csv")
reviews = pd.read_csv(DATA_DIR / "olist_order_reviews_dataset.csv")


# --------------------------------------------------
# 3. ORDERS - MISSING DATE ANALYSIS
# --------------------------------------------------

print("=" * 60)
print("ORDERS - MISSING DATE ANALYSIS")
print("=" * 60)

date_columns = [
    "order_approved_at",
    "order_delivered_carrier_date",
    "order_delivered_customer_date"
]

for column in date_columns:

    missing = orders[orders[column].isna()]

    print(f"\n{column}")
    print(f"Missing records: {len(missing)}")

    if len(missing) > 0:
        print("Order status distribution:")
        print(missing["order_status"].value_counts())


# --------------------------------------------------
# 4. PRODUCTS - MISSING VALUE ANALYSIS
# --------------------------------------------------

print("\n" + "=" * 60)
print("PRODUCTS - MISSING VALUE ANALYSIS")
print("=" * 60)

product_missing = products[
    products["product_category_name"].isna()
]

print("\nProducts with missing category:")
print(len(product_missing))

print("\nMissing values in those products:")
print(product_missing.isna().sum())


# --------------------------------------------------
# 5. GEOLOCATION - DUPLICATE ANALYSIS
# --------------------------------------------------

print("\n" + "=" * 60)
print("GEOLOCATION - DUPLICATE ANALYSIS")
print("=" * 60)

duplicate_rows = geolocation[
    geolocation.duplicated(keep=False)
]

print(f"\nTotal duplicate rows: {len(duplicate_rows)}")

print("\nSample duplicate records:")
print(duplicate_rows.head(10))


# --------------------------------------------------
# 6. REVIEWS - MISSING COMMENT ANALYSIS
# --------------------------------------------------

print("\n" + "=" * 60)
print("REVIEWS - MISSING COMMENT ANALYSIS")
print("=" * 60)

missing_title = reviews[
    "review_comment_title"
].isna().sum()

missing_message = reviews[
    "review_comment_message"
].isna().sum()

print(f"\nMissing review titles   : {missing_title}")
print(f"Missing review messages : {missing_message}")

print("\nReview score distribution:")
print(
    reviews["review_score"]
    .value_counts()
    .sort_index()
)


# --------------------------------------------------
# 7. COMPLETION
# --------------------------------------------------

print("\n" + "=" * 60)
print("DATA QUALITY ANALYSIS COMPLETED")
print("=" * 60)