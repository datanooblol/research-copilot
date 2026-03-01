"""Repository for dashboard database operations."""
import json
import uuid
from database.connection import get_db

class DashboardRepository:
    """Repository for dashboard operations."""
    
    def __init__(self):
        """Initialize repository with database connection."""
        self.db = get_db()
    
    def get_all_papers(self, user_id: str) -> list[dict]:
        """Get all papers for a user.
        
        Args:
            user_id: User identifier.
            
        Returns:
            List of papers with metadata.
        """
        query = """
            SELECT d.id, d.paper_id, d.paper_info, d.created_at,
                   COUNT(p.note_id) as note_count
            FROM dashboards d
            LEFT JOIN papers p ON d.paper_id = p.paper_id
            WHERE d.user_id = ?
            GROUP BY d.id, d.paper_id, d.paper_info, d.created_at
            ORDER BY d.created_at DESC
        """
        result = self.db.execute(query, [user_id]).fetchall()
        return [dict(zip(['id', 'paper_id', 'paper_info', 'created_at', 'note_count'], row)) for row in result]
    
    def add_paper(self, user_id: str, paper_info: dict) -> dict:
        """Add a paper to dashboard.
        
        Args:
            user_id: User identifier.
            paper_info: Paper metadata.
            
        Returns:
            Created paper record.
        """
        id = str(uuid.uuid4())
        paper_id = str(uuid.uuid4())
        
        query = """
            INSERT INTO dashboards (id, user_id, paper_id, paper_info)
            VALUES (?, ?, ?, ?)
        """
        self.db.execute(query, [id, user_id, paper_id, json.dumps(paper_info)])
        
        result = self.db.execute(
            "SELECT id, paper_id, paper_info, created_at FROM dashboards WHERE id = ?",
            [id]
        ).fetchone()
        
        return dict(zip(['id', 'paper_id', 'paper_info', 'created_at'], result))
    
    def delete_paper(self, paper_id: str) -> bool:
        """Delete a paper from dashboard.
        
        Args:
            paper_id: Paper identifier.
            
        Returns:
            True if deleted successfully.
        """
        self.db.execute("DELETE FROM papers WHERE paper_id = ?", [paper_id])
        self.db.execute("DELETE FROM dashboards WHERE paper_id = ?", [paper_id])
        return True
