import streamlit as st
from database import supabase

def show():
    st.header("📝 Attendance Management")

    # --- Student ID Input ---
    student_id = st.text_input("Enter Student ID")

    if student_id:
        try:
            # Fetch student details
            student = supabase.table("students").select("*").eq("id", int(student_id)).execute()
            if student.data:
                s = student.data[0]
                st.subheader("👩‍🎓 Student Details")
                st.write(f"**Name:** {s['name']}")
                st.write(f"**Class:** {s['class']}")
                st.write(f"**Email:** {s['email']}")

                # Fetch attendance records for this student
                attendance = supabase.table("attendance").select("*").eq("student_id", int(student_id)).execute()
                st.subheader("📑 Attendance Records")
                if attendance.data:
                    joined_data = [
                        {
                            "Status": a["status"],   # Attendance ID की जगह Status दिखेगा
                            "Student ID": a["student_id"],
                            "Name": s["name"],
                            "Class": s["class"],
                            "Email": s["email"],
                            "Date": a["date"],
                            "Created At": a["created_at"]
                        }
                        for a in attendance.data
                    ]
                    st.dataframe(joined_data)
                else:
                    st.info("No attendance records found for this student.")
            else:
                st.error("⚠️ Student not found.")
        except Exception as e:
            st.error(f"Error fetching student details: {e}")

    # --- Add Attendance Form ---
    st.subheader("➕ Add Attendance Record")
    date = st.date_input("Date")
    status = st.selectbox("Status", ["Present", "Absent"])

    if st.button("Add Attendance"):
        if not student_id or not status:
            st.error("⚠️ Please fill all fields before adding attendance record.")
        else:
            try:
                supabase.table("attendance").insert({
                    "student_id": int(student_id),
                    "date": str(date),
                    "status": status
                }).execute()
                st.success("✅ Attendance record added successfully!")
                st.rerun()
            except Exception as e:
                st.error(f"Error: {e}")
