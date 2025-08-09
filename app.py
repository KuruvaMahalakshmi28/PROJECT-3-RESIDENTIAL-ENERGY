import streamlit as st
from dashboard import show_dashboard
from assistant import show_assistant

st.set_page_config(page_title="Energy Analytics", layout="wide")

page = st.sidebar.radio("Select View", ["Dashboard", "AI Assistant"])

if page == "Dashboard":
    show_dashboard()
elif page == "AI Assistant":
    show_assistant()
