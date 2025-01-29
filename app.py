import streamlit as st
from database_connection import test_db_connection, run_query
from sql_chain import generate_sql_query

# Set the title of the web page
st.title("Retail Chatbot")

# Input for user question
user_question = st.text_input("Ask your question:", "")

if user_question:
    try:
        # Generate the SQL query using Groq LLM
        sql_query = generate_sql_query(user_question)
        st.write(f"Generated SQL Query: {sql_query}")

        # Execute the SQL query
        query_result = run_query(sql_query)
        
        # If query_result is a list of tuples, format it properly
        if query_result:
            query_result = query_result[0][0]  # Extract the first value if it's a single result
        st.write("Query Result:", query_result)

    except Exception as e:
        st.error(f"Error: {e}")
