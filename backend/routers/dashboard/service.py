"""Service layer for dashboard operations."""
import json
from repositories.dashboard_repository import DashboardRepository
from .model import PaperInfo, PaperResponse

class DashboardService:
    """Service for dashboard operations."""
    
    def __init__(self):
        """Initialize service with repository."""
        self.repository = DashboardRepository()
    
    def get_all_papers(self, user_id: str = "admin") -> list[PaperResponse]:
        """Get all papers for user.
        
        Args:
            user_id: User identifier.
            
        Returns:
            List of papers.
        """
        papers = self.repository.get_all_papers(user_id)
        results = []
        
        for paper in papers:
            info = json.loads(paper['paper_info']) if isinstance(paper['paper_info'], str) else paper['paper_info']
            results.append(PaperResponse(
                id=paper['id'],
                paper_id=paper['paper_id'],
                title=info['title'],
                authors=info['authors'],
                year=info['year'],
                published=info['published'],
                summary=info['summary'],
                doi=info.get('doi'),
                publisher=info.get('publisher', 'arxiv'),
                entry_id=info['entry_id'],
                pdf_url=info['pdf_url'],
                created_at=paper['created_at'].isoformat(),
                note_count=paper['note_count']
            ))
        
        return results
    
    def add_paper(self, paper_info: PaperInfo, user_id: str = "admin") -> PaperResponse:
        """Add paper to dashboard.
        
        Args:
            paper_info: Paper metadata.
            user_id: User identifier.
            
        Returns:
            Created paper.
        """
        paper = self.repository.add_paper(user_id, paper_info.model_dump())
        info = json.loads(paper['paper_info']) if isinstance(paper['paper_info'], str) else paper['paper_info']
        
        return PaperResponse(
            id=paper['id'],
            paper_id=paper['paper_id'],
            title=info['title'],
            authors=info['authors'],
            year=info['year'],
            published=info['published'],
            summary=info['summary'],
            doi=info.get('doi'),
            publisher=info.get('publisher', 'arxiv'),
            entry_id=info['entry_id'],
            pdf_url=info['pdf_url'],
            created_at=paper['created_at'].isoformat(),
            note_count=0
        )
    
    def delete_paper(self, paper_id: str) -> bool:
        """Delete paper from dashboard.
        
        Args:
            paper_id: Paper identifier.
            
        Returns:
            True if deleted.
        """
        return self.repository.delete_paper(paper_id)
