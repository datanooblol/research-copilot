import streamlit as st
import requests

st.set_page_config(layout="wide")

if "editing" not in st.session_state:
    st.session_state.editing = None

if not st.session_state.current_paper_id:
    st.warning("No paper selected. Go to Dashboard to select a paper.")
    st.stop()

paper = st.session_state.papers.get(st.session_state.current_paper_id)

if not paper:
    st.error("Paper not found")
    st.stop()

st.title(f"📄 {paper['title']}")

col1, col2 = st.columns([2, 1])

with col1:
    with st.spinner("Loading PDF..."):
        response = requests.get(paper["pdf_url"])
        st.pdf(response.content, height=800)

with col2:
    st.subheader("Add Note")
    page = st.number_input("Page", min_value=1, step=1)
    tag = st.text_input("Tag")
    note = st.text_area("Note")
    
    if st.button("Add"):
        paper["notes"].append({"page": page, "tag": tag, "note": note})
        st.rerun()
    
    st.divider()
    st.subheader(f"Notes ({len(paper['notes'])})")
    
    for i, n in enumerate(paper["notes"]):
        with st.container(border=True):
            if st.session_state.editing == i:
                new_page = st.number_input("Page", value=n["page"], key=f"page_{i}")
                new_tag = st.text_input("Tag", value=n["tag"], key=f"tag_{i}")
                new_note = st.text_area("Note", value=n["note"], key=f"note_{i}")
                col_a, col_b = st.columns(2)
                with col_a:
                    if st.button("Save", key=f"save_{i}"):
                        paper["notes"][i] = {"page": new_page, "tag": new_tag, "note": new_note}
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
                        paper["notes"].pop(i)
                        st.rerun()
