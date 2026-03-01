"""API endpoints for dashboard operations."""
from fastapi import APIRouter, Depends
from .service import DashboardService
from .model import PaperCreate, PaperResponse, DashboardResponse, DeleteResponse

router = APIRouter(prefix="/dashboard", tags=["dashboard"])

def get_service() -> DashboardService:
    """Dependency injection for dashboard service.
    
    Returns:
        DashboardService instance.
    """
    return DashboardService()

@router.get("", response_model=DashboardResponse)
def get_dashboard(service: DashboardService = Depends(get_service)):
    """Get all papers in dashboard.
    
    Args:
        service: Injected dashboard service.
        
    Returns:
        List of papers.
    """
    papers = service.get_all_papers()
    return DashboardResponse(papers=papers)

@router.post("", response_model=PaperResponse)
def add_paper(paper: PaperCreate, service: DashboardService = Depends(get_service)):
    """Add paper to dashboard.
    
    Args:
        paper: Paper data to add.
        service: Injected dashboard service.
        
    Returns:
        Created paper.
    """
    return service.add_paper(paper.paper_info)

@router.delete("/{paper_id}", response_model=DeleteResponse)
def delete_paper(paper_id: str, service: DashboardService = Depends(get_service)):
    """Delete paper from dashboard.
    
    Args:
        paper_id: Paper identifier.
        service: Injected dashboard service.
        
    Returns:
        Success status.
    """
    success = service.delete_paper(paper_id)
    return DeleteResponse(success=success)
