import streamlit as st
from dotenv import load_dotenv
from loguru import logger
import os

from utils.styles import inject_css
from pages.home import render_home
from pages.admin import render_admin_dashboard
from pages.doctor import render_doctor_dashboard

# Load environment variables
load_dotenv()

# Configure logging
logger.add("logs/app.log", rotation="1 MB", level="DEBUG", 
           format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {file}:{line} | {message}")

# Streamlit page configuration
st.set_page_config(page_title="Clinical Intelligence Platform", layout="wide", initial_sidebar_state="expanded")

# Inject custom CSS
inject_css()

def main():
    logger.info("Dashboard launched")
    
    if "user_role" not in st.session_state:
        render_home()
    elif st.session_state.user_role == "admin":
        render_admin_dashboard()
    elif st.session_state.user_role == "doctor":
        render_doctor_dashboard()

if __name__ == "__main__":
    main()