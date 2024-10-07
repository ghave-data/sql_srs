import streamlit as st
import pandas as pd
import duckdb
import io

csv = '''
beverage,price
orange juice,2.5
Expresso,2
Tea,3
'''

beverages = pd.read_csv(io.StringIO(csv))

csv2 = '''
food_item,price
cookie,2.5
chocolatine,2
muffin,3
'''

food_items = pd.read_csv(io.StringIO(csv2))

answer = """
SELECT * FROM beverages
CROSS JOIN food_items
"""

solution = duckdb.sql(answer)

st.header("Enter your code:")
query = st.text_area(label="your SQL code here", key="user_input")
if query:
    result = duckdb.sql(query)
    st.dataframe(result)

tab1, tab2 = st.tabs(["Tables","Solutions"])

with tab1:
    st.write("table: beverages")
    st.dataframe(beverages)
    st.write("table: food_items")
    st.dataframe(food_items)
    st.write("expected:")
    st.dataframe(solution)

with tab2:
    st.write(answer)