from llm_service import generate_sql
from database import execute_query


question = "What is the total revenue?"

# Step 1: Generate SQL using Phi-3
sql = generate_sql(question)

print("\nGenerated SQL:")
print(sql)


# Step 2: Execute SQL on PostgreSQL
result = execute_query(sql)

print("\nQuery Result:")
print(result)