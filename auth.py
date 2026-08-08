import streamlit as st
from database import supabase

def login_signup():
    st.sidebar.header("🔑 Authentication")
    option = st.sidebar.radio("Choose", ["Login", "Signup"])

    # Callback functions (set flag only)
    def do_signup():
        st.session_state["auth_action"] = "signup"

    def do_login():
        st.session_state["auth_action"] = "login"

    # Inputs with Enter key trigger
    st.sidebar.text_input("Email", key="email")
    st.sidebar.text_input(
        "Password",
        type="password",
        key="password",
        on_change=do_signup if option == "Signup" else do_login
    )

    # Process action outside callback
    if "auth_action" in st.session_state:
        if st.session_state["auth_action"] == "signup":
            try:
                supabase.auth.sign_up({"email": st.session_state["email"], "password": st.session_state["password"]})
                st.success("Signup successful! Please login.")
            except Exception as e:
                st.error(f"Error: {e}")
        elif st.session_state["auth_action"] == "login":
            try:
                user = supabase.auth.sign_in_with_password({"email": st.session_state["email"], "password": st.session_state["password"]})
                if user and user.user:
                    st.session_state["user"] = user.user
                    st.session_state["menu"] = "Overview"
                    st.success("Login successful! Redirecting to dashboard...")
                    st.session_state.pop("auth_action")  # clear flag
                    st.rerun()  # ✅ works here, outside callback
                else:
                    st.error("Invalid credentials")
            except Exception as e:
                st.error(f"Error: {e}")
