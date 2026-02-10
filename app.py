import streamlit as st
from ui import sidebar

from agents import agent
import os

# Page config
st.set_page_config(
    page_title="Recruitment Agent 🚀",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom session state initialization
if 'score' not in st.session_state:
    st.session_state.score = None
if 'passed' not in st.session_state:
    st.session_state.passed = False

def main():
    # Sidebar with agent status
    with st.sidebar:
        st.title("⚙️ Agent Controls")
        st.info("✅ Backend: Mistral LLM + RAG")
        st.info("✅ Frontend: Streamlit + Plotly")
        st.info("✅ NLP: Sentence Transformers")
        
        if st.button("🔄 Refresh Agent"):
            st.cache_data.clear()
            st.rerun()
    
    # Render complete UI
    render_ui()

if __name__ == "__main__":
    main()
