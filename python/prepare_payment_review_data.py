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
    PROCESSED_DIR / "sales_features.csv"
)

payments = pd.read_csv(
    DATA_DIR / "olist_order_payments_dataset.csv"
)

reviews = pd.read_csv(
    PROCESSED_DIR / "reviews_cleaned.csv"
)


print("=" * 60)
print("PAYMENT & REVIEW DATA INTEGRATION")
print("=" * 60)

print("\nSales rows:", len(sales))
print("Payments rows:", len(payments))
print("Reviews rows:", len(reviews))


# --------------------------------------------------
# 3. PAYMENT ANALYSIS
# --------------------------------------------------

print("\n" + "=" * 60)
print("PAYMENT DATA ANALYSIS")
print("=" * 60)

print("\nPayment types:")
print(payments["payment_type"].value_counts())

print("\nPayment value summary:")
print(payments["payment_value"].describe())


# --------------------------------------------------
# 4. AGGREGATE PAYMENTS AT ORDER LEVEL
# --------------------------------------------------

print("\nAggregating payments by order...")

payment_summary = (
    payments
    .groupby("order_id")
    .agg(
        total_payment_value=("payment_value", "sum"),
        payment_installments=("payment_installments", "max"),
        payment_type=("payment_type", "first")
    )
    .reset_index()
)

print("Unique orders in payment data:", len(payment_summary))

print("Payment aggregation completed ✅")


# --------------------------------------------------
# 5. JOIN SALES + PAYMENTS
# --------------------------------------------------

print("\nJoining Sales with Payments...")

sales = sales.merge(
    payment_summary,
    on="order_id",
    how="left"
)

print("Payment join completed ✅")
print("Rows after payment join:", len(sales))


# --------------------------------------------------
# 6. PAYMENT MATCHING CHECK
# --------------------------------------------------

missing_payment_match = (
    sales["payment_type"].isna().sum()
)

print(
    "Rows with missing payment match:",
    missing_payment_match
)


# --------------------------------------------------
# 7. REVIEW DATA PREPARATION
# --------------------------------------------------

print("\nPreparing review data...")

review_summary = (
    reviews
    .groupby("order_id")
    .agg(
        review_score=("review_score", "mean"),
        review_count=("review_id", "nunique")
    )
    .reset_index()
)

print(
    "Unique orders with reviews:",
    len(review_summary)
)

print("Review aggregation completed ✅")


# --------------------------------------------------
# 8. JOIN SALES + REVIEWS
# --------------------------------------------------

print("\nJoining Sales with Reviews...")

sales = sales.merge(
    review_summary,
    on="order_id",
    how="left"
)

print("Review join completed ✅")
print("Rows after review join:", len(sales))


# --------------------------------------------------
# 9. REVIEW MATCHING CHECK
# --------------------------------------------------

missing_review_match = (
    sales["review_score"].isna().sum()
)

print(
    "Rows with missing review:",
    missing_review_match
)


# --------------------------------------------------
# 10. CREATE PAYMENT / REVIEW FEATURES
# --------------------------------------------------

print("\nCreating payment and review features...")

sales["payment_gap"] = (
    sales["total_payment_value"]
    - sales["total_item_value"]
)

sales["has_review"] = (
    sales["review_score"]
    .notna()
    .astype(int)
)

sales["is_positive_review"] = (
    sales["review_score"]
    >= 4
).astype(int)

print("Payment and review features created ✅")


# --------------------------------------------------
# 11. FINAL DATASET CHECK
# --------------------------------------------------

print("\n" + "=" * 60)
print("FINAL ANALYTICAL DATASET")
print("=" * 60)

print("\nRows:", len(sales))
print("Columns:", len(sales.columns))

print("\nNew columns:")

new_columns = [
    "total_payment_value",
    "payment_installments",
    "payment_type",
    "review_score",
    "review_count",
    "payment_gap",
    "has_review",
    "is_positive_review"
]

for column in new_columns:
    print("-", column)


# --------------------------------------------------
# 12. CHECK DUPLICATION
# --------------------------------------------------

print("\nChecking order duplication...")

unique_orders = sales["order_id"].nunique()

print("Unique orders:", unique_orders)
print("Sales rows:", len(sales))

print(
    "Rows per order:",
    round(len(sales) / unique_orders, 2)
)


# --------------------------------------------------
# 13. SAVE FINAL ANALYTICAL DATA
# --------------------------------------------------

output_file = (
    PROCESSED_DIR /
    "sales_analytics.csv"
)

sales.to_csv(
    output_file,
    index=False
)

print("\nSaved:")
print(output_file)


print("\n" + "=" * 60)
print("PAYMENT & REVIEW INTEGRATION COMPLETED ✅")
print("=" * 60)