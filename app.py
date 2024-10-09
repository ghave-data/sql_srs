# pylint: disable=missing-module-docstring
import logging
import os
from datetime import date, timedelta

import duckdb
import streamlit as st

if "data" not in os.listdir():
    logging.debug(os.listdir())
    logging.debug("creating folder data")
    os.mkdir("data")

if "exercises_sql_tables.duckdb" not in os.listdir("data"):
    exec(open("init_db.py").read())

con = duckdb.connect(database="data/exercises_sql_tables.duckdb", read_only=False)


def check_users_solution(user_query: str):
    """
    Checks that user query is correct by:
    1) checking the columns
    2) checking the rows
    :param user_query: a string containing a query inserted by the user
    :return: succession of action testing the input
    """
    result = con.execute(user_query).df()
    st.dataframe(result)
    if len(result.columns) != len(solution_df.columns):
        st.write("Some columns are missing")
    try:
        result = result[solution_df.columns]
        st.dataframe(result.compare(solution_df))
        if result.compare(solution_df).shape == (0, 0):
            st.write("Correct !")
    except KeyError as e:
        st.write("Some columns are missing")
    n_lines_difference = result.shape[0] - solution_df.shape[0]
    if n_lines_difference != 0:
        st.write(
            f"result has a {n_lines_difference} lines difference with the solution_df"
        )


with st.sidebar:
    available_theme_df = con.execute("SELECT DISTINCT theme FROM memory_state").df()
    theme = st.selectbox(
        "How would you like to review?",
        available_theme_df["theme"].unique(),
        index=None,
        placeholder="Select contact method...",
    )

    if theme:
        st.write(f"You selected {theme}")
        SELECT_EXERCISE_QUERY = f"SELECT * FROM memory_state WHERE theme = '{theme}'"
    else:
        SELECT_EXERCISE_QUERY = "SELECT * FROM memory_state"

    exercise = (
        con.execute(SELECT_EXERCISE_QUERY)
        .df()
        .sort_values("last_reviewed")
        .reset_index(drop=True)
    )
    st.write(exercise)
    exercise_name = exercise.loc[0, "exercise_name"]
    with open(f"answers/{exercise_name}.sql", "r", encoding="UTF-8") as f:
        answer = f.read()

    solution_df = con.execute(answer).df()

st.header("Enter your code:")
query = st.text_area(label="your SQL code here", key="user_input")

if query:
    check_users_solution(query)

for n_days in [2, 7, 21]:
    if st.button(f"test back in {n_days} days"):
        next_review = date.today() + timedelta(days=n_days)
        con.execute(
            f"UPADATE memory_state SET last_reviewed = '{next_review}'"
            f"WHERE exercise_name = '{exercise_name}"
        )
        st.rerun()

if st.button("Reset"):
    con.execute("UPDATE memory_state SET last_reviewed = '1970-01-01'")

tab1, tab2 = st.tabs(["Tables", "Solutions"])

with tab1:
    exercise_tables = exercise.loc[0, "tables"]
    for table in exercise_tables:
        st.write(f"Table: {table}")
        df_table = con.execute(f"SELECT * FROM {table}").df()
        st.dataframe(df_table)
    st.write("Expected result:")
    st.dataframe(solution_df)

with tab2:
    st.write(answer)
