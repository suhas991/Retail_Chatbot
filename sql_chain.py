from langchain_core.runnables import RunnablePassthrough
from langchain_groq import ChatGroq
from langchain_community.utilities import SQLDatabase  # Updated import
from langchain.prompts import PromptTemplate
import re
import os
import urllib.parse

# Initialize the Groq LLM and database
password = urllib.parse.quote(os.getenv("DB_PASSWORD", "Suhas@123"))
db = SQLDatabase.from_uri(f"mysql+mysqlconnector://root:{password}@localhost:3306/global_tshirts")

llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    groq_api_key="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"
)

# Prompt for Pure SQL Output
sql_prompt = PromptTemplate(
    input_variables=["schema", "question"],
    template="""\
Given the following schema:
{schema}

Answer the user's question by providing only the SQL query. Do not include any additional explanation or formatting.

Question: {question}
SQL Query:
"""
)

# Helper Function to Extract SQL Query
def extract_sql(output):
    if hasattr(output, "content"):  # For AIMessage objects
        output = output.content
    match = re.search(r"```sql\n(.*?)\n```", output, re.DOTALL)
    if not match:
        match = re.search(r"(SELECT .*?);", output, re.DOTALL)
    return match.group(1).strip() if match else output.strip()

# SQL Chain Using Groq
def generate_sql_query(user_question):
    sql_chain = (
        RunnablePassthrough.assign(schema=lambda vars: db.get_table_info())
        | sql_prompt
        | llm.bind(stop=["\n"])
        | (lambda output: extract_sql(output))  # Output only the SQL query as a string
    )
    
    return sql_chain.invoke({"question": user_question})
