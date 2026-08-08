import streamlit as st
from database import supabase
import pandas as pd
import plotly.express as px

def show():
    st.header("📊 School Dashboard")

    # Fetch data
    students = supabase.table("students").select("*").execute().data
    teachers = supabase.table("teachers").select("*").execute().data
    fees = supabase.table("fees").select("*").execute().data
    attendance = supabase.table("attendance").select("*").execute().data

    # Top metrics
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("👩‍🎓 Students", len(students))
    col2.metric("👩‍🏫 Teachers", len(teachers))
    col3.metric("💰 Fees Records", len(fees))
    col4.metric("📅 Attendance Records", len(attendance))

    st.markdown("---")

    # Attendance chart
    if attendance:
        df_attendance = pd.DataFrame(attendance)
        fig_attendance = px.histogram(df_attendance, x="status", color="status",
                                      title="Attendance Distribution")
        st.plotly_chart(fig_attendance, use_container_width=True)

    # Fees chart
    if fees:
        df_fees = pd.DataFrame(fees)
        fig_fees = px.pie(df_fees, names="status", title="Fees Status")
        st.plotly_chart(fig_fees, use_container_width=True)

    # Students by class
    if students:
        df_students = pd.DataFrame(students)
        fig_students = px.bar(df_students, x="class", title="Students per Class")
        st.plotly_chart(fig_students, use_container_width=True)

    st.info("📌 Tip: Use sidebar to navigate to Admissions, Faculty, Finance, and other modules.")
