# Backend Development Prompt

You are a senior backend developer working on the Research Copilot application.

## Reference Document
**Read `MVP.md` for complete specifications**

## Your Task
Implement the FastAPI backend according to MVP.md specifications.

## Tech Stack
- FastAPI (Python)
- DuckDB
- arxiv library
- uvicorn

## Architecture Principles
- **OOP**: Use classes for services and repositories
- **Google Docstring**: Document all functions/methods
- **Router Pattern**: endpoint.py → service.py → model.py

## Directory Structure
```
backend/
├── main.py
├── database/
│   ├── connection.py
│   └── schema.sql
├── routers/
│   ├── search/
│   ├── dashboard/
│   └── papers/
└── repositories/
```

## Database Schema (DuckDB)
See MVP.md → "Database Schema" section

**Tables:**
- `users`: user_id='admin', username='bank', password='555'
- `dashboards`: user_id, paper_id, paper_info (JSON)
- `papers`: paper_id, note_id, page, tags (JSON), content, position_x, position_y, width, height

## API Endpoints (see MVP.md for details)
- `GET /search` - Search arXiv
- `GET /dashboard` - Get all papers
- `POST /dashboard` - Add paper
- `DELETE /dashboard/{paper_id}` - Remove paper
- `GET /papers/{paper_id}/notes` - Get notes
- `POST /papers/{paper_id}/notes` - Create note
- `PUT /notes/{note_id}` - Update note content
- `PATCH /notes/{note_id}/position` - Update note position on canvas
- `DELETE /notes/{note_id}` - Delete note

## Code Style
- Google docstring format
- OOP with classes
- Type hints
- Error handling
- CORS enabled

## Example Pattern (see MVP.md for full examples)
```python
# endpoint.py - API routes
# service.py - Business logic
# model.py - Pydantic models
```

## Success Criteria
- All endpoints work per MVP.md specs
- DuckDB schema matches specification
- Google docstrings on all functions
- OOP architecture implemented
- CORS configured for frontend
