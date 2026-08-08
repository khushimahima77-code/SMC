import streamlit as st
from database import supabase

def show():
    st.header("🎓 Academy")
    st.write("Manage courses, subjects, and academic programs here.")

    # --- Add Course Form ---
    st.subheader("➕ Add New Course")
    course_name = st.text_input("Course Name")
    description = st.text_area("Description")

    if st.button("Add Course"):
        if not course_name:
            st.error("⚠️ Please enter course name.")
        else:
            try:
                supabase.table("courses").insert({
                    "name": course_name,
                    "description": description
                }).execute()
                st.success("✅ Course added successfully!")
                st.rerun()
            except Exception as e:
                st.error(f"Error: {e}")

    # --- Show All Courses ---
    st.subheader("📑 All Courses")
    try:
        courses = supabase.table("courses").select("*").execute()
        if courses.data:
            st.dataframe(courses.data)
        else:
            st.info("No courses found.")
    except Exception as e:
        st.error(f"Error fetching courses: {e}")

    # --- Assign Course to Student ---
    st.subheader("👩‍🎓 Assign Course to Student")
    student_id = st.text_input("Student ID")
    course_id = st.text_input("Course ID")

    if st.button("Assign Course"):
        if not student_id or not course_id:
            st.error("⚠️ Please enter both Student ID and Course ID.")
        else:
            try:
                supabase.table("student_courses").insert({
                    "student_id": int(student_id),
                    "course_id": int(course_id)
                }).execute()
                st.success("✅ Course assigned to student successfully!")
            except Exception as e:
                st.error(f"Error: {e}")

    # --- Show Student-Course Assignments ---
    st.subheader("📘 Student Course Assignments")
    try:
        assignments = supabase.table("student_courses").select("*").execute()
        if assignments.data:
            joined_data = []
            for a in assignments.data:
                student = supabase.table("students").select("*").eq("id", a["student_id"]).execute().data[0]
                course = supabase.table("courses").select("*").eq("id", a["course_id"]).execute().data[0]
                joined_data.append({
                    "Student Name": student["name"],
                    "Class": student["class"],
                    "Email": student["email"],
                    "Course Name": course["name"],
                    "Description": course["description"]
                })
            st.dataframe(joined_data)
        else:
            st.info("No student-course assignments found.")
    except Exception as e:
        st.error(f"Error fetching assignments: {e}")
