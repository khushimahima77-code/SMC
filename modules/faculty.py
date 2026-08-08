import streamlit as st
from database import supabase
import re

def show():
    st.header("👩‍🏫 Faculty Management")

    # --- Add Teacher Form ---
    name = st.text_input("Teacher Name")
    subject = st.text_input("Subject")
    email = st.text_input("Email")

    if st.button("Add Teacher"):
        if not name or not subject or not email:
            st.error("⚠️ Please fill all fields before adding a teacher.")
        elif not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            st.error("⚠️ Please enter a valid email address.")
        else:
            try:
                supabase.table("teachers").insert({
                    "name": name,
                    "subject": subject,
                    "email": email
                }).execute()
                st.success("✅ Teacher added successfully!")
                st.rerun()
            except Exception as e:
                st.error(f"Error: {e}")

    # --- Show All Teachers ---
    st.subheader("All Teachers")
    try:
        teachers = supabase.table("teachers").select("*").execute()
        if teachers.data:
            # --- Search/Filter ---
            search_query = st.text_input("🔍 Search teacher by name, subject, or email")
            if search_query:
                filtered = [
                    t for t in teachers.data
                    if search_query.lower() in str(t["name"]).lower()
                    or search_query.lower() in str(t["subject"]).lower()
                    or search_query.lower() in str(t["email"]).lower()
                ]
                st.dataframe(filtered)
            else:
                st.dataframe(teachers.data)

            # --- Delete Teacher Section ---
            teacher_options = {
                f"{t['id']} - {t['name']} ({t['subject']}) [{t['email']}]": t["id"]
                for t in teachers.data
            }
            delete_choice = st.selectbox("Select Teacher to delete", list(teacher_options.keys()))
            if st.button("Delete Teacher"):
                delete_id = teacher_options[delete_choice]
                try:
                    supabase.table("teachers").delete().eq("id", delete_id).execute()
                    st.success(f"🗑️ Teacher '{delete_choice}' deleted successfully!")
                    st.rerun()
                except Exception as e:
                    st.error(f"Error deleting teacher: {e}")

            # --- Update Teacher Section ---
            st.subheader("✏️ Update Teacher Details")
            update_choice = st.selectbox("Select Teacher to update", list(teacher_options.keys()))
            update_id = teacher_options[update_choice]

            new_name = st.text_input("New Name")
            new_subject = st.text_input("New Subject")
            new_email = st.text_input("New Email")

            if st.button("Update Teacher"):
                if not new_name or not new_subject or not new_email:
                    st.error("⚠️ Please fill all fields before updating.")
                elif not re.match(r"[^@]+@[^@]+\.[^@]+", new_email):
                    st.error("⚠️ Please enter a valid email address.")
                else:
                    try:
                        supabase.table("teachers").update({
                            "name": new_name,
                            "subject": new_subject,
                            "email": new_email
                        }).eq("id", update_id).execute()
                        st.success(f"✅ Teacher '{update_choice}' updated successfully!")
                        st.rerun()
                    except Exception as e:
                        st.error(f"Error updating teacher: {e}")

        else:
            st.info("No teachers found.")
    except Exception as e:
        st.error(f"Error fetching teachers: {e}")
