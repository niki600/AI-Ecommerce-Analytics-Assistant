import streamlit as st
import pandas as pd
import numbers

from llm_service import generate_sql
from database import execute_query


# ==================================================
# PAGE CONFIG
# ==================================================

st.set_page_config(
    page_title="AI E-commerce Analytics Assistant",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ==================================================
# CUSTOM CSS
# ==================================================

st.markdown(
    """
    <style>

    .stApp {
        background-color: #f6f8fc;
    }

    h1 {
        color: #1f2937;
        font-weight: 700;
    }

    h2, h3 {
        color: #374151;
    }

    .stButton > button {
        width: 100%;
        border-radius: 10px;
        min-height: 45px;
        font-size: 15px;
        font-weight: 600;
        transition: 0.2s;
    }

    .stButton > button:hover {
        transform: translateY(-1px);
    }

    .stTextInput input {
        border-radius: 10px;
        padding: 12px;
        font-size: 16px;
    }

    [data-testid="stSidebar"] {
        background-color: #eef2f7;
    }

    [data-testid="stDataFrame"] {
        border-radius: 10px;
        overflow: hidden;
    }

    [data-testid="stMetric"] {
        background-color: white;
        padding: 18px;
        border-radius: 14px;
        border: 1px solid #e5e7eb;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.06);
    }

    </style>
    """,
    unsafe_allow_html=True
)


# ==================================================
# SESSION STATE
# ==================================================

if "question" not in st.session_state:
    st.session_state.question = ""

if "last_sql" not in st.session_state:
    st.session_state.last_sql = None

if "last_result" not in st.session_state:
    st.session_state.last_result = None

if "last_question" not in st.session_state:
    st.session_state.last_question = None

if "history" not in st.session_state:
    st.session_state.history = []


# ==================================================
# HELPER FUNCTIONS
# ==================================================

def set_question(question_text):
    """
    Set question from example/history button.
    """
    st.session_state.question = question_text


def format_number(value):
    """
    Safely format numeric values.
    """

    if value is None:
        return "No Data"

    try:

        if pd.isna(value):
            return "No Data"

    except Exception:
        pass

    if isinstance(value, numbers.Number):

        # Integer
        if float(value).is_integer():

            return f"{int(value):,}"

        # Decimal / Float
        return f"{float(value):,.2f}"

    return str(value)


def get_numeric_columns(dataframe):
    """
    Detect numeric columns safely.

    Also handles PostgreSQL Decimal values that may
    appear as object dtype in Pandas.
    """

    numeric_columns = []

    for column in dataframe.columns:

        series = dataframe[column]

        # Already numeric
        if pd.api.types.is_numeric_dtype(series):

            numeric_columns.append(column)

        else:

            # Try converting object values to numeric
            converted = pd.to_numeric(
                series,
                errors="coerce"
            )

            original_non_null = series.dropna()

            converted_non_null = converted.dropna()

            # Consider numeric only when all
            # non-null values can be converted
            if (
                len(original_non_null) > 0
                and len(converted_non_null)
                == len(original_non_null)
            ):

                dataframe[column] = converted

                numeric_columns.append(column)

    return numeric_columns


def is_time_column(column_name):
    """
    Check whether a column represents time/date data.
    """

    column_name = str(column_name).lower()

    time_keywords = [

        "date",
        "month",
        "year",
        "time",
        "day",
        "week"

    ]

    return any(
        keyword in column_name
        for keyword in time_keywords
    )


def should_show_chart(
    dataframe,
    numeric_columns,
    non_numeric_columns
):
    """
    Decide whether visualization is meaningful.

    Rules:
    - At least 2 rows
    - At least 1 numeric value
    - Must have something to compare
    """

    if len(dataframe) < 2:
        return False

    if len(numeric_columns) < 1:
        return False

    return True


# ==================================================
# SIDEBAR
# ==================================================

with st.sidebar:

    st.title("📊 AI Analytics")

    st.caption(
        "Your intelligent e-commerce data assistant"
    )

    st.markdown("---")


    # ==============================================
    # EXAMPLE QUESTIONS
    # ==============================================

    st.subheader("💡 Example Questions")

    example_questions = [

        "What is the total revenue?",

        "What are the top 10 product categories by sales?",

        "Which states generate the highest revenue?",

        "What is the average review score?",

        "How many orders were delayed?",

        "Which payment method is most popular?",

        "Show monthly revenue trends",

        "Which customer type generates more revenue?"

    ]


    for i, example in enumerate(example_questions):

        if st.button(
            example,
            key=f"example_{i}"
        ):

            set_question(example)

            st.rerun()


    st.markdown("---")


    # ==============================================
    # AI MODEL
    # ==============================================

    st.subheader("🤖 AI Model")

    st.success("phi3:mini")

    st.caption(
        "Running locally with Ollama"
    )


    st.markdown("---")


    # ==============================================
    # RECENT QUESTIONS
    # ==============================================

    st.subheader("🕘 Recent Questions")

    if st.session_state.history:

        recent_questions = list(
            reversed(
                st.session_state.history[-5:]
            )
        )

        for i, item in enumerate(recent_questions):

            if st.button(
                f"💬 {item}",
                key=f"history_{i}"
            ):

                set_question(item)

                st.rerun()

    else:

        st.caption(
            "No questions yet."
        )


    st.markdown("---")


    # ==============================================
    # CLEAR ANALYSIS
    # ==============================================

    if st.button(
        "🗑️ Clear Analysis"
    ):

        st.session_state.question = ""

        st.session_state.last_sql = None

        st.session_state.last_result = None

        st.session_state.last_question = None

        st.rerun()


# ==================================================
# MAIN HEADER
# ==================================================

st.title(
    "📊 E-commerce Analytics Assistant"
)

st.markdown(
    """
    Ask questions about your **e-commerce data**
    and get instant insights using
    **AI-powered SQL generation**.
    """
)

st.markdown("---")


# ==================================================
# QUESTION INPUT
# ==================================================

question = st.text_input(
    "🔍 What would you like to know?",
    key="question",
    placeholder=(
        "Example: What is the total revenue?"
    )
)


# ==================================================
# ANALYZE BUTTON
# ==================================================

col1, col2 = st.columns([2, 8])


with col1:

    analyze = st.button(
        "✨ Analyze Data",
        type="primary"
    )


with col2:

    st.caption(
        "Ask anything about revenue, orders, "
        "products, customers, reviews or deliveries."
    )


# ==================================================
# ANALYSIS
# ==================================================

if analyze:

    if question.strip():

        try:

            with st.status(
                "🤖 AI Analytics Assistant is working...",
                expanded=True
            ) as status:


                # --------------------------------------
                # STEP 1
                # --------------------------------------

                st.write(
                    "🧠 Understanding your question..."
                )


                # --------------------------------------
                # STEP 2 - GENERATE SQL
                # --------------------------------------

                sql = generate_sql(question)

                st.write(
                    "🔎 Generated PostgreSQL query..."
                )


                # --------------------------------------
                # STEP 3 - EXECUTE QUERY
                # --------------------------------------

                result = execute_query(sql)

                st.write(
                    "📊 Analyzing database results..."
                )


                # --------------------------------------
                # SAVE RESULTS
                # --------------------------------------

                st.session_state.last_sql = sql

                st.session_state.last_result = result

                st.session_state.last_question = question


                # --------------------------------------
                # SAVE HISTORY
                # --------------------------------------

                if (
                    question
                    not in st.session_state.history
                ):

                    st.session_state.history.append(
                        question
                    )


                # --------------------------------------
                # COMPLETE STATUS
                # --------------------------------------

                status.update(
                    label=(
                        "🎉 Analysis completed successfully!"
                    ),
                    state="complete",
                    expanded=False
                )


        except Exception as e:

            st.error(
                "❌ Something went wrong while "
                "analyzing your question."
            )

            st.exception(e)


    else:

        st.warning(
            "⚠️ Please enter a question first."
        )


# ==================================================
# DISPLAY RESULTS
# ==================================================

if st.session_state.last_result is not None:


    # ==============================================
    # GET SAVED DATA
    # ==============================================

    result = st.session_state.last_result

    sql = st.session_state.last_sql

    last_question = (
        st.session_state.last_question
    )


    st.markdown("---")


    # ==============================================
    # RESULT HEADER
    # ==============================================

    st.subheader(
        "🤖 Analysis Result"
    )


    if last_question:

        st.caption(
            f"Question: {last_question}"
        )


    # ==============================================
    # VALIDATE RESULT
    # ==============================================

    if (
        isinstance(result, pd.DataFrame)
        and not result.empty
    ):


        # ==========================================
        # CASE 1: SINGLE VALUE
        # ==========================================

        if (
            len(result) == 1
            and len(result.columns) == 1
        ):


            column_name = result.columns[0]

            value = result.iloc[0, 0]


            # --------------------------------------
            # FORMAT NAME
            # --------------------------------------

            display_name = (
                str(column_name)
                .replace("_", " ")
                .title()
            )


            # --------------------------------------
            # FORMAT VALUE
            # --------------------------------------

            formatted_value = format_number(
                value
            )


            # --------------------------------------
            # DISPLAY METRIC
            # --------------------------------------

            metric_col, empty_col = st.columns(
                [3, 7]
            )


            with metric_col:

                st.metric(
                    label=display_name,
                    value=formatted_value
                )


            # --------------------------------------
            # KEY INSIGHT
            # --------------------------------------

            st.markdown(
                "### 💡 Key Insight"
            )


            st.info(
                f"The analysis shows that "
                f"**{display_name.lower()}** "
                f"is **{formatted_value}**."
            )


        # ==========================================
        # CASE 2: MULTIPLE COLUMNS / RESULTS
        # ==========================================

        else:


            # --------------------------------------
            # RESULT COUNT
            # --------------------------------------

            st.info(
                f"📊 Found **{len(result)} result(s)** "
                f"based on your question."
            )


            # --------------------------------------
            # DETAILED RESULTS
            # --------------------------------------

            st.subheader(
                "📋 Detailed Results"
            )


            st.dataframe(
                result,
                use_container_width=True,
                hide_index=True
            )


            # ======================================
            # CREATE COPY FOR VISUALIZATION
            # ======================================

            chart_result = result.copy()


            # ======================================
            # DETECT NUMERIC COLUMNS
            # ======================================

            numeric_columns = get_numeric_columns(
                chart_result
            )


            # ======================================
            # DETECT CATEGORY COLUMNS
            # ======================================

            non_numeric_columns = [

                column

                for column
                in chart_result.columns

                if column
                not in numeric_columns

            ]


            # ======================================
            # DECIDE WHETHER GRAPH IS REQUIRED
            # ======================================

            show_chart = should_show_chart(
                chart_result,
                numeric_columns,
                non_numeric_columns
            )


            # ======================================
            # AUTOMATIC VISUALIZATION
            # ======================================

            if show_chart:


                # ----------------------------------
                # CHOOSE METRIC COLUMN
                # ----------------------------------

                y_column = numeric_columns[0]


                # ----------------------------------
                # CASE: CATEGORY / TIME COLUMN EXISTS
                # ----------------------------------

                if len(non_numeric_columns) >= 1:


                    x_column = (
                        non_numeric_columns[0]
                    )


                    # Prepare chart data

                    chart_data = chart_result[
                        [
                            x_column,
                            y_column
                        ]
                    ].copy()


                    # Remove missing values

                    chart_data = (
                        chart_data
                        .dropna()
                    )


                    # Chart needs at least 2 values

                    if len(chart_data) >= 2:


                        # Convert category to string

                        chart_data[x_column] = (
                            chart_data[x_column]
                            .astype(str)
                        )


                        # Set index

                        chart_data = (
                            chart_data
                            .set_index(x_column)
                        )


                        # Limit chart to 20 rows

                        chart_data = (
                            chart_data
                            .head(20)
                        )


                        # --------------------------------
                        # SHOW VISUALIZATION
                        # --------------------------------

                        st.markdown("---")

                        st.subheader(
                            "📈 Data Visualization"
                        )


                        # ------------------------------
                        # TIME DATA → LINE CHART
                        # ------------------------------

                        if is_time_column(x_column):


                            st.line_chart(
                                chart_data
                            )


                        # ------------------------------
                        # CATEGORY DATA → BAR CHART
                        # ------------------------------

                        else:


                            st.bar_chart(
                                chart_data
                            )


                # ----------------------------------
                # ONLY NUMERIC COLUMNS
                # ----------------------------------

                elif (
                    len(numeric_columns) >= 2
                ):


                    chart_data = chart_result[
                        numeric_columns
                    ].head(20)


                    if len(chart_data) >= 2:

                        st.markdown("---")

                        st.subheader(
                            "📈 Data Visualization"
                        )


                        st.line_chart(
                            chart_data
                        )


            # ======================================
            # QUICK INSIGHT
            # ======================================

            if (
                len(numeric_columns) >= 1
                and len(chart_result) > 0
            ):


                metric_column = (
                    numeric_columns[0]
                )


                # Convert safely

                metric_series = pd.to_numeric(
                    chart_result[
                        metric_column
                    ],
                    errors="coerce"
                )


                # Check valid values

                if metric_series.notna().any():


                    highest_index = (
                        metric_series.idxmax()
                    )


                    highest_value = (
                        metric_series.loc[
                            highest_index
                        ]
                    )


                    formatted_highest = (
                        format_number(
                            highest_value
                        )
                    )


                    st.markdown("---")

                    st.subheader(
                        "💡 Quick Insight"
                    )


                    # ----------------------------------
                    # CATEGORY + METRIC
                    # ----------------------------------

                    if len(non_numeric_columns) >= 1:


                        category_column = (
                            non_numeric_columns[0]
                        )


                        highest_category = (
                            chart_result.loc[
                                highest_index,
                                category_column
                            ]
                        )


                        st.info(
                            f"🏆 **{highest_category}** has "
                            f"the highest **"
                            f"{str(metric_column).replace('_', ' ')}"
                            f"** with a value of "
                            f"**{formatted_highest}**."
                        )


                    # ----------------------------------
                    # ONLY NUMERIC DATA
                    # ----------------------------------

                    else:


                        st.info(
                            f"📊 The highest value of "
                            f"**{str(metric_column).replace('_', ' ')}** "
                            f"is **{formatted_highest}**."
                        )


    # ==============================================
    # NO DATA
    # ==============================================

    else:

        st.warning(
            "📭 No data was found for this question."
        )


    # ==================================================
    # GENERATED SQL
    # ==================================================

    if sql:

        st.markdown("---")


        with st.expander(
            "🔎 View Generated SQL Query"
        ):

            st.code(
                sql,
                language="sql"
            )


    # ==================================================
    # DOWNLOAD RESULTS
    # ==================================================

    if (
        isinstance(result, pd.DataFrame)
        and not result.empty
    ):


        st.markdown("---")

        st.markdown(
            "### 📥 Export Results"
        )


        csv = result.to_csv(
            index=False
        ).encode("utf-8")


        st.download_button(
            label=(
                "📥 Download Results as CSV"
            ),
            data=csv,
            file_name=(
                "ecommerce_analysis.csv"
            ),
            mime="text/csv",
            type="primary"
        )


# ==================================================
# FOOTER
# ==================================================

st.markdown("---")


st.caption(
    "🤖 AI-Powered E-commerce Analytics Assistant | "
    "PostgreSQL + Ollama + Phi-3"
)