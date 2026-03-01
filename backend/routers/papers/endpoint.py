"""API endpoints for paper/note operations."""
from fastapi import APIRouter, Depends
from .service import PaperService
from .model import NoteCreate, NoteUpdate, NotePositionUpdate, NoteResponse, NotesResponse, DeleteResponse

router = APIRouter(tags=["papers"])

def get_service() -> PaperService:
    """Dependency injection for paper service.
    
    Returns:
        PaperService instance.
    """
    return PaperService()

@router.get("/papers/{paper_id}/notes", response_model=NotesResponse)
def get_notes(paper_id: str, service: PaperService = Depends(get_service)):
    """Get all notes for a paper.
    
    Args:
        paper_id: Paper identifier.
        service: Injected paper service.
        
    Returns:
        List of notes.
    """
    notes = service.get_notes(paper_id)
    return NotesResponse(notes=notes)

@router.post("/papers/{paper_id}/notes", response_model=NoteResponse)
def create_note(paper_id: str, note: NoteCreate, service: PaperService = Depends(get_service)):
    """Create a new note for a paper.
    
    Args:
        paper_id: Paper identifier.
        note: Note data.
        service: Injected paper service.
        
    Returns:
        Created note.
    """
    return service.create_note(paper_id, note)

@router.put("/notes/{note_id}", response_model=NoteResponse)
def update_note(note_id: str, note: NoteUpdate, service: PaperService = Depends(get_service)):
    """Update a note.
    
    Args:
        note_id: Note identifier.
        note: Note update data.
        service: Injected paper service.
        
    Returns:
        Updated note.
    """
    return service.update_note(note_id, note)

@router.delete("/notes/{note_id}", response_model=DeleteResponse)
def delete_note(note_id: str, service: PaperService = Depends(get_service)):
    """Delete a note.
    
    Args:
        note_id: Note identifier.
        service: Injected paper service.
        
    Returns:
        Success status.
    """
    success = service.delete_note(note_id)
    return DeleteResponse(success=success)

@router.patch("/notes/{note_id}/position", response_model=NoteResponse)
def update_note_position(note_id: str, position: NotePositionUpdate, service: PaperService = Depends(get_service)):
    """Update note position on canvas.
    
    Args:
        note_id: Note identifier.
        position: Position update data.
        service: Injected paper service.
        
    Returns:
        Updated note.
    """
    return service.update_note_position(note_id, position)
