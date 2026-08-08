import streamlit as st
from database import supabase

def show():
    st.header("⚙️ Settings")
    st.write("Manage system settings and configurations here.")

    # --- Add / Update Setting ---
    st.subheader("Add / Update Setting")
    key = st.text_input("Setting Key")
    value = st.text_input("Setting Value")
    if st.button("Save Setting"):
        if key and value:
            # Upsert ensures: if key exists → update, else → insert
            supabase.table("settings").upsert({"key": key, "value": value}).execute()
            st.success(f"Setting '{key}' saved successfully!")
        else:
            st.warning("Please enter both key and value.")

    st.markdown("---")

    # --- Display all settings ---
    st.subheader("All Settings")
    try:
        settings = supabase.table("settings").select("*").execute()
        if settings.data:
            st.dataframe(settings.data)
        else:
            st.info("No settings found.")
    except Exception as e:
        st.error(f"Error fetching settings: {e}")
