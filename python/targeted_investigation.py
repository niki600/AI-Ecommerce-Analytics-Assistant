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


# --------------------------------------------------
# 3. ORDERS - SUSPICIOUS DELIVERED ORDERS
# --------------------------------------------------

print("=" * 60)
print("TARGETED DATA QUALITY INVESTIGATION")
print("=" * 60)


print("\n" + "=" * 60)
print("1. DELIVERED ORDERS WITH MISSING APPROVAL DATE")
print("=" * 60)

issue_approval = orders[
    (orders["order_status"] == "delivered") &
    (orders["order_approved_at"].isna())
]

print(f"Records found: {len(issue_approval)}")

if len(issue_approval) > 0:
    print("\nSuspicious records:")
    print(
        issue_approval[
            [
                "order_id",
                "customer_id",
                "order_status",
                "order_purchase_timestamp",
                "order_approved_at",
                "order_delivered_carrier_date",
                "order_delivered_customer_date"
            ]
        ].to_string(index=False)
    )


# --------------------------------------------------
# 4. DELIVERED ORDERS WITH MISSING CARRIER DATE
# --------------------------------------------------

print("\n" + "=" * 60)
print("2. DELIVERED ORDERS WITH MISSING CARRIER DATE")
print("=" * 60)

issue_carrier = orders[
    (orders["order_status"] == "delivered") &
    (orders["order_delivered_carrier_date"].isna())
]

print(f"Records found: {len(issue_carrier)}")

if len(issue_carrier) > 0:
    print("\nSuspicious records:")
    print(
        issue_carrier[
            [
                "order_id",
                "customer_id",
                "order_status",
                "order_purchase_timestamp",
                "order_approved_at",
                "order_delivered_carrier_date",
                "order_delivered_customer_date"
            ]
        ].to_string(index=False)
    )


# --------------------------------------------------
# 5. DELIVERED ORDERS WITH MISSING CUSTOMER DELIVERY DATE
# --------------------------------------------------

print("\n" + "=" * 60)
print("3. DELIVERED ORDERS WITH MISSING CUSTOMER DELIVERY DATE")
print("=" * 60)

issue_delivery = orders[
    (orders["order_status"] == "delivered") &
    (orders["order_delivered_customer_date"].isna())
]

print(f"Records found: {len(issue_delivery)}")

if len(issue_delivery) > 0:
    print("\nSuspicious records:")
    print(
        issue_delivery[
            [
                "order_id",
                "customer_id",
                "order_status",
                "order_purchase_timestamp",
                "order_approved_at",
                "order_delivered_carrier_date",
                "order_delivered_customer_date",
                "order_estimated_delivery_date"
            ]
        ].to_string(index=False)
    )


# --------------------------------------------------
# 6. PRODUCTS WITH MISSING CATEGORY
# --------------------------------------------------

print("\n" + "=" * 60)
print("4. PRODUCTS WITH MISSING CATEGORY")
print("=" * 60)

missing_category = products[
    products["product_category_name"].isna()
]

print(f"Products found: {len(missing_category)}")

if len(missing_category) > 0:
    print("\nSample records:")
    print(
        missing_category.head(20).to_string(index=False)
    )


# --------------------------------------------------
# 7. PRODUCTS WITH MISSING PHYSICAL ATTRIBUTES
# --------------------------------------------------

print("\n" + "=" * 60)
print("5. PRODUCTS WITH MISSING PHYSICAL ATTRIBUTES")
print("=" * 60)

physical_columns = [
    "product_weight_g",
    "product_length_cm",
    "product_height_cm",
    "product_width_cm"
]

for column in physical_columns:

    missing_count = products[column].isna().sum()

    print(f"{column}: {missing_count}")


# --------------------------------------------------
# 8. FINAL SUMMARY
# --------------------------------------------------

print("\n" + "=" * 60)
print("INVESTIGATION SUMMARY")
print("=" * 60)

print(f"Delivered + missing approval date  : {len(issue_approval)}")
print(f"Delivered + missing carrier date   : {len(issue_carrier)}")
print(f"Delivered + missing delivery date  : {len(issue_delivery)}")
print(f"Products + missing category       : {len(missing_category)}")

print("\nTARGETED INVESTIGATION COMPLETED")
print("=" * 60)