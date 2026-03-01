import streamlit as st
import arxiv
import requests

st.set_page_config(layout="wide")

if "notes" not in st.session_state:
    st.session_state.notes = []
if "editing" not in st.session_state:
    st.session_state.editing = None
if "current_pdf" not in st.session_state:
    st.session_state.current_pdf = None
if "search_results" not in st.session_state:
    st.session_state.search_results = []

# Search Section
st.title("Research Paper Reader")
query = st.text_input("Search arXiv")
if st.button("Search"):
    search = arxiv.Search(query=query, max_results=10, sort_by=arxiv.SortCriterion.Relevance)
    st.session_state.search_results = list(arxiv.Client().results(search))

if st.session_state.search_results:
    st.subheader("Search Results")
    for result in st.session_state.search_results:
        with st.expander(f"{result.title}"):
            st.write(f"**Authors:** {', '.join(a.name for a in result.authors)}")
            st.write(f"**Published:** {result.published.date()}")
            st.write(f"**Summary:** {result.summary}")
            if st.button("Read Paper", key=result.entry_id):
                pdf_url = result.entry_id.replace("abs", "pdf")
                response = requests.get(pdf_url)
                st.session_state.current_pdf = response.content
                st.session_state.notes = []
                st.rerun()

st.divider()

# PDF Reader and Notes Section
if st.session_state.current_pdf:
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.pdf(st.session_state.current_pdf, height=800)
    
    with col2:
        st.subheader("Add Note")
        page = st.number_input("Page", min_value=1, step=1)
        tag = st.text_input("Tag")
        note = st.text_area("Note")
        
        if st.button("Add"):
            st.session_state.notes.append({"page": page, "tag": tag, "note": note})
            st.rerun()
        
        st.divider()
        st.subheader("Notes")
        
        for i, n in enumerate(st.session_state.notes):
            with st.container(border=True):
                if st.session_state.editing == i:
                    new_page = st.number_input("Page", value=n["page"], key=f"page_{i}")
                    new_tag = st.text_input("Tag", value=n["tag"], key=f"tag_{i}")
                    new_note = st.text_area("Note", value=n["note"], key=f"note_{i}")
                    col_a, col_b = st.columns(2)
                    with col_a:
                        if st.button("Save", key=f"save_{i}"):
                            st.session_state.notes[i] = {"page": new_page, "tag": new_tag, "note": new_note}
                            st.session_state.editing = None
                            st.rerun()
                    with col_b:
                        if st.button("Cancel", key=f"cancel_{i}"):
                            st.session_state.editing = None
                            st.rerun()
                else:
                    st.write(f"**Page {n['page']}** | `{n['tag']}`")
                    st.write(n["note"])
                    col_a, col_b = st.columns(2)
                    with col_a:
                        if st.button("Edit", key=f"edit_{i}"):
                            st.session_state.editing = i
                            st.rerun()
                    with col_b:
                        if st.button("Delete", key=f"del_{i}"):
                            st.session_state.notes.pop(i)
                            st.rerun()
