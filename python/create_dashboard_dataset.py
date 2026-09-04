import pandas as pd
from pathlib import Path


# ==================================================
# 1. PATHS
# ==================================================

BASE_DIR = Path(__file__).resolve().parent.parent

DATA_DIR = BASE_DIR / "data"
PROCESSED_DIR = DATA_DIR / "processed"


# ==================================================
# 2. LOAD DATA
# ==================================================

sales = pd.read_csv(
    PROCESSED_DIR / "sales_analytics.csv"
)

print("=" * 60)
print("FINAL DASHBOARD DATASET CREATION")
print("=" * 60)

print("\nSource rows:", len(sales))
print("Source columns:", len(sales.columns))


# ==================================================
# 3. DATE CONVERSION
# ==================================================

print("\nConverting date columns...")

date_columns = [
    "order_purchase_timestamp",
    "order_approved_at",
    "order_delivered_carrier_date",
    "order_delivered_customer_date",
    "order_estimated_delivery_date"
]

for column in date_columns:
    if column in sales.columns:
        sales[column] = pd.to_datetime(
            sales[column],
            errors="coerce"
        )

print("Date conversion completed ✅")


# ==================================================
# 4. CLEAN CATEGORY VALUES
# ==================================================

if "product_category_name" in sales.columns:

    sales["product_category_name"] = (
        sales["product_category_name"]
        .fillna("Unknown")
        .astype(str)
        .str.replace("_", " ", regex=False)
        .str.title()
    )


# ==================================================
# 5. CLEAN PAYMENT TYPE
# ==================================================

if "payment_type" in sales.columns:

    sales["payment_type"] = (
        sales["payment_type"]
        .fillna("Unknown")
        .astype(str)
        .str.replace("_", " ", regex=False)
        .str.title()
    )


# ==================================================
# 6. CREATE BUSINESS-FRIENDLY FEATURES
# ==================================================

print("\nCreating dashboard features...")


# Revenue

if "sales_amount" in sales.columns:

    sales["revenue"] = sales["sales_amount"]


# Freight

if "freight_cost" in sales.columns:

    sales["freight_cost"] = sales["freight_cost"]


# Total item value

if (
    "price" in sales.columns
    and "freight_value" in sales.columns
):

    sales["total_item_value"] = (
        sales["price"] +
        sales["freight_value"]
    )


# Order month

if "order_purchase_timestamp" in sales.columns:

    sales["order_date"] = (
        sales["order_purchase_timestamp"]
        .dt.date
    )

    sales["order_year"] = (
        sales["order_purchase_timestamp"]
        .dt.year
    )

    sales["order_month"] = (
        sales["order_purchase_timestamp"]
        .dt.month
    )

    sales["order_month_name"] = (
        sales["order_purchase_timestamp"]
        .dt.month_name()
    )

    sales["order_year_month"] = (
        sales["order_purchase_timestamp"]
        .dt.to_period("M")
        .astype(str)
    )


# ==================================================
# 7. DELIVERY STATUS
# ==================================================

if "is_delayed" in sales.columns:

    sales["delivery_status"] = sales[
        "is_delayed"
    ].apply(
        lambda x:
        "Delayed"
        if x == True
        else "On-time / Early"
        if x == False
        else "Unknown"
    )


# ==================================================
# 8. CUSTOMER TYPE
# ==================================================

if "customer_unique_id" in sales.columns:

    customer_order_count = (
        sales.groupby("customer_unique_id")[
            "order_id"
        ]
        .nunique()
    )

    sales["customer_type"] = (
        sales["customer_unique_id"]
        .map(customer_order_count)
        .apply(
            lambda x:
            "Repeat Customer"
            if x > 1
            else "One-time Customer"
        )
    )


# ==================================================
# 9. REVIEW CATEGORY
# ==================================================

if "review_score" in sales.columns:

    sales["review_category"] = (
        sales["review_score"]
        .apply(
            lambda x:
            "Very Low"
            if pd.notna(x) and x <= 2
            else "Average"
            if pd.notna(x) and x == 3
            else "Good"
            if pd.notna(x) and x == 4
            else "Excellent"
            if pd.notna(x) and x >= 5
            else "No Review"
        )
    )


# ==================================================
# 10. SELECT DASHBOARD COLUMNS
# ==================================================

dashboard_columns = [
    # Identifiers
    "order_id",
    "customer_id",
    "customer_unique_id",
    "product_id",

    # Product
    "product_category_name",

    # Customer
    "customer_state",
    "customer_type",

    # Order
    "order_status",
    "order_date",
    "order_year",
    "order_month",
    "order_month_name",
    "order_year_month",

    # Revenue
    "price",
    "freight_value",
    "sales_amount",
    "freight_cost",
    "total_item_value",
    "revenue",

    # Delivery
    "delivery_days",
    "estimated_delivery_days",
    "delivery_delay_days",
    "is_delayed",
    "delivery_status",

    # Payment
    "payment_type",
    "payment_installments",
    "total_payment_value",
    "payment_gap",

    # Review
    "review_score",
    "review_category",
    "review_count",
    "has_review",
    "is_positive_review"
]


# Keep only columns that exist

dashboard_columns = [
    column
    for column in dashboard_columns
    if column in sales.columns
]

dashboard_sales = sales[
    dashboard_columns
].copy()


# ==================================================
# 11. REMOVE EXACT DUPLICATES
# ==================================================

dashboard_sales = (
    dashboard_sales
    .drop_duplicates()
    .reset_index(drop=True)
)


# ==================================================
# 12. CREATE ORDER-LEVEL DATASET
# ==================================================

print("\nCreating order-level dashboard dataset...")

order_data = (
    sales.groupby("order_id")
    .agg(
        customer_id=("customer_id", "first"),
        customer_unique_id=("customer_unique_id", "first"),
        customer_state=("customer_state", "first"),
        order_status=("order_status", "first"),

        order_date=("order_purchase_timestamp", "first"),

        revenue=("sales_amount", "sum"),
        freight_cost=("freight_value", "sum"),

        delivery_days=("delivery_days", "first"),
        estimated_delivery_days=(
            "estimated_delivery_days",
            "first"
        ),

        delivery_delay_days=(
            "delivery_delay_days",
            "first"
        ),

        is_delayed=("is_delayed", "first"),

        payment_type=("payment_type", "first"),
        total_payment_value=(
            "total_payment_value",
            "first"
        ),

        payment_installments=(
            "payment_installments",
            "first"
        ),

        payment_gap=("payment_gap", "first"),

        review_score=("review_score", "first"),
        has_review=("has_review", "first"),
        is_positive_review=(
            "is_positive_review",
            "first"
        ),

        item_count=("order_id", "size")
    )
    .reset_index()
)


# ==================================================
# 13. ORDER-LEVEL FEATURES
# ==================================================

order_data["order_year"] = (
    order_data["order_date"]
    .dt.year
)

order_data["order_month"] = (
    order_data["order_date"]
    .dt.month
)

order_data["order_month_name"] = (
    order_data["order_date"]
    .dt.month_name()
)

order_data["order_year_month"] = (
    order_data["order_date"]
    .dt.to_period("M")
    .astype(str)
)

order_data["delivery_status"] = (
    order_data["is_delayed"]
    .apply(
        lambda x:
        "Delayed"
        if x == True
        else "On-time / Early"
        if x == False
        else "Unknown"
    )
)

order_data["review_category"] = (
    order_data["review_score"]
    .apply(
        lambda x:
        "Very Low"
        if pd.notna(x) and x <= 2
        else "Average"
        if pd.notna(x) and x == 3
        else "Good"
        if pd.notna(x) and x == 4
        else "Excellent"
        if pd.notna(x) and x >= 5
        else "No Review"
    )
)


# ==================================================
# 14. CUSTOMER TYPE AT ORDER LEVEL
# ==================================================

customer_orders = (
    order_data.groupby(
        "customer_unique_id"
    )["order_id"]
    .transform("nunique")
)

order_data["customer_type"] = (
    customer_orders
    .apply(
        lambda x:
        "Repeat Customer"
        if x > 1
        else "One-time Customer"
    )
)


# ==================================================
# 15. CHECK DATA QUALITY
# ==================================================

print("\n" + "=" * 60)
print("DASHBOARD DATA QUALITY CHECK")
print("=" * 60)

print("\nDashboard sales rows:")
print(len(dashboard_sales))

print("\nDashboard sales columns:")
print(len(dashboard_sales.columns))

print("\nOrder-level rows:")
print(len(order_data))

print(
    "\nUnique orders in order dataset:",
    order_data["order_id"].nunique()
)

print(
    "Unique customers:",
    order_data["customer_unique_id"].nunique()
)

print(
    "Duplicate order IDs:",
    order_data["order_id"].duplicated().sum()
)


# ==================================================
# 16. SAVE FILES
# ==================================================

dashboard_sales_file = (
    PROCESSED_DIR /
    "dashboard_sales.csv"
)

dashboard_orders_file = (
    PROCESSED_DIR /
    "dashboard_orders.csv"
)


dashboard_sales.to_csv(
    dashboard_sales_file,
    index=False
)

order_data.to_csv(
    dashboard_orders_file,
    index=False
)


# ==================================================
# 17. FINAL OUTPUT
# ==================================================

print("\n" + "=" * 60)
print("DASHBOARD DATASETS CREATED ✅")
print("=" * 60)

print("\nSaved:")

print(
    dashboard_sales_file
)

print(
    dashboard_orders_file
)

print("\nFiles:")

print("- dashboard_sales.csv")
print("- dashboard_orders.csv")

print("\n" + "=" * 60)
print("FINAL DASHBOARD PREPARATION COMPLETED ✅")
print("=" * 60)