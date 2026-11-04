import streamlit as st
import pandas as pd
from sqlalchemy import create_engine
from urllib.parse import quote_plus

# ---------- Page Set-Up ----------
st.set_page_config(page_title="NextGenLearners Program Dashboard", layout="wide")
st.title("NextGenLearners Program Performance Dashboard")
st.caption("Practice dashboard built on sample data. Day 5: connect to MySQL and load the three tables.")

# ---------- Database Connection ----------
st.sidebar.header("Database Connection")
password = st.sidebar.text_input("MySQL password", type="password")

if not password:
    st.info("Enter your MySQL password in the sidebar to load the data.")
    st.stop()


@st.cache_resource
def get_engine(pw):
    """Build the connection to the nextgen database once and reuse it."""
    return create_engine(f"mysql+pymysql://root:{quote_plus(pw)}@localhost:3306/nextgen")


@st.cache_data
def load_table(table_name, _engine):
    """Read one whole table from MySQL and remember the result."""
    return pd.read_sql(f"SELECT * FROM {table_name};", _engine)


try:
    engine = get_engine(password)
    applicants = load_table("applicants", engine)
    interns = load_table("interns", engine)
    scores = load_table("hackathon_scores", engine)
except Exception as error:
    st.error("Could not load the data. Check that MySQL is running and the password is correct.")
    st.caption(str(error)[:200])
    st.stop()

# ---------- Data Check ----------
st.subheader("Data Check")
col1, col2, col3 = st.columns(3)
col1.metric("Applicants", len(applicants))
col2.metric("Interns", len(interns))
col3.metric("Hackathon Scores", len(scores))

with st.expander("Preview the Data"):
    st.write("Applicants")
    st.dataframe(applicants.head())
    st.write("Interns")
    st.dataframe(interns.head())
    st.write("Hackathon Scores")
    st.dataframe(scores.head())