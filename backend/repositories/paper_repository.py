"""Repository for paper/note database operations."""
import json
import uuid
from datetime import datetime
from database.connection import get_db

class PaperRepository:
    """Repository for paper and note operations."""
    
    def __init__(self):
        """Initialize repository with database connection."""
        self.db = get_db()
    
    def get_notes(self, paper_id: str) -> list[dict]:
        """Get all notes for a paper.
        
        Args:
            paper_id: Paper identifier.
            
        Returns:
            List of notes.
        """
        query = """
            SELECT id, paper_id, note_id, page, tags, content, position_x, position_y, width, height, created_at, updated_at
            FROM papers
            WHERE paper_id = ?
            ORDER BY created_at DESC
        """
        result = self.db.execute(query, [paper_id]).fetchall()
        return [dict(zip(['id', 'paper_id', 'note_id', 'page', 'tags', 'content', 'position_x', 'position_y', 'width', 'height', 'created_at', 'updated_at'], row)) for row in result]
    
    def create_note(self, paper_id: str, page: str, tags: list[str], content: str, position_x: float, position_y: float, width: float, height: float) -> dict:
        """Create a new note.
        
        Args:
            paper_id: Paper identifier.
            page: Page reference.
            tags: List of tags.
            content: Note content.
            position_x: Canvas X coordinate.
            position_y: Canvas Y coordinate.
            width: Note card width.
            height: Note card height.
            
        Returns:
            Created note.
        """
        id = str(uuid.uuid4())
        note_id = str(uuid.uuid4())
        
        query = """
            INSERT INTO papers (id, paper_id, note_id, page, tags, content, position_x, position_y, width, height)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """
        self.db.execute(query, [id, paper_id, note_id, page, json.dumps(tags), content, position_x, position_y, width, height])
        
        result = self.db.execute(
            "SELECT id, paper_id, note_id, page, tags, content, position_x, position_y, width, height, created_at, updated_at FROM papers WHERE id = ?",
            [id]
        ).fetchone()
        
        self.db.commit()
        
        return dict(zip(['id', 'paper_id', 'note_id', 'page', 'tags', 'content', 'position_x', 'position_y', 'width', 'height', 'created_at', 'updated_at'], result))
    
    def update_note(self, note_id: str, page: str | None, tags: list[str] | None, content: str | None) -> dict:
        """Update a note.
        
        Args:
            note_id: Note identifier.
            page: Page reference.
            tags: List of tags.
            content: Note content.
            
        Returns:
            Updated note.
        """
        updates = []
        params = []
        
        if page is not None:
            updates.append("page = ?")
            params.append(page)
        if tags is not None:
            updates.append("tags = ?")
            params.append(json.dumps(tags))
        if content is not None:
            updates.append("content = ?")
            params.append(content)
        
        updates.append("updated_at = CURRENT_TIMESTAMP")
        params.append(note_id)
        
        query = f"UPDATE papers SET {', '.join(updates)} WHERE note_id = ?"
        self.db.execute(query, params)
        
        result = self.db.execute(
            "SELECT id, paper_id, note_id, page, tags, content, position_x, position_y, width, height, created_at, updated_at FROM papers WHERE note_id = ?",
            [note_id]
        ).fetchone()
        
        self.db.commit()
        
        return dict(zip(['id', 'paper_id', 'note_id', 'page', 'tags', 'content', 'position_x', 'position_y', 'width', 'height', 'created_at', 'updated_at'], result))
    
    def update_note_position(self, note_id: str, position_x: float, position_y: float, width: float | None, height: float | None) -> dict:
        """Update note position on canvas.
        
        Args:
            note_id: Note identifier.
            position_x: Canvas X coordinate.
            position_y: Canvas Y coordinate.
            width: Note card width.
            height: Note card height.
            
        Returns:
            Updated note.
        """
        updates = ["position_x = ?", "position_y = ?"]
        params = [position_x, position_y]
        
        if width is not None:
            updates.append("width = ?")
            params.append(width)
        if height is not None:
            updates.append("height = ?")
            params.append(height)
        
        updates.append("updated_at = CURRENT_TIMESTAMP")
        params.append(note_id)
        
        query = f"UPDATE papers SET {', '.join(updates)} WHERE note_id = ?"
        self.db.execute(query, params)
        
        result = self.db.execute(
            "SELECT id, paper_id, note_id, page, tags, content, position_x, position_y, width, height, created_at, updated_at FROM papers WHERE note_id = ?",
            [note_id]
        ).fetchone()
        
        self.db.commit()
        
        return dict(zip(['id', 'paper_id', 'note_id', 'page', 'tags', 'content', 'position_x', 'position_y', 'width', 'height', 'created_at', 'updated_at'], result))
    
    def delete_note(self, note_id: str) -> bool:
        """Delete a note.
        
        Args:
            note_id: Note identifier.
            
        Returns:
            True if deleted.
        """
        self.db.execute("DELETE FROM papers WHERE note_id = ?", [note_id])
        self.db.commit()
        return True
