"""Service layer for search operations."""
import arxiv
from .model import SearchResult

class SearchService:
    """Service for searching arXiv papers."""
    
    def search_papers(self, query: str, max_results: int = 10) -> list[SearchResult]:
        """Search arXiv for papers.
        
        Args:
            query: Search query string.
            max_results: Maximum number of results to return.
            
        Returns:
            List of search results.
        """
        search = arxiv.Search(
            query=query,
            max_results=max_results,
            sort_by=arxiv.SortCriterion.Relevance
        )
        
        results = []
        for result in arxiv.Client().results(search):
            results.append(SearchResult(
                id=result.get_short_id(),
                title=result.title,
                authors=[a.name for a in result.authors],
                year=result.published.year,
                published=result.published.isoformat(),
                summary=result.summary,
                entry_id=result.entry_id,
                pdf_url=result.pdf_url,
                doi=result.doi
            ))
        
        return results
