import streamlit as st

st.set_page_config(page_title="Research Copilot", layout="wide")

# Initialize session state
if "papers" not in st.session_state:
    st.session_state.papers = {}
if "current_paper_id" not in st.session_state:
    st.session_state.current_paper_id = None

st.title("🔬 Research Copilot")
st.write("Navigate using the sidebar to search papers, view your dashboard, or read papers.")
