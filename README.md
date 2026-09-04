# AI-Powered E-Commerce Analytics Assistant

An end-to-end data analytics project that combines **Python, SQL, Power BI, and Generative AI** to analyze e-commerce business data and generate insights from natural-language questions.

## Project Overview

This project analyzes e-commerce data across multiple business areas, including:

- Sales and Revenue
- Customers
- Products and Categories
- Payments
- Order Status
- Customer Reviews
- Delivery Performance
- Regional Sales

The project also includes an **AI-powered analytics assistant** that allows users to ask questions in natural language and receive data-driven insights through AI-generated SQL queries.

---

## Key Features

### Data Analysis
- Data cleaning and preprocessing using Python
- Exploratory data analysis
- Customer analysis
- Product and category performance analysis
- Sales and revenue analysis
- Payment analysis
- Customer review analysis
- Delivery performance analysis

### SQL Analysis
SQL queries were used to analyze key business metrics and relationships within the e-commerce dataset.

### AI Analytics Assistant
The application includes an AI-powered analytics assistant that:

- Accepts natural-language questions
- Generates SQL queries using a local LLM
- Retrieves relevant data from the analytics dataset
- Displays insights and visualizations

The application uses **Ollama** with the `phi3:mini` model for local AI-powered SQL generation.

### Power BI Dashboard

An interactive Power BI dashboard was developed to visualize key business metrics and trends.

The dashboard includes:

- Total Revenue
- Total Orders
- Total Customers
- Average Delivery Days
- Monthly Revenue Trends
- Top Product Categories by Revenue
- Top States by Revenue
- Order Status Distribution
- Payment Type Distribution
- Order Date Filters

Power BI files are available in the [`powerbi`](./powerbi) folder.

> **Note:** If the `.pbix` file does not open on your Power BI Desktop version, please refer to the **PDF dashboard preview** available in the same `powerbi` folder. This allows the complete dashboard and its visualizations to be viewed without opening the Power BI file.

---

## 🛠️ Technologies Used

- **Python**
- **Pandas**
- **SQL**
- **Power BI**
- **Streamlit**
- **Ollama**
- **Phi-3 Mini**
- **Git & GitHub**

---

## Project Structure

```text
AI-Ecommerce-Analytics-Assistant/
│
├── data/
│   ├── processed/
│   └── e-commerce datasets
│
├── llm_analytics_assistant/
│   ├── app.py
│   ├── database.py
│   ├── llm_service.py
│   └── requirements.txt
│
├── powerbi/
│   ├── Dashboard_Final_v3.pbix
│   ├── Dashboard_Final.pdf
│   └── README.md
│
├── python/
│   ├── data_cleaning.py
│   ├── sales_analysis.py
│   ├── customer_analysis.py
│   ├── product_analysis.py
│   └── other analytical scripts
│
├── sql/
│   └── ecommerce_analysis.sql
│
└── README.md
