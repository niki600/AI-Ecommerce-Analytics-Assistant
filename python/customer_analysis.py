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
    PROCESSED_DIR / "sales_analytics.csv"
)

print("=" * 60)
print("CUSTOMER ANALYSIS")
print("=" * 60)

print("\nSales rows:", len(sales))


# --------------------------------------------------
# 3. CUSTOMER LEVEL DATA
# --------------------------------------------------

customer_data = (
    sales.groupby("customer_unique_id")
    .agg(
        orders=("order_id", "nunique"),
        revenue=("sales_amount", "sum"),
        units=("order_item_id", "count"),
        freight_cost=("freight_cost", "sum")
    )
    .reset_index()
)


# --------------------------------------------------
# 4. CUSTOMER AOV
# --------------------------------------------------

customer_data["AOV"] = (
    customer_data["revenue"] /
    customer_data["orders"]
)


# --------------------------------------------------
# 5. CUSTOMER TYPE
# --------------------------------------------------

customer_data["customer_type"] = customer_data["orders"].apply(
    lambda x: "Repeat Customer"
    if x > 1
    else "One-time Customer"
)


# --------------------------------------------------
# 6. CUSTOMER SUMMARY
# --------------------------------------------------

print("\n" + "=" * 60)
print("CUSTOMER SUMMARY")
print("=" * 60)

total_customers = len(customer_data)

repeat_customers = (
    customer_data["customer_type"]
    .eq("Repeat Customer")
    .sum()
)

one_time_customers = (
    customer_data["customer_type"]
    .eq("One-time Customer")
    .sum()
)

print("\nTotal Customers      :", total_customers)
print("Repeat Customers     :", repeat_customers)
print("One-time Customers   :", one_time_customers)


# --------------------------------------------------
# 7. CUSTOMER REVENUE SUMMARY
# --------------------------------------------------

print("\n" + "=" * 60)
print("CUSTOMER REVENUE SUMMARY")
print("=" * 60)

print(
    customer_data[
        ["revenue", "orders", "units", "AOV"]
    ].describe()
)


# --------------------------------------------------
# 8. TOP CUSTOMERS BY REVENUE
# --------------------------------------------------

print("\n" + "=" * 60)
print("TOP CUSTOMERS BY REVENUE")
print("=" * 60)

top_customers = (
    customer_data
    .sort_values("revenue", ascending=False)
    .head(15)
)

print(
    top_customers[
        [
            "customer_unique_id",
            "revenue",
            "orders",
            "units",
            "AOV",
            "customer_type"
        ]
    ].to_string(index=False)
)


# --------------------------------------------------
# 9. TOP REPEAT CUSTOMERS
# --------------------------------------------------

print("\n" + "=" * 60)
print("TOP REPEAT CUSTOMERS")
print("=" * 60)

top_repeat = (
    customer_data[
        customer_data["customer_type"] == "Repeat Customer"
    ]
    .sort_values("orders", ascending=False)
    .head(15)
)

print(
    top_repeat[
        [
            "customer_unique_id",
            "orders",
            "revenue",
            "AOV"
        ]
    ].to_string(index=False)
)


# --------------------------------------------------
# 10. REPEAT VS ONE-TIME REVENUE
# --------------------------------------------------

print("\n" + "=" * 60)
print("REPEAT VS ONE-TIME CUSTOMER REVENUE")
print("=" * 60)

customer_type_summary = (
    customer_data
    .groupby("customer_type")
    .agg(
        customers=("customer_unique_id", "count"),
        revenue=("revenue", "sum"),
        orders=("orders", "sum")
    )
    .reset_index()
)

customer_type_summary["revenue_share_pct"] = (
    customer_type_summary["revenue"]
    / customer_type_summary["revenue"].sum()
    * 100
)

print(customer_type_summary)


# --------------------------------------------------
# 11. ORDER FREQUENCY
# --------------------------------------------------

print("\n" + "=" * 60)
print("CUSTOMER ORDER FREQUENCY")
print("=" * 60)

order_frequency = (
    customer_data["orders"]
    .value_counts()
    .sort_index()
    .rename_axis("orders")
    .reset_index(name="customers")
)

print(order_frequency)


# --------------------------------------------------
# 12. SAVE RESULTS
# --------------------------------------------------

customer_data.to_csv(
    PROCESSED_DIR / "customer_analysis.csv",
    index=False
)

customer_type_summary.to_csv(
    PROCESSED_DIR / "customer_type_analysis.csv",
    index=False
)

order_frequency.to_csv(
    PROCESSED_DIR / "customer_order_frequency.csv",
    index=False
)


print("\n" + "=" * 60)
print("CUSTOMER ANALYSIS COMPLETED ✅")
print("=" * 60)

print("\nFiles saved:")
print("- customer_analysis.csv")
print("- customer_type_analysis.csv")
print("- customer_order_frequency.csv")