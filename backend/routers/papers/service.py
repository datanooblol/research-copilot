"""Service layer for paper/note operations."""
import json
from repositories.paper_repository import PaperRepository
from .model import NoteCreate, NoteUpdate, NotePositionUpdate, NoteResponse

class PaperService:
    """Service for paper and note operations."""
    
    def __init__(self):
        """Initialize service with repository."""
        self.repository = PaperRepository()
    
    def get_notes(self, paper_id: str) -> list[NoteResponse]:
        """Get all notes for a paper.
        
        Args:
            paper_id: Paper identifier.
            
        Returns:
            List of notes.
        """
        notes = self.repository.get_notes(paper_id)
        results = []
        
        for note in notes:
            tags = json.loads(note['tags']) if isinstance(note['tags'], str) else note['tags']
            results.append(NoteResponse(
                id=note['id'],
                note_id=note['note_id'],
                paper_id=note['paper_id'],
                page=note['page'] or "",
                tags=tags or [],
                content=note['content'],
                position_x=note['position_x'],
                position_y=note['position_y'],
                width=note['width'],
                height=note['height'],
                created_at=note['created_at'].isoformat(),
                updated_at=note['updated_at'].isoformat()
            ))
        
        return results
    
    def create_note(self, paper_id: str, note: NoteCreate) -> NoteResponse:
        """Create a new note.
        
        Args:
            paper_id: Paper identifier.
            note: Note data.
            
        Returns:
            Created note.
        """
        created = self.repository.create_note(paper_id, note.page, note.tags, note.content, note.position_x, note.position_y, note.width, note.height)
        tags = json.loads(created['tags']) if isinstance(created['tags'], str) else created['tags']
        
        return NoteResponse(
            id=created['id'],
            note_id=created['note_id'],
            paper_id=created['paper_id'],
            page=created['page'] or "",
            tags=tags or [],
            content=created['content'],
            position_x=created['position_x'],
            position_y=created['position_y'],
            width=created['width'],
            height=created['height'],
            created_at=created['created_at'].isoformat(),
            updated_at=created['updated_at'].isoformat()
        )
    
    def update_note(self, note_id: str, note: NoteUpdate) -> NoteResponse:
        """Update a note.
        
        Args:
            note_id: Note identifier.
            note: Note update data.
            
        Returns:
            Updated note.
        """
        updated = self.repository.update_note(note_id, note.page, note.tags, note.content)
        tags = json.loads(updated['tags']) if isinstance(updated['tags'], str) else updated['tags']
        
        return NoteResponse(
            id=updated['id'],
            note_id=updated['note_id'],
            paper_id=updated['paper_id'],
            page=updated['page'] or "",
            tags=tags or [],
            content=updated['content'],
            position_x=updated['position_x'],
            position_y=updated['position_y'],
            width=updated['width'],
            height=updated['height'],
            created_at=updated['created_at'].isoformat(),
            updated_at=updated['updated_at'].isoformat()
        )
    
    def update_note_position(self, note_id: str, position: NotePositionUpdate) -> NoteResponse:
        """Update note position on canvas.
        
        Args:
            note_id: Note identifier.
            position: Position update data.
            
        Returns:
            Updated note.
        """
        updated = self.repository.update_note_position(note_id, position.position_x, position.position_y, position.width, position.height)
        tags = json.loads(updated['tags']) if isinstance(updated['tags'], str) else updated['tags']
        
        return NoteResponse(
            id=updated['id'],
            note_id=updated['note_id'],
            paper_id=updated['paper_id'],
            page=updated['page'] or "",
            tags=tags or [],
            content=updated['content'],
            position_x=updated['position_x'],
            position_y=updated['position_y'],
            width=updated['width'],
            height=updated['height'],
            created_at=updated['created_at'].isoformat(),
            updated_at=updated['updated_at'].isoformat()
        )
    
    def delete_note(self, note_id: str) -> bool:
        """Delete a note.
        
        Args:
            note_id: Note identifier.
            
        Returns:
            True if deleted.
        """
        return self.repository.delete_note(note_id)
