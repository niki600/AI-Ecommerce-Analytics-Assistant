import pandas as pd
from pathlib import Path


# --------------------------------------------------
# 1. PATHS
# --------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent.parent

DATA_DIR = BASE_DIR / "data"
PROCESSED_DIR = DATA_DIR / "processed"


# --------------------------------------------------
# 2. LOAD CLEANED DATA
# --------------------------------------------------

orders = pd.read_csv(
    PROCESSED_DIR / "orders_cleaned.csv"
)

order_items = pd.read_csv(
    DATA_DIR / "olist_order_items_dataset.csv"
)


print("=" * 60)
print("ANALYTICAL DATASET PREPARATION")
print("=" * 60)


print("\nOrders rows:", len(orders))
print("Order Items rows:", len(order_items))


# --------------------------------------------------
# 3. CONVERT ORDER DATE
# --------------------------------------------------

orders["order_purchase_timestamp"] = pd.to_datetime(
    orders["order_purchase_timestamp"],
    errors="coerce"
)


# --------------------------------------------------
# 4. JOIN ORDERS + ORDER ITEMS
# --------------------------------------------------

print("\nJoining Orders with Order Items...")

sales = orders.merge(
    order_items,
    on="order_id",
    how="left"
)


# --------------------------------------------------
# 5. CHECK RESULT
# --------------------------------------------------

print("\nJoin completed ✅")

print("Rows after join:", len(sales))
print("Columns after join:", len(sales.columns))


print("\nColumns:")
print(sales.columns.tolist())


# --------------------------------------------------
# 6. CHECK MISSING ORDER IDs
# --------------------------------------------------

missing_order_ids = sales["order_id"].isna().sum()

print("\nMissing order IDs:", missing_order_ids)

# --------------------------------------------------
# 7. LOAD CLEANED PRODUCTS
# --------------------------------------------------

products = pd.read_csv(
    PROCESSED_DIR / "products_cleaned.csv"
)

print("\nProducts rows:", len(products))


# --------------------------------------------------
# 8. JOIN SALES + PRODUCTS
# --------------------------------------------------

print("\nJoining Sales with Products...")

sales = sales.merge(
    products,
    on="product_id",
    how="left"
)

print("Product join completed ✅")


# --------------------------------------------------
# 9. CHECK PRODUCT MATCHING
# --------------------------------------------------

missing_product_match = sales["product_category_name"].isna().sum()

print(
    "Rows with missing product category:",
    missing_product_match
)

print("\nRows after product join:", len(sales))
print("Columns after product join:", len(sales.columns))

# --------------------------------------------------
# 10. LOAD CLEANED CUSTOMERS
# --------------------------------------------------

customers = pd.read_csv(
    PROCESSED_DIR / "customers_cleaned.csv"
)

print("\nCustomers rows:", len(customers))


# --------------------------------------------------
# 11. JOIN SALES + CUSTOMERS
# --------------------------------------------------

print("\nJoining Sales with Customers...")

sales = sales.merge(
    customers,
    on="customer_id",
    how="left"
)

print("Customer join completed ✅")


# --------------------------------------------------
# 12. CHECK CUSTOMER MATCHING
# --------------------------------------------------

missing_customer_match = sales["customer_unique_id"].isna().sum()

print(
    "Rows with missing customer match:",
    missing_customer_match
)

print("\nRows after customer join:", len(sales))
print("Columns after customer join:", len(sales.columns))


print("\nUpdated columns:")
print(sales.columns.tolist())


# --------------------------------------------------
# 13. SAVE ANALYTICAL DATASET
# --------------------------------------------------

output_file = PROCESSED_DIR / "sales_base.csv"

sales.to_csv(
    output_file,
    index=False
)


print("\nSaved:")
print(output_file)


print("\n" + "=" * 60)
print("ANALYTICAL DATASET CREATED ✅")
print("=" * 60)