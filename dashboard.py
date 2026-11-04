import streamlit as st
import pandas as pd
from sqlalchemy import create_engine
from urllib.parse import quote_plus

# ---------- Page Set-Up ----------
st.set_page_config(page_title="NextGenLearners Program Dashboard", layout="wide")
st.title("NextGenLearners Program Performance Dashboard")
st.caption("Practice dashboard built on sample data. Use the domain filter in the sidebar to explore one program at a time.")

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

# MySQL returns scores as exact decimals; convert them to normal numbers so we can average them
scores["score"] = scores["score"].astype(float)

# ---------- Domain Filter ----------
st.sidebar.header("Filter")
domain_list = ["All"] + sorted(applicants["domain"].unique().tolist())
selected_domain = st.sidebar.selectbox("Filter by Domain", domain_list)

if selected_domain != "All":
    applicants_f = applicants[applicants["domain"] == selected_domain]
    interns_f = interns[interns["domain"] == selected_domain]
    scores_f = scores[scores["domain"] == selected_domain]
else:
    applicants_f, interns_f, scores_f = applicants, interns, scores

st.subheader(f"Showing: {selected_domain} Domain" if selected_domain != "All" else "Showing: All Domains")

# ---------- Element 1: Funnel ----------
st.subheader("1. Program Funnel")
st.caption("How many people applied, how many were selected as interns, and how many finished the program.")
total_applicants = len(applicants_f)
total_interns = len(interns_f)
total_completed = int((interns_f["completion_status"] == "Completed").sum())

col1, col2, col3 = st.columns(3)
col1.metric("Total Applicants", total_applicants)
col2.metric("Total Interns", total_interns)
col3.metric("Completed Interns", total_completed)

# ---------- Elements 2 and 3: Charts ----------
left, right = st.columns(2)

with left:
    st.subheader("2. Completion Rate per Domain")
    st.caption("Completed interns as a percentage of all applicants (same logic as Query 4).")
    applicants_by_domain = applicants_f.groupby("domain").size()
    completed_by_domain = (
        interns_f[interns_f["completion_status"] == "Completed"]
        .groupby("domain").size()
        .reindex(applicants_by_domain.index, fill_value=0)
    )
    completion_rate = (100.0 * completed_by_domain / applicants_by_domain).round(2)
    completion_df = completion_rate.rename("completion_rate_pct").reset_index()
    st.bar_chart(completion_df, x="domain", y="completion_rate_pct", sort="-completion_rate_pct")

with right:
    st.subheader("3. Average Hackathon Score per Domain")
    st.caption("Average score of interns who took the hackathon (same logic as Query 2).")
    avg_score = scores_f.groupby("domain")["score"].mean().round(2).rename("avg_score").reset_index()
    st.bar_chart(avg_score, x="domain", y="avg_score", sort="-avg_score")

# ---------- Element 4: Leaderboard ----------
st.subheader("4. Top 10 Performers")
st.caption("The ten highest hackathon scores (same logic as Query 3, without the 85 threshold).")
leaderboard = (
    scores_f
    .merge(interns[["intern_id", "applicant_id"]], on="intern_id")
    .merge(applicants[["applicant_id", "name", "university"]], on="applicant_id")
    .sort_values("score", ascending=False)
    .head(10)[["intern_id", "name", "domain", "university", "score"]]
    .reset_index(drop=True)
)
leaderboard.index = leaderboard.index + 1      # rank starts at 1, not 0
st.dataframe(leaderboard)

# ---------- Raw Data Check ----------
with st.expander("Preview the Raw Data"):
    st.write("Applicants")
    st.dataframe(applicants.head())
    st.write("Interns")
    st.dataframe(interns.head())
    st.write("Hackathon Scores")
    st.dataframe(scores.head())