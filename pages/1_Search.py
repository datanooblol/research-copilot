import streamlit as st
import arxiv
import requests

st.title("🔍 Search Papers")

query = st.text_input("Search arXiv", placeholder="Enter keywords...")

if st.button("Search"):
    with st.spinner("Searching..."):
        search = arxiv.Search(query=query, max_results=10, sort_by=arxiv.SortCriterion.Relevance)
        results = list(arxiv.Client().results(search))
        
        if results:
            st.success(f"Found {len(results)} papers")
            
            for result in results:
                with st.expander(f"📄 {result.title}"):
                    st.write(f"**Authors:** {', '.join(a.name for a in result.authors)}")
                    st.write(f"**Published:** {result.published.date()}")
                    st.write(f"**Summary:** {result.summary}")
                    
                    if st.button("Add to Dashboard", key=result.entry_id):
                        paper_id = result.get_short_id()
                        pdf_url = result.entry_id.replace("abs", "pdf")
                        
                        st.session_state.papers[paper_id] = {
                            "id": paper_id,
                            "title": result.title,
                            "authors": [a.name for a in result.authors],
                            "published": result.published.date(),
                            "summary": result.summary,
                            "pdf_url": pdf_url,
                            "notes": []
                        }
                        st.success(f"Added '{result.title}' to dashboard!")
                        st.rerun()
        else:
            st.warning("No results found")
