import pandas as pd
from pathlib import Path


# --------------------------------------------------
# 1. PATHS
# --------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent.parent

PROCESSED_DIR = BASE_DIR / "data" / "processed"


# --------------------------------------------------
# 2. LOAD DATA
# --------------------------------------------------

sales = pd.read_csv(
    PROCESSED_DIR / "sales_analytics.csv"
)

print("=" * 60)
print("DELIVERY & LOGISTICS ANALYSIS")
print("=" * 60)

print("\nSales rows:", len(sales))


# --------------------------------------------------
# 3. CONVERT DATE COLUMNS
# --------------------------------------------------

print("\nConverting date columns...")

date_columns = [
    "order_purchase_timestamp",
    "order_delivered_carrier_date",
    "order_delivered_customer_date",
    "order_estimated_delivery_date"
]

for column in date_columns:
    sales[column] = pd.to_datetime(
        sales[column],
        errors="coerce"
    )

print("Date conversion completed ✅")


# --------------------------------------------------
# 4. ORDER LEVEL DATA
# --------------------------------------------------

# Sales dataset has multiple rows for orders
# because one order can contain multiple products.
#
# Therefore delivery analysis should be done
# at order level.

order_data = (
    sales.groupby("order_id")
    .agg(
        order_status=("order_status", "first"),
        customer_state=("customer_state", "first"),
        order_purchase_timestamp=(
            "order_purchase_timestamp",
            "first"
        ),
        order_delivered_carrier_date=(
            "order_delivered_carrier_date",
            "first"
        ),
        order_delivered_customer_date=(
            "order_delivered_customer_date",
            "first"
        ),
        order_estimated_delivery_date=(
            "order_estimated_delivery_date",
            "first"
        )
    )
    .reset_index()
)


# --------------------------------------------------
# 5. DELIVERY DAYS
# --------------------------------------------------

order_data["delivery_days"] = (
    order_data["order_delivered_customer_date"]
    - order_data["order_purchase_timestamp"]
).dt.total_seconds() / 86400


# --------------------------------------------------
# 6. ESTIMATED DELIVERY DAYS
# --------------------------------------------------

order_data["estimated_delivery_days"] = (
    order_data["order_estimated_delivery_date"]
    - order_data["order_purchase_timestamp"]
).dt.total_seconds() / 86400


# --------------------------------------------------
# 7. DELIVERY DELAY
# --------------------------------------------------

order_data["delivery_delay_days"] = (
    order_data["order_delivered_customer_date"]
    - order_data["order_estimated_delivery_date"]
).dt.total_seconds() / 86400


# --------------------------------------------------
# 8. DELAY STATUS
# --------------------------------------------------

order_data["is_delayed"] = (
    order_data["delivery_delay_days"] > 0
)


# --------------------------------------------------
# 9. DELIVERY SUMMARY
# --------------------------------------------------

print("\n" + "=" * 60)
print("DELIVERY SUMMARY")
print("=" * 60)

orders_with_delivery = (
    order_data["order_delivered_customer_date"]
    .notna()
    .sum()
)

delayed_orders = (
    order_data["is_delayed"]
    .fillna(False)
    .sum()
)

on_time_orders = (
    orders_with_delivery - delayed_orders
)

print("\nTotal orders:", len(order_data))
print("Orders with delivery date:", orders_with_delivery)
print("Delayed orders:", delayed_orders)
print("On-time / early orders:", on_time_orders)


# --------------------------------------------------
# 10. DELIVERY STATISTICS
# --------------------------------------------------

print("\n" + "=" * 60)
print("DELIVERY TIME STATISTICS")
print("=" * 60)

print(
    order_data["delivery_days"]
    .describe()
)


# --------------------------------------------------
# 11. STATE LEVEL DELIVERY PERFORMANCE
# --------------------------------------------------

print("\n" + "=" * 60)
print("STATE LEVEL DELIVERY PERFORMANCE")
print("=" * 60)

state_delivery = (
    order_data
    .dropna(subset=["delivery_days"])
    .groupby("customer_state")
    .agg(
        orders=("order_id", "count"),
        avg_delivery_days=("delivery_days", "mean"),
        median_delivery_days=("delivery_days", "median"),
        delayed_orders=("is_delayed", "sum")
    )
    .reset_index()
)

state_delivery["delay_rate_pct"] = (
    state_delivery["delayed_orders"]
    / state_delivery["orders"]
    * 100
)

state_delivery = state_delivery.sort_values(
    "avg_delivery_days",
    ascending=False
)

print(
    state_delivery
    .head(15)
    .to_string(index=False)
)


# --------------------------------------------------
# 12. WORST STATES BY DELAY RATE
# --------------------------------------------------

print("\n" + "=" * 60)
print("STATES WITH HIGHEST DELAY RATE")
print("=" * 60)

worst_states = (
    state_delivery
    .sort_values(
        "delay_rate_pct",
        ascending=False
    )
    .head(15)
)

print(
    worst_states
    .to_string(index=False)
)


# --------------------------------------------------
# 13. ORDER STATUS DELIVERY ANALYSIS
# --------------------------------------------------

print("\n" + "=" * 60)
print("DELIVERY BY ORDER STATUS")
print("=" * 60)

status_delivery = (
    order_data
    .groupby("order_status")
    .agg(
        orders=("order_id", "count"),
        avg_delivery_days=("delivery_days", "mean"),
        delayed_orders=("is_delayed", "sum")
    )
    .reset_index()
)

status_delivery["delay_rate_pct"] = (
    status_delivery["delayed_orders"]
    / status_delivery["orders"]
    * 100
)

print(
    status_delivery
    .sort_values(
        "orders",
        ascending=False
    )
    .to_string(index=False)
)


# --------------------------------------------------
# 14. DELIVERY TIME BUCKETS
# --------------------------------------------------

print("\n" + "=" * 60)
print("DELIVERY TIME DISTRIBUTION")
print("=" * 60)

delivery_orders = order_data[
    order_data["delivery_days"].notna()
].copy()

delivery_orders["delivery_bucket"] = pd.cut(
    delivery_orders["delivery_days"],
    bins=[
        -1,
        3,
        7,
        14,
        21,
        30,
        float("inf")
    ],
    labels=[
        "0-3 days",
        "4-7 days",
        "8-14 days",
        "15-21 days",
        "22-30 days",
        "30+ days"
    ]
)

delivery_distribution = (
    delivery_orders["delivery_bucket"]
    .value_counts()
    .sort_index()
    .rename_axis("delivery_bucket")
    .reset_index(name="orders")
)

delivery_distribution["percentage"] = (
    delivery_distribution["orders"]
    / delivery_distribution["orders"].sum()
    * 100
)

print(delivery_distribution)


# --------------------------------------------------
# 15. TOP LONGEST DELIVERY ORDERS
# --------------------------------------------------

print("\n" + "=" * 60)
print("LONGEST DELIVERY ORDERS")
print("=" * 60)

longest_delivery = (
    order_data[
        order_data["delivery_days"].notna()
    ]
    .sort_values(
        "delivery_days",
        ascending=False
    )
    .head(15)
)

print(
    longest_delivery[
        [
            "order_id",
            "customer_state",
            "delivery_days",
            "estimated_delivery_days",
            "delivery_delay_days",
            "is_delayed"
        ]
    ].to_string(index=False)
)


# --------------------------------------------------
# 16. SAVE RESULTS
# --------------------------------------------------

order_data.to_csv(
    PROCESSED_DIR / "order_delivery_analysis.csv",
    index=False
)

state_delivery.to_csv(
    PROCESSED_DIR / "state_delivery_analysis.csv",
    index=False
)

status_delivery.to_csv(
    PROCESSED_DIR / "status_delivery_analysis.csv",
    index=False
)

delivery_distribution.to_csv(
    PROCESSED_DIR / "delivery_distribution.csv",
    index=False
)

worst_states.to_csv(
    PROCESSED_DIR / "worst_states_by_delay.csv",
    index=False
)


# --------------------------------------------------
# 17. FINAL SUMMARY
# --------------------------------------------------

print("\n" + "=" * 60)
print("DELIVERY & LOGISTICS ANALYSIS COMPLETED ✅")
print("=" * 60)

print("\nFiles saved:")
print("- order_delivery_analysis.csv")
print("- state_delivery_analysis.csv")
print("- status_delivery_analysis.csv")
print("- delivery_distribution.csv")
print("- worst_states_by_delay.csv")