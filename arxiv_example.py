import arxiv

# Search for papers
search = arxiv.Search(
    query="machine learning",
    max_results=5,
    sort_by=arxiv.SortCriterion.SubmittedDate
)

for result in search.results():
    print(f"Title: {result.title}")
    print(f"Authors: {', '.join(a.name for a in result.authors)}")
    print(f"Published: {result.published}")
    print(f"URL: {result.entry_id}")
    print("-" * 80)
