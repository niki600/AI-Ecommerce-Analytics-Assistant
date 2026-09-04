import pandas as pd
from pathlib import Path


# --------------------------------------------------
# 1. DATA FOLDER PATH
# --------------------------------------------------

DATA_DIR = Path(__file__).resolve().parent.parent / "data"


# --------------------------------------------------
# 2. LOAD DATA
# --------------------------------------------------

customers = pd.read_csv(DATA_DIR / "olist_customers_dataset.csv")
orders = pd.read_csv(DATA_DIR / "olist_orders_dataset.csv")
order_items = pd.read_csv(DATA_DIR / "olist_order_items_dataset.csv")
products = pd.read_csv(DATA_DIR / "olist_products_dataset.csv")
sellers = pd.read_csv(DATA_DIR / "olist_sellers_dataset.csv")
payments = pd.read_csv(DATA_DIR / "olist_order_payments_dataset.csv")
reviews = pd.read_csv(DATA_DIR / "olist_order_reviews_dataset.csv")


# --------------------------------------------------
# 3. PRIMARY KEY VALIDATION
# --------------------------------------------------

def check_primary_key(df, column, table_name):

    duplicate_count = df[column].duplicated().sum()

    print(f"\n{table_name}")
    print(f"Primary Key: {column}")
    print(f"Duplicate values: {duplicate_count}")

    if duplicate_count == 0:
        print("Status: PASS ✅")
    else:
        print("Status: FAIL ❌")


print("=" * 60)
print("PRIMARY KEY VALIDATION")
print("=" * 60)

check_primary_key(customers, "customer_id", "Customers")
check_primary_key(orders, "order_id", "Orders")
check_primary_key(products, "product_id", "Products")
check_primary_key(sellers, "seller_id", "Sellers")


# --------------------------------------------------
# 4. FOREIGN KEY VALIDATION
# --------------------------------------------------

def check_foreign_key(
    child_df,
    child_column,
    parent_df,
    parent_column,
    relationship_name
):

    unmatched = ~child_df[child_column].isin(
        parent_df[parent_column]
    )

    unmatched_count = unmatched.sum()

    print(f"\n{relationship_name}")
    print(f"Unmatched records: {unmatched_count}")

    if unmatched_count == 0:
        print("Status: PASS ✅")
    else:
        print("Status: FAIL ❌")


print("\n" + "=" * 60)
print("FOREIGN KEY VALIDATION")
print("=" * 60)


check_foreign_key(
    orders,
    "customer_id",
    customers,
    "customer_id",
    "Orders → Customers"
)

check_foreign_key(
    order_items,
    "order_id",
    orders,
    "order_id",
    "Order Items → Orders"
)

check_foreign_key(
    order_items,
    "product_id",
    products,
    "product_id",
    "Order Items → Products"
)

check_foreign_key(
    order_items,
    "seller_id",
    sellers,
    "seller_id",
    "Order Items → Sellers"
)

check_foreign_key(
    payments,
    "order_id",
    orders,
    "order_id",
    "Payments → Orders"
)

check_foreign_key(
    reviews,
    "order_id",
    orders,
    "order_id",
    "Reviews → Orders"
)


print("\n" + "=" * 60)
print("RELATIONSHIP VALIDATION COMPLETED")
print("=" * 60)