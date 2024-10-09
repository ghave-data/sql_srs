# pylint: disable=missing-module-docstring
import duckdb
import streamlit as st
import ast

con = duckdb.connect(database="data/exercises_sql_tables.duckdb", read_only=False)

#solution_df = duckdb.sql(ANSWER_STRING).df()

with st.sidebar:
    theme = st.selectbox(
        "How would you like to review?",
        ("cross_joins", "GroupBy", "window_functions"),
        index=None,
        placeholder="Select contact method...",
    )

    st.write("You selected:", theme)

    exercise = con.execute(f"SELECT * FROM memory_state WHERE theme = '{theme}'").df()
    st.write(exercise)

st.header("Enter your code:")
query = st.text_area(label="your SQL code here", key="user_input")

if query:
    result = con.execute(query).df()
    st.dataframe(result)
    """
    if len(result.columns) != len(solution_df.columns):
        st.write("Some columns are missing")

    try:
        result = result[solution_df.columns]
        st.dataframe(result.compare(solution_df))
    except KeyError as e:
        st.write("Some columns are missing")

    n_lines_difference = result.shape[0] - solution_df.shape[0]
    if n_lines_difference != 0:
        st.write(
            f"result has a {n_lines_difference} lines difference with the solution_df"
        )
"""
tab1, tab2 = st.tabs(["Tables", "Solutions"])

with tab1:
    exercise_tables = ast.literal_eval(exercise.loc[0, "tables"])
    for table in exercise_tables:
        st.write(f"table: {table}")
        df_table = con.execute(f"SELECT * FROM {table}").df()
        st.dataframe(df_table)

with tab2:
    ANSWER_STRING = exercise.loc[0, "exercise_name"]
    with open(f"answers/{ANSWER_STRING}.sql", "r") as f:
        answer = f.read()
    st.write(answer)