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
print("CUSTOMER RELATIONSHIP VALIDATION")
print("=" * 60)


# --------------------------------------------------
# 3. BASIC CUSTOMER CHECK
# --------------------------------------------------

print("\nTotal sales rows:", len(sales))

print(
    "Unique customer_id:",
    sales["customer_id"].nunique()
)

print(
    "Unique customer_unique_id:",
    sales["customer_unique_id"].nunique()
)


# --------------------------------------------------
# 4. MISSING CUSTOMER IDs
# --------------------------------------------------

print("\n" + "=" * 60)
print("MISSING CUSTOMER IDs")
print("=" * 60)

missing_customer_id = sales["customer_id"].isna().sum()

missing_unique_id = sales["customer_unique_id"].isna().sum()

print(
    "Missing customer_id:",
    missing_customer_id
)

print(
    "Missing customer_unique_id:",
    missing_unique_id
)


# --------------------------------------------------
# 5. CUSTOMER ID → UNIQUE CUSTOMER ID
# --------------------------------------------------

print("\n" + "=" * 60)
print("CUSTOMER ID RELATIONSHIP")
print("=" * 60)

customer_mapping = (
    sales[
        ["customer_id", "customer_unique_id"]
    ]
    .drop_duplicates()
)

multiple_unique_ids = (
    customer_mapping
    .groupby("customer_id")["customer_unique_id"]
    .nunique()
)

invalid_customer_mapping = (
    multiple_unique_ids[
        multiple_unique_ids > 1
    ]
)

print(
    "customer_id linked to multiple "
    "customer_unique_id:",
    len(invalid_customer_mapping)
)


# --------------------------------------------------
# 6. UNIQUE CUSTOMER → CUSTOMER ID
# --------------------------------------------------

print("\n" + "=" * 60)
print("UNIQUE CUSTOMER → CUSTOMER ID ANALYSIS")
print("=" * 60)

customer_id_count = (
    customer_mapping
    .groupby("customer_unique_id")["customer_id"]
    .nunique()
)

multiple_customer_ids = (
    customer_id_count[
        customer_id_count > 1
    ]
)

print(
    "Unique customers with multiple customer_id:",
    len(multiple_customer_ids)
)


# --------------------------------------------------
# 7. TOP REPEAT CUSTOMERS
# --------------------------------------------------

print("\n" + "=" * 60)
print("TOP REPEAT CUSTOMERS")
print("=" * 60)

repeat_customers = (
    sales
    .groupby("customer_unique_id")
    ["order_id"]
    .nunique()
    .sort_values(ascending=False)
)

print(
    repeat_customers
    .head(10)
)


# --------------------------------------------------
# 8. CUSTOMER ORDER DISTRIBUTION
# --------------------------------------------------

print("\n" + "=" * 60)
print("CUSTOMER ORDER DISTRIBUTION")
print("=" * 60)

order_distribution = (
    repeat_customers
    .value_counts()
    .sort_index()
)

print(order_distribution.head(10))


# --------------------------------------------------
# 9. REPEAT CUSTOMER COUNT
# --------------------------------------------------

repeat_customer_count = (
    (repeat_customers > 1)
    .sum()
)

total_unique_customers = (
    repeat_customers.count()
)

print("\n" + "=" * 60)
print("REPEAT CUSTOMER SUMMARY")
print("=" * 60)

print(
    "Total unique customers:",
    total_unique_customers
)

print(
    "Repeat customers:",
    repeat_customer_count
)

print(
    "One-time customers:",
    total_unique_customers
    - repeat_customer_count
)


# --------------------------------------------------
# 10. FINAL STATUS
# --------------------------------------------------

print("\n" + "=" * 60)
print("CUSTOMER RELATIONSHIP VALIDATION COMPLETED")
print("=" * 60)