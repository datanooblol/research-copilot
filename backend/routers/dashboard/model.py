"""Pydantic models for dashboard endpoints."""
from pydantic import BaseModel

class PaperInfo(BaseModel):
    """Paper metadata stored in paper_info JSON."""
    title: str
    year: int
    published: str
    authors: list[str]
    summary: str
    doi: str | None = None
    publisher: str = "arxiv"
    entry_id: str
    pdf_url: str

class PaperCreate(BaseModel):
    """Request model for adding a paper."""
    paper_info: PaperInfo

class PaperResponse(BaseModel):
    """Paper response for dashboard."""
    id: str
    paper_id: str
    title: str
    authors: list[str]
    year: int
    published: str
    summary: str
    doi: str | None
    publisher: str
    entry_id: str
    pdf_url: str
    created_at: str
    note_count: int = 0

class DashboardResponse(BaseModel):
    """Response for dashboard endpoint."""
    papers: list[PaperResponse]

class DeleteResponse(BaseModel):
    """Response for delete operations."""
    success: bool
