import streamlit as st
from database import supabase
from modules import overview, admissions, faculty, presence, finance, bookhub, academy, reports, notices, settings

# ---------------- AUTH MODULE ----------------
def login_signup():
    st.sidebar.header("🔑 Authentication")
    option = st.sidebar.radio("Choose", ["Login", "Signup"])

    email = st.sidebar.text_input("Email")
    password = st.sidebar.text_input("Password", type="password")

    if option == "Signup":
        if st.sidebar.button("Signup"):
            try:
                supabase.auth.sign_up({"email": email, "password": password})
                st.success("Signup successful! Please login.")
            except Exception as e:
                st.error(f"Error: {e}")

    if option == "Login":
        if st.sidebar.button("Login"):
            try:
                user = supabase.auth.sign_in_with_password({"email": email, "password": password})
                if user and user.user:
                    st.session_state["user"] = user.user
                    st.success("Login successful! Redirecting to dashboard...")
                    st.session_state["menu"] = "Overview"   # default dashboard
                    st.rerun()   # refresh app state
                else:
                    st.error("Invalid credentials")
            except Exception as e:
                st.error(f"Error: {e}")

# ---------------- MAIN APP ----------------
st.title("🏫 School Management Console")

if "user" not in st.session_state:
    login_signup()
else:
    # Logout button
    if st.sidebar.button("Logout"):
        st.session_state.clear()
        st.rerun()

    # Sidebar menu
    menu = st.sidebar.selectbox("Menu", [
        "Overview", "Admissions", "Faculty", "Presence", "Finance",
        "BookHub", "Academy", "Reports", "Notices", "Settings"
    ], index=["Overview", "Admissions", "Faculty", "Presence", "Finance",
            "BookHub", "Academy", "Reports", "Notices", "Settings"].index(
                st.session_state.get("menu", "Overview")
            ))

    st.session_state["menu"] = menu

    # Show selected module
    if menu == "Overview":
        overview.show()
    elif menu == "Admissions":
        admissions.show()
    elif menu == "Faculty":
        faculty.show()
    elif menu == "Presence":
        presence.show()
    elif menu == "Finance":
        finance.show()
    elif menu == "BookHub":
        bookhub.show()
    elif menu == "Academy":
        academy.show()
    elif menu == "Reports":
        reports.show()
    elif menu == "Notices":
        notices.show()
    elif menu == "Settings":
        settings.show()
