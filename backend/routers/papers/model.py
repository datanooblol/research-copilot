"""Pydantic models for papers/notes endpoints."""
from pydantic import BaseModel

class NoteCreate(BaseModel):
    """Request model for creating a note."""
    page: str = ""
    tags: list[str] = []
    content: str

class NoteUpdate(BaseModel):
    """Request model for updating a note."""
    page: str | None = None
    tags: list[str] | None = None
    content: str | None = None

class NoteResponse(BaseModel):
    """Response model for a note."""
    id: str
    note_id: str
    paper_id: str
    page: str
    tags: list[str]
    content: str
    created_at: str
    updated_at: str

class NotesResponse(BaseModel):
    """Response for notes list endpoint."""
    notes: list[NoteResponse]

class DeleteResponse(BaseModel):
    """Response for delete operations."""
    success: bool
