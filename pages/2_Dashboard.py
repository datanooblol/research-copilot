import streamlit as st

st.title("📚 Dashboard")

if not st.session_state.papers:
    st.info("No papers added yet. Go to Search to add papers.")
else:
    st.write(f"**Total Papers:** {len(st.session_state.papers)}")
    
    for paper_id, paper in st.session_state.papers.items():
        with st.container(border=True):
            col1, col2 = st.columns([4, 1])
            
            with col1:
                st.subheader(paper["title"])
                st.write(f"**Authors:** {', '.join(paper['authors'])}")
                st.write(f"**Published:** {paper['published']}")
                st.write(f"**Notes:** {len(paper['notes'])}")
            
            with col2:
                if st.button("Open", key=f"open_{paper_id}"):
                    st.session_state.current_paper_id = paper_id
                    st.switch_page("pages/3_Paper.py")
                
                if st.button("Remove", key=f"remove_{paper_id}"):
                    del st.session_state.papers[paper_id]
                    st.rerun()
