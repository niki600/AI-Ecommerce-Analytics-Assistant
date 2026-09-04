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
    PROCESSED_DIR / "sales_analytics.csv"
)

print("=" * 60)
print("PAYMENT & CUSTOMER REVIEW ANALYSIS")
print("=" * 60)

print("\nSales rows:", len(sales))


# --------------------------------------------------
# 3. PAYMENT ANALYSIS
# --------------------------------------------------

print("\n" + "=" * 60)
print("PAYMENT PERFORMANCE")
print("=" * 60)

payment_summary = (
    sales.groupby("payment_type")
    .agg(
        payment_value=("total_payment_value", "sum"),
        orders=("order_id", "nunique"),
        avg_payment=("total_payment_value", "mean"),
        avg_installments=("payment_installments", "mean")
    )
    .sort_values("payment_value", ascending=False)
    .reset_index()
)

payment_summary["payment_share_pct"] = (
    payment_summary["payment_value"]
    / payment_summary["payment_value"].sum()
    * 100
)

print(payment_summary)


# --------------------------------------------------
# 4. PAYMENT INSTALLMENTS
# --------------------------------------------------

print("\n" + "=" * 60)
print("PAYMENT INSTALLMENT ANALYSIS")
print("=" * 60)

installment_analysis = (
    sales.groupby("payment_installments")
    .agg(
        orders=("order_id", "nunique"),
        payment_value=("total_payment_value", "sum")
    )
    .sort_values("payment_value", ascending=False)
    .reset_index()
)

print(installment_analysis.head(15))


# --------------------------------------------------
# 5. CUSTOMER REVIEW SUMMARY
# --------------------------------------------------

print("\n" + "=" * 60)
print("CUSTOMER REVIEW SUMMARY")
print("=" * 60)

review_summary = (
    sales.groupby("review_score")
    .agg(
        orders=("order_id", "nunique"),
        revenue=("sales_amount", "sum")
    )
    .sort_index()
    .reset_index()
)

review_summary["order_share_pct"] = (
    review_summary["orders"]
    / review_summary["orders"].sum()
    * 100
)

print(review_summary)


# --------------------------------------------------
# 6. REVIEW SCORE OVERVIEW
# --------------------------------------------------

print("\n" + "=" * 60)
print("REVIEW SCORE KPIs")
print("=" * 60)

valid_reviews = sales[
    sales["review_score"].notna()
]

average_review_score = valid_reviews["review_score"].mean()

positive_reviews = (
    valid_reviews["is_positive_review"].sum()
)

total_reviews = len(valid_reviews)

positive_review_rate = (
    positive_reviews / total_reviews * 100
    if total_reviews > 0 else 0
)

print(
    f"Average Review Score : {average_review_score:.2f}"
)

print(
    f"Total Reviewed Orders: {total_reviews}"
)

print(
    f"Positive Reviews     : {positive_reviews}"
)

print(
    f"Positive Review Rate : {positive_review_rate:.2f}%"
)


# --------------------------------------------------
# 7. REVIEW VS DELIVERY DELAY
# --------------------------------------------------

print("\n" + "=" * 60)
print("REVIEW VS DELIVERY PERFORMANCE")
print("=" * 60)

review_delivery = (
    sales[sales["review_score"].notna()]
    .groupby("is_delayed")
    .agg(
        orders=("order_id", "nunique"),
        avg_review_score=("review_score", "mean")
    )
    .reset_index()
)

review_delivery["delivery_status"] = review_delivery[
    "is_delayed"
].apply(
    lambda x: "Delayed" if x == 1 else "On-time / Early"
)

print(
    review_delivery[
        [
            "delivery_status",
            "orders",
            "avg_review_score"
        ]
    ]
)


# --------------------------------------------------
# 8. REVIEW VS PAYMENT
# --------------------------------------------------

print("\n" + "=" * 60)
print("REVIEW VS PAYMENT")
print("=" * 60)

review_payment = (
    sales[sales["review_score"].notna()]
    .groupby("review_score")
    .agg(
        orders=("order_id", "nunique"),
        avg_payment=("total_payment_value", "mean"),
        avg_installments=("payment_installments", "mean")
    )
    .reset_index()
)

print(review_payment)


# --------------------------------------------------
# 9. PAYMENT GAP ANALYSIS
# --------------------------------------------------

print("\n" + "=" * 60)
print("PAYMENT GAP ANALYSIS")
print("=" * 60)

payment_gap_summary = (
    sales.groupby("payment_type")
    .agg(
        orders=("order_id", "nunique"),
        avg_sales_amount=("sales_amount", "mean"),
        avg_payment_value=("total_payment_value", "mean"),
        avg_payment_gap=("payment_gap", "mean")
    )
    .reset_index()
)

print(payment_gap_summary)


# --------------------------------------------------
# 10. REVIEW BY PRODUCT CATEGORY
# --------------------------------------------------

print("\n" + "=" * 60)
print("CATEGORY REVIEW PERFORMANCE")
print("=" * 60)

category_reviews = (
    sales[sales["review_score"].notna()]
    .groupby("product_category_name")
    .agg(
        orders=("order_id", "nunique"),
        avg_review_score=("review_score", "mean"),
        positive_review_rate=("is_positive_review", "mean")
    )
    .reset_index()
)

category_reviews["positive_review_rate"] *= 100

category_reviews = category_reviews.sort_values(
    "avg_review_score",
    ascending=False
)

print(category_reviews.head(15))


# --------------------------------------------------
# 11. SAVE RESULTS
# --------------------------------------------------

print("\n" + "=" * 60)
print("SAVING ANALYTICS RESULTS")
print("=" * 60)

payment_summary.to_csv(
    PROCESSED_DIR / "payment_analysis.csv",
    index=False
)

installment_analysis.to_csv(
    PROCESSED_DIR / "payment_installment_analysis.csv",
    index=False
)

review_summary.to_csv(
    PROCESSED_DIR / "review_score_analysis.csv",
    index=False
)

review_delivery.to_csv(
    PROCESSED_DIR / "review_delivery_analysis.csv",
    index=False
)

review_payment.to_csv(
    PROCESSED_DIR / "review_payment_analysis.csv",
    index=False
)

payment_gap_summary.to_csv(
    PROCESSED_DIR / "payment_gap_analysis.csv",
    index=False
)

category_reviews.to_csv(
    PROCESSED_DIR / "category_review_analysis.csv",
    index=False
)


print("\nAnalytics files saved ✅")

print("- payment_analysis.csv")
print("- payment_installment_analysis.csv")
print("- review_score_analysis.csv")
print("- review_delivery_analysis.csv")
print("- review_payment_analysis.csv")
print("- payment_gap_analysis.csv")
print("- category_review_analysis.csv")

print("\n" + "=" * 60)
print("PAYMENT & REVIEW ANALYSIS COMPLETED ✅")
print("=" * 60)