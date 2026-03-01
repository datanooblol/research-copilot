"""Pydantic models for papers/notes endpoints."""
from pydantic import BaseModel

class NoteCreate(BaseModel):
    """Request model for creating a note."""
    page: str = ""
    tags: list[str] = []
    content: str
    position_x: float = 0.0
    position_y: float = 0.0
    width: float = 300.0
    height: float = 200.0

class NoteUpdate(BaseModel):
    """Request model for updating a note."""
    page: str | None = None
    tags: list[str] | None = None
    content: str | None = None

class NotePositionUpdate(BaseModel):
    """Request model for updating note position."""
    position_x: float
    position_y: float
    width: float | None = None
    height: float | None = None

class NoteResponse(BaseModel):
    """Response model for a note."""
    id: str
    note_id: str
    paper_id: str
    page: str
    tags: list[str]
    content: str
    position_x: float
    position_y: float
    width: float
    height: float
    created_at: str
    updated_at: str

class NotesResponse(BaseModel):
    """Response for notes list endpoint."""
    notes: list[NoteResponse]

class DeleteResponse(BaseModel):
    """Response for delete operations."""
    success: bool
