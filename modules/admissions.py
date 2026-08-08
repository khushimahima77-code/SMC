import streamlit as st
from database import supabase
import re

def show():
    st.header("🎓 Student Admissions Management")

    # --- Add Student Form ---
    name = st.text_input("Student Name")
    student_class = st.text_input("Class/Grade")
    email = st.text_input("Email")

    if st.button("Add Student"):
        if not name or not student_class or not email:
            st.error("⚠️ Please fill all fields before adding student.")
        elif not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            st.error("⚠️ Please enter a valid email address.")
        else:
            try:
                supabase.table("students").insert({
                    "name": name,
                    "class": student_class,
                    "email": email
                }).execute()
                st.success("✅ Student added successfully!")
                st.rerun()
            except Exception as e:
                st.error(f"Error: {e}")

    # --- Show All Students ---
    st.subheader("All Students")
    try:
        students = supabase.table("students").select("*").execute()
        if students.data:
            # --- Search/Filter ---
            search_query = st.text_input("🔍 Search by name, class, or email")
            if search_query:
                filtered = [
                    s for s in students.data
                    if search_query.lower() in str(s["name"]).lower()
                    or search_query.lower() in str(s["class"]).lower()
                    or search_query.lower() in str(s["email"]).lower()
                ]
                st.dataframe(filtered)
            else:
                st.dataframe(students.data)

            # --- Delete Student Section ---
            student_options = {
                f"{s['id']} - {s['name']} (Class: {s['class']}) [{s['email']}]": s["id"]
                for s in students.data
            }
            delete_choice = st.selectbox("Select Student to delete", list(student_options.keys()))
            if st.button("Delete Student"):
                delete_id = student_options[delete_choice]
                try:
                    supabase.table("students").delete().eq("id", delete_id).execute()
                    st.success(f"🗑️ Student '{delete_choice}' deleted successfully!")
                    st.rerun()
                except Exception as e:
                    st.error(f"Error deleting student: {e}")

            # --- Update Student Section ---
            st.subheader("✏️ Update Student Details")
            update_choice = st.selectbox("Select Student to update", list(student_options.keys()))
            update_id = student_options[update_choice]

            new_name = st.text_input("New Student Name")
            new_class = st.text_input("New Class/Grade")
            new_email = st.text_input("New Email")

            if st.button("Update Student"):
                if not new_name or not new_class or not new_email:
                    st.error("⚠️ Please fill all fields before updating.")
                elif not re.match(r"[^@]+@[^@]+\.[^@]+", new_email):
                    st.error("⚠️ Please enter a valid email address.")
                else:
                    try:
                        supabase.table("students").update({
                            "name": new_name,
                            "class": new_class,
                            "email": new_email
                        }).eq("id", update_id).execute()
                        st.success(f"✅ Student '{update_choice}' updated successfully!")
                        st.rerun()
                    except Exception as e:
                        st.error(f"Error updating student: {e}")

        else:
            st.info("No students found.")
    except Exception as e:
        st.error(f"Error fetching students: {e}")
