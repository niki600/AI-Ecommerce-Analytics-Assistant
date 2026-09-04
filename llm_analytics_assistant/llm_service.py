import requests
import re


# --------------------------------------------------
# DATABASE SCHEMA
# --------------------------------------------------

DATABASE_SCHEMA = """
You are working with a PostgreSQL e-commerce analytics database.

TABLE: dashboard_orders

Columns:
- order_id (varchar)
- customer_id (varchar)
- customer_unique_id (varchar)
- customer_state (varchar)
- order_status (varchar)
- order_date (date)
- revenue (numeric)
- freight_cost (numeric)
- delivery_days (numeric)
- estimated_delivery_days (numeric)
- delivery_delay_days (numeric)
- is_delayed (boolean)
- payment_type (varchar)
- total_payment_value (numeric)
- payment_installments (numeric)
- payment_gap (numeric)
- review_score (numeric)
- has_review (boolean)
- is_positive_review (boolean)
- item_count (integer)
- order_year (integer)
- order_month (integer)
- order_month_name (varchar)
- order_year_month (varchar)
- delivery_status (varchar)
- review_category (varchar)
- customer_type (varchar)


TABLE: dashboard_sales

Columns:
- order_id (varchar)
- customer_id (varchar)
- customer_unique_id (varchar)
- product_id (varchar)
- product_category_name (varchar)
- customer_state (varchar)
- customer_type (varchar)
- order_status (varchar)
- order_date (date)
- order_year (integer)
- order_month (integer)
- order_month_name (varchar)
- order_year_month (varchar)
- price (numeric)
- freight_value (numeric)
- sales_amount (numeric)
- freight_cost (numeric)
- total_item_value (numeric)
- revenue (numeric)
- delivery_days (numeric)
- estimated_delivery_days (numeric)
- delivery_delay_days (numeric)
- is_delayed (boolean)
- delivery_status (varchar)
- payment_type (varchar)
- payment_installments (numeric)
- total_payment_value (numeric)
- payment_gap (numeric)
- review_score (numeric)
- review_category (varchar)
- review_count (numeric)
- has_review (boolean)
- is_positive_review (boolean)
"""


# --------------------------------------------------
# CLEAN SQL
# --------------------------------------------------

def clean_sql(sql):

    if not sql:
        raise ValueError("AI returned an empty response.")

    # Convert response to string
    sql = str(sql).strip()

    # Remove Markdown code blocks
    sql = re.sub(
        r"```(?:sql)?",
        "",
        sql,
        flags=re.IGNORECASE
    )

    sql = sql.strip()

    # Find the first SELECT
    match = re.search(
        r"\bSELECT\b",
        sql,
        flags=re.IGNORECASE
    )

    if not match:
        raise ValueError(
            f"AI did not generate a valid SELECT query. Response: {sql}"
        )

    # Remove everything before SELECT
    sql = sql[match.start():]

    # --------------------------------------------------
    # REMOVE COMMON AI MISTAKES
    # --------------------------------------------------

    # Remove accidental END keyword at query end
    sql = re.sub(
        r"\s+\bEND\b\s*;?\s*$",
        "",
        sql,
        flags=re.IGNORECASE
    )

    # Remove "end" after LIMIT values
    sql = re.sub(
        r"(LIMIT\s+\d+)\s+\bEND\b",
        r"\1",
        sql,
        flags=re.IGNORECASE
    )

    # Fix GROUP BY 0, 1 -> GROUP BY 1, 2
    sql = re.sub(
        r"GROUP\s+BY\s+0\s*,\s*1",
        "GROUP BY 1, 2",
        sql,
        flags=re.IGNORECASE
    )

    # Fix GROUP BY 0 -> GROUP BY 1
    sql = re.sub(
        r"GROUP\s+BY\s+0\b",
        "GROUP BY 1",
        sql,
        flags=re.IGNORECASE
    )

    # --------------------------------------------------
    # REMOVE EXTRA SQL STATEMENTS
    # --------------------------------------------------

    # Keep only the first SQL statement
    if ";" in sql:
        sql = sql.split(";")[0]

    # Remove trailing unwanted text after LIMIT
    sql = re.sub(
        r"(LIMIT\s+\d+).*",
        r"\1",
        sql,
        flags=re.IGNORECASE | re.DOTALL
    )

    # Clean whitespace
    sql = re.sub(
        r"\s+",
        " ",
        sql
    ).strip()

    # Add exactly one semicolon
    sql = sql.rstrip(";").strip() + ";"

    return sql


# --------------------------------------------------
# VALIDATE SQL
# --------------------------------------------------

def validate_sql(sql):

    if not sql:
        raise ValueError("Generated SQL is empty.")

    sql_upper = sql.upper().strip()

    # Query must start with SELECT
    if not sql_upper.startswith("SELECT"):
        raise ValueError(
            "Only SELECT queries are allowed."
        )

    # --------------------------------------------------
    # BLOCK DANGEROUS SQL
    # --------------------------------------------------

    dangerous_keywords = [
        "INSERT",
        "UPDATE",
        "DELETE",
        "DROP",
        "ALTER",
        "CREATE",
        "TRUNCATE",
        "GRANT",
        "REVOKE",
        "EXECUTE",
        "CALL"
    ]

    for keyword in dangerous_keywords:

        if re.search(
            rf"\b{keyword}\b",
            sql_upper
        ):

            raise ValueError(
                f"Unsafe SQL keyword detected: {keyword}"
            )

    # Only allowed tables
    allowed_tables = [
        "dashboard_orders",
        "dashboard_sales"
    ]

    # Check FROM table if possible
    table_matches = re.findall(
        r"\bFROM\s+([a-zA-Z_][a-zA-Z0-9_]*)",
        sql,
        flags=re.IGNORECASE
    )

    for table in table_matches:

        if table.lower() not in allowed_tables:

            raise ValueError(
                f"Unauthorized table detected: {table}"
            )

    return True


# --------------------------------------------------
# GENERATE SQL
# --------------------------------------------------

def generate_sql(user_question):

    prompt = f"""
You are an expert PostgreSQL data analyst.

Your task is to convert the user's question into ONE valid PostgreSQL SELECT query.

DATABASE SCHEMA:

{DATABASE_SCHEMA}


IMPORTANT RULES:

- Return ONLY the SQL query.
- Start directly with SELECT.
- Do not use Markdown.
- Do not use code blocks.
- Do not explain the query.
- Do not add comments.
- Generate exactly ONE query.
- Never write the word END.
- Use only SELECT queries.
- Use only the tables and columns provided in the schema.

SQL CLAUSE ORDER MUST ALWAYS BE:

SELECT
FROM
WHERE
GROUP BY
HAVING
ORDER BY
LIMIT

IMPORTANT:

- GROUP BY numbering starts at 1, never 0.
- LIMIT must always be the final SQL clause.
- Never put GROUP BY after LIMIT.
- Never put ORDER BY after LIMIT.
- Do not write anything after the SQL query.
- Check PostgreSQL syntax before responding.

EXAMPLES:

User Question:
What is the total revenue?

Correct SQL:
SELECT SUM(revenue) AS total_revenue
FROM dashboard_orders;


User Question:
What is the average review score?

Correct SQL:
SELECT AVG(review_score) AS average_review_score
FROM dashboard_orders;


User Question:
Which customer type generates more revenue?

Correct SQL:
SELECT customer_type, SUM(revenue) AS total_revenue
FROM dashboard_orders
GROUP BY customer_type
ORDER BY total_revenue DESC
LIMIT 1;


User Question:
Show monthly revenue trends.

Correct SQL:
SELECT order_year_month, SUM(revenue) AS monthly_revenue
FROM dashboard_orders
GROUP BY order_year_month
ORDER BY order_year_month;


NOW ANSWER THIS USER QUESTION:

{user_question}

RETURN ONLY VALID POSTGRESQL SQL.
"""

    try:

        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": "phi3:mini",
                "prompt": prompt,
                "stream": False,
                "options": {
                    "temperature": 0,
                    "num_predict": 300
                }
            },
            timeout=120
        )

        response.raise_for_status()

        data = response.json()

        if "response" not in data:
            raise ValueError(
                "Ollama returned an unexpected response."
            )

        # Get AI-generated SQL
        sql_query = data["response"]

        # Clean SQL
        sql_query = clean_sql(sql_query)

        # Validate SQL
        validate_sql(sql_query)

        return sql_query

    except requests.exceptions.ConnectionError:

        raise ConnectionError(
            "Cannot connect to Ollama. Please make sure Ollama is running."
        )

    except requests.exceptions.Timeout:

        raise TimeoutError(
            "The AI model took too long to generate the query."
        )

    except requests.exceptions.RequestException as e:

        raise ConnectionError(
            f"Error communicating with Ollama: {str(e)}"
        )