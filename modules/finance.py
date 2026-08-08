import streamlit as st
from database import supabase

def show():
    st.header("💰 Finance Management (Fees)")

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

                # Fetch fees for this student
                fees = supabase.table("fees").select("*").eq("student_id", int(student_id)).execute()
                st.subheader("📑 Fee Records")
                if fees.data:
                    # Show joined view (student info + fee info)
                    joined_data = [
                        {
                            "Fee ID": f["id"],
                            "Student ID": f["student_id"],
                            "Name": s["name"],
                            "Class": s["class"],
                            "Email": s["email"],
                            "Amount": f["amount"],
                            "Status": f["status"],
                            "Due Date": f["due_date"],
                            "Created At": f["created_at"]
                        }
                        for f in fees.data
                    ]
                    st.dataframe(joined_data)
                else:
                    st.info("No fee records found for this student.")
            else:
                st.error("⚠️ Student not found.")
        except Exception as e:
            st.error(f"Error fetching student details: {e}")

    # --- Add Fee Form ---
    st.subheader("➕ Add Fee Record")
    amount = st.text_input("Amount")
    status = st.selectbox("Status", ["Paid", "Pending"])
    due_date = st.date_input("Due Date")

    if st.button("Add Fee"):
        if not student_id or not amount or not status:
            st.error("⚠️ Please fill all fields before adding fee record.")
        else:
            try:
                supabase.table("fees").insert({
                    "student_id": int(student_id),
                    "amount": float(amount),
                    "status": status,
                    "due_date": str(due_date)
                }).execute()
                st.success("✅ Fee record added successfully!")
                st.rerun()
            except Exception as e:
                st.error(f"Error: {e}")
