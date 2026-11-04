import streamlit as st
from gui import render_dashboard

st.set_page_config(
    page_title="RAG Deadlock Simulator",
    page_icon="🔄",
    layout="wide",
    initial_sidebar_state="expanded"
)

render_dashboard()