import streamlit as st
import sys
import os

# Thêm đường dẫn để import các module
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from src.ui.tabs import create_sidebar, create_tabs
from src.logic.data_manager import DataManager
from src.ai.gemini_client import GeminiClient

def main():
    # Cấu hình trang
    st.set_page_config(
        page_title="CADAP - Credit Analysis & Decision Assistance Platform",
        page_icon="🏦",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Khởi tạo session state
    if 'data_manager' not in st.session_state:
        st.session_state.data_manager = DataManager()
    if 'gemini_client' not in st.session_state:
        st.session_state.gemini_client = GeminiClient()
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []
    
    # Tạo sidebar
    create_sidebar()
    
    # Header
    st.title("🏦 CADAP - Credit Analysis & Decision Assistance Platform")
    st.markdown("---")
    
    # Tạo các tab
    create_tabs()

if __name__ == "__main__":
    main()