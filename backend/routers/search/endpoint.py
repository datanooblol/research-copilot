"""API endpoints for search operations."""
from fastapi import APIRouter, Depends
from .service import SearchService
from .model import SearchResponse

router = APIRouter(prefix="/search", tags=["search"])

def get_service() -> SearchService:
    """Dependency injection for search service.
    
    Returns:
        SearchService instance.
    """
    return SearchService()

@router.get("", response_model=SearchResponse)
def search_papers(query: str, max_results: int = 10, service: SearchService = Depends(get_service)):
    """Search arXiv for papers.
    
    Args:
        query: Search query string.
        max_results: Maximum number of results.
        service: Injected search service.
        
    Returns:
        Search results from arXiv.
    """
    results = service.search_papers(query, max_results)
    return SearchResponse(results=results)
