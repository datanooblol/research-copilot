"""Pydantic models for search endpoints."""
from pydantic import BaseModel

class SearchResult(BaseModel):
    """Search result from arXiv."""
    id: str
    title: str
    authors: list[str]
    year: int
    published: str
    summary: str
    entry_id: str
    pdf_url: str
    doi: str | None = None

class SearchResponse(BaseModel):
    """Response for search endpoint."""
    results: list[SearchResult]
