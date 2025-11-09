# Filename: student_productivity_hub.py
import streamlit as st
import pandas as pd
import pickle
from datetime import date, datetime
import plotly.express as px
import random

# -------------------------------
# Data Persistence
# -------------------------------
DATA_FILE = "student_data.pkl"

def load_data():
    try:
        with open(DATA_FILE, "rb") as f:
            return pickle.load(f)
    except:
        return {"assignments": [], "study_sessions": []}

def save_data(data):
    with open(DATA_FILE, "wb") as f:
        pickle.dump(data, f)

data = load_data()

# -------------------------------
# App Settings
# -------------------------------
st.set_page_config(page_title="Student Productivity & Assignment Hub", layout="wide")
st.title("🎓 Student Productivity & Assignment Hub")

# -------------------------------
# Section 1: Add Assignment
# -------------------------------
st.header("📝 Add New Assignment")
with st.form("assignment_form"):
    subject = st.text_input("Subject")
    title = st.text_input("Assignment Title")
    description = st.text_area("Description")
    due_date = st.date_input("Due Date")
    priority = st.selectbox("Priority", ["High", "Medium", "Low"])
    submitted = st.form_submit_button("Add Assignment")
    
    if submitted:
        data["assignments"].append({
            "subject": subject,
            "title": title,
            "description": description,
            "due_date": due_date.strftime("%Y-%m-%d"),
            "priority": priority,
            "status": "Pending"
        })
        save_data(data)
        st.success("Assignment added successfully!")

# -------------------------------
# Section 2: Assignment Dashboard
# -------------------------------
st.header("📊 Assignment Dashboard")
if data["assignments"]:
    df = pd.DataFrame(data["assignments"])
    df['Days Left'] = df['due_date'].apply(lambda x: (datetime.strptime(x, "%Y-%m-%d").date() - date.today()).days)
    
    st.dataframe(df)
    
    # Plot: Workload by Subject
    workload = df.groupby("subject").size().reset_index(name="Assignments")
    fig1 = px.bar(workload, x="subject", y="Assignments", title="Assignments by Subject")
    st.plotly_chart(fig1, use_container_width=True)
    
    # Plot: Pending vs Completed
    status_counts = df['status'].value_counts().reset_index()
    status_counts.columns = ["Status", "Count"]
    fig2 = px.pie(status_counts, names="Status", values="Count", title="Assignment Status")
    st.plotly_chart(fig2, use_container_width=True)

# -------------------------------
# Section 3: Study Planner
# -------------------------------
st.header("📅 Study Planner")
with st.form("study_form"):
    study_subject = st.text_input("Subject for Study")
    study_topic = st.text_input("Topic / Assignment")
    study_date = st.date_input("Planned Date")
    study_duration = st.number_input("Duration (hours)", min_value=0.5, max_value=12.0, step=0.5)
    add_study = st.form_submit_button("Add Study Session")
    
    if add_study:
        data["study_sessions"].append({
            "subject": study_subject,
            "topic": study_topic,
            "date": study_date.strftime("%Y-%m-%d"),
            "duration": study_duration
        })
        save_data(data)
        st.success("Study session added!")

# Display study sessions
if data["study_sessions"]:
    st.subheader("Your Planned Study Sessions")
    df_study = pd.DataFrame(data["study_sessions"])
    st.dataframe(df_study)
    fig3 = px.bar(df_study, x="date", y="duration", color="subject", title="Study Duration by Date")
    st.plotly_chart(fig3, use_container_width=True)

# -------------------------------
# Section 4: Motivational Tip
# -------------------------------
st.header("💡 Daily Motivation")
tips = [
    "Break big tasks into small, manageable steps.",
    "Focus on one assignment at a time.",
    "Take short breaks between study sessions.",
    "Plan ahead to avoid last-minute stress.",
    "Consistency beats intensity — study regularly."
]
st.info(random.choice(tips))
