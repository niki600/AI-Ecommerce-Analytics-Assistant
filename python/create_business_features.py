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
    PROCESSED_DIR / "sales_base.csv"
)

print("=" * 60)
print("BUSINESS FEATURE CREATION")
print("=" * 60)

print("\nSales rows:", len(sales))


# --------------------------------------------------
# 3. CONVERT DATE COLUMNS
# --------------------------------------------------

print("\nConverting date columns...")

date_columns = [
    "order_purchase_timestamp",
    "order_approved_at",
    "order_delivered_carrier_date",
    "order_delivered_customer_date",
    "order_estimated_delivery_date",
    "shipping_limit_date"
]

for column in date_columns:
    sales[column] = pd.to_datetime(
        sales[column],
        errors="coerce"
    )

print("Date conversion completed ✅")


# --------------------------------------------------
# 4. SALES & REVENUE FEATURES
# --------------------------------------------------

print("\nCreating sales features...")

sales["sales_amount"] = sales["price"]

sales["freight_cost"] = sales["freight_value"]

sales["total_item_value"] = (
    sales["price"] + sales["freight_value"]
)

print("Sales features created ✅")


# --------------------------------------------------
# 5. DATE FEATURES
# --------------------------------------------------

print("\nCreating date features...")

sales["order_year"] = (
    sales["order_purchase_timestamp"].dt.year
)

sales["order_month"] = (
    sales["order_purchase_timestamp"].dt.month
)

sales["order_month_name"] = (
    sales["order_purchase_timestamp"].dt.month_name()
)

sales["order_year_month"] = (
    sales["order_purchase_timestamp"]
    .dt.to_period("M")
    .astype(str)
)

print("Date features created ✅")


# --------------------------------------------------
# 6. DELIVERY FEATURES
# --------------------------------------------------

print("\nCreating delivery features...")

sales["delivery_days"] = (
    sales["order_delivered_customer_date"]
    - sales["order_purchase_timestamp"]
).dt.total_seconds() / (24 * 60 * 60)


sales["estimated_delivery_days"] = (
    sales["order_estimated_delivery_date"]
    - sales["order_purchase_timestamp"]
).dt.total_seconds() / (24 * 60 * 60)


sales["delivery_delay_days"] = (
    sales["order_delivered_customer_date"]
    - sales["order_estimated_delivery_date"]
).dt.total_seconds() / (24 * 60 * 60)


# --------------------------------------------------
# 7. DELAY FLAG
# --------------------------------------------------

sales["is_delayed"] = (
    sales["delivery_delay_days"] > 0
).astype(int)

print("Delivery features created ✅")


# --------------------------------------------------
# 8. BASIC FEATURE CHECK
# --------------------------------------------------

print("\n" + "=" * 60)
print("FEATURE CHECK")
print("=" * 60)

feature_columns = [
    "sales_amount",
    "freight_cost",
    "total_item_value",
    "order_year",
    "order_month",
    "order_month_name",
    "order_year_month",
    "delivery_days",
    "estimated_delivery_days",
    "delivery_delay_days",
    "is_delayed"
]

print("\nCreated features:")

for column in feature_columns:
    print(f"- {column}")


# --------------------------------------------------
# 9. DELAY SUMMARY
# --------------------------------------------------

print("\n" + "=" * 60)
print("DELIVERY SUMMARY")
print("=" * 60)

print(
    "\nOrders with delivery date:",
    sales["delivery_days"].notna().sum()
)

print(
    "Delayed records:",
    sales["is_delayed"].sum()
)

print(
    "On-time / early records:",
    (
        (sales["delivery_delay_days"] <= 0)
        & sales["delivery_delay_days"].notna()
    ).sum()
)


# --------------------------------------------------
# 10. SAVE FEATURE DATASET
# --------------------------------------------------

output_file = (
    PROCESSED_DIR / "sales_features.csv"
)

sales.to_csv(
    output_file,
    index=False
)

print("\nSaved:")
print(output_file)


print("\n" + "=" * 60)
print("BUSINESS FEATURES CREATED ✅")
print("=" * 60)