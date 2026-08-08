import streamlit as st
from database import supabase

def show():
    st.header("📑 Reports")
    st.write("Generate reports for Students, Attendance, Fees, etc.")

    students = supabase.table("students").select("*").execute()
    attendance = supabase.table("attendance").select("*").execute()
    fees = supabase.table("fees").select("*").execute()

    st.subheader("Students Report")
    st.dataframe(students.data)

    st.subheader("Attendance Report")
    st.dataframe(attendance.data)

    st.subheader("Fees Report")
    st.dataframe(fees.data)
