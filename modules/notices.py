import streamlit as st
from database import supabase

def show():
    st.header("📢 Notices")

    # --- Add new notice ---
    with st.form("notice_form"):
        title = st.text_input("Title")
        message = st.text_area("Message")
        submitted = st.form_submit_button("Publish")
        if submitted:
            if title and message:
                supabase.table("notices").insert({
                    "title": title,
                    "message": message
                }).execute()
                st.success("Notice published successfully!")
            else:
                st.warning("Please fill in both fields.")

    st.markdown("---")

    # --- Display all notices ---
    st.subheader("All Notices")
    try:
        response = supabase.table("notices").select("*").order("created_at", desc=True).execute()
        if response.data:
            for notice in response.data:
                st.markdown(f"### 📌 {notice['title']}")
                st.write(notice['message'])
                st.caption(f"Published on {notice['created_at']}")
                st.markdown("---")
        else:
            st.info("No notices yet.")
    except Exception as e:
        st.error(f"Error fetching notices: {e}")
