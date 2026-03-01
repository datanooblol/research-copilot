# Research Copilot - MVP Technical Specification

## Overview
A web application for managing research papers with PDF viewing and note-taking capabilities.

## Tech Stack
- **Frontend**: Next.js 14+ (TypeScript, React)
- **Backend**: FastAPI (Python)
- **Database**: DuckDB
- **PDF Viewer**: react-pdf
- **Rich Text Editor**: BlockNote (markdown-style editor)
- **UI Components**: Tailwind CSS + shadcn/ui

---

## Codebase Architecture

### Frontend Structure

**Design System:**
- **Design Tokens**: Centralized design variables
  - `tokens/colors.ts` - Color palette
  - `tokens/spacing.ts` - Spacing scale
  - `tokens/typography.ts` - Font sizes, weights, line heights
  - `tokens/shadows.ts` - Shadow definitions
  - `tokens/breakpoints.ts` - Responsive breakpoints

- **Atomic Design Pattern**:
  ```
  components/
  ├── atoms/           # Basic building blocks
  │   ├── Button.tsx
  │   ├── Input.tsx
  │   ├── Badge.tsx
  │   └── Text.tsx
  ├── molecules/       # Simple component groups
  │   ├── SearchBar.tsx
  │   ├── TagInput.tsx
  │   └── NoteCard.tsx
  ├── organisms/       # Complex components
  │   ├── SearchModal.tsx
  │   ├── PaperCard.tsx
  │   ├── NoteModal.tsx
  │   └── PdfViewer.tsx
  ├── templates/       # Page layouts
  │   ├── DashboardLayout.tsx
  │   └── PaperLayout.tsx
  └── pages/           # Full pages
      ├── dashboard/
      └── paper/[id]/
  ```

### Backend Structure

**Architecture Principles:**
- **OOP (Object-Oriented Programming)**: Classes for services and repositories
- **Google Docstring**: All functions/methods documented
- **Separation of Concerns**: Router → Service → Repository pattern

**Directory Structure:**
```
backend/
├── main.py                 # FastAPI app entry point
├── database/
│   ├── connection.py       # DuckDB connection manager
│   └── schema.sql          # Database schema
├── routers/
│   ├── search/
│   │   ├── endpoint.py     # API endpoints
│   │   ├── service.py      # Business logic
│   │   └── model.py        # Pydantic models
│   ├── dashboard/
│   │   ├── endpoint.py
│   │   ├── service.py
│   │   └── model.py
│   └── papers/
│       ├── endpoint.py
│       ├── service.py
│       └── model.py
└── repositories/
    ├── user_repository.py
    ├── dashboard_repository.py
    └── paper_repository.py
```

**Code Style:**
```python
class PaperService:
    """Service for managing research papers.
    
    This service handles business logic for paper operations including
    searching, adding, and retrieving papers from the dashboard.
    """
    
    def __init__(self, repository: PaperRepository):
        """Initialize the paper service.
        
        Args:
            repository: Repository instance for database operations.
        """
        self.repository = repository
    
    def add_paper(self, user_id: str, paper_data: dict) -> Paper:
        """Add a paper to user's dashboard.
        
        Args:
            user_id: UUID of the user.
            paper_data: Dictionary containing paper metadata.
            
        Returns:
            Paper: The created paper object.
            
        Raises:
            ValueError: If paper already exists in dashboard.
        """
        # Implementation
        pass
```

---

## Database Schema (DuckDB)

### Tables

#### users
```sql
CREATE TABLE users (
    user_id VARCHAR PRIMARY KEY,     -- UUID or 'admin' for MVP
    username VARCHAR NOT NULL,       -- 'bank'
    password VARCHAR NOT NULL        -- '555' (plain text for MVP)
);

-- Default user
INSERT INTO users VALUES ('admin', 'bank', '555');
```

#### dashboards
```sql
CREATE TABLE dashboards (
    id VARCHAR PRIMARY KEY,          -- UUID
    user_id VARCHAR NOT NULL,        -- Foreign key to users
    paper_id VARCHAR NOT NULL,       -- UUID
    paper_info JSON NOT NULL,        -- Paper metadata
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(user_id)
);
```

**paper_info JSON structure:**
```json
{
  "title": "Paper Title",
  "year": 2025,
  "published": "2025-04-07T10:52:22+00:00",
  "authors": ["Author 1", "Author 2"],
  "summary": "Abstract text...",
  "doi": "10.1234/example",
  "publisher": "arxiv",
  "entry_id": "http://arxiv.org/abs/2504.04915v1",
  "pdf_url": "http://arxiv.org/pdf/2504.04915v1"
}
```

#### papers
```sql
CREATE TABLE papers (
    id VARCHAR PRIMARY KEY,          -- UUID
    paper_id VARCHAR NOT NULL,       -- Foreign key to dashboards.paper_id
    note_id VARCHAR NOT NULL,        -- UUID
    page VARCHAR,                    -- "1", "1,3", "1-5", or ""
    tags JSON,                       -- ["methodology", "important"]
    content TEXT,                    -- BlockNote JSON/HTML
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

---

## Page-to-Storage Mapping

### Dashboard Page
**Connects to:** `dashboards` table

**Operations:**
- **GET** all papers for user:
  ```sql
  SELECT * FROM dashboards WHERE user_id = 'admin';
  ```
- **DELETE** paper:
  ```sql
  DELETE FROM dashboards WHERE paper_id = ?;
  DELETE FROM papers WHERE paper_id = ?;
  ```

**API Endpoints:**
- `GET /dashboard` → Fetch all papers
- `DELETE /dashboard/{paper_id}` → Remove paper

---

### Search Modal
**Connects to:** `dashboards` table (when adding)

**Operations:**
- **Search**: Call arXiv API (no database)
- **Add paper**: Insert into `dashboards`
  ```sql
  INSERT INTO dashboards (id, user_id, paper_id, paper_info)
  VALUES (uuid(), 'admin', uuid(), ?);
  ```
- **Navigate**: Redirect to `/paper/{paper_id}`

**API Endpoints:**
- `GET /search?query=...` → Search arXiv
- `POST /dashboard` → Add paper to dashboard

---

### Paper Page
**Connects to:** `papers` table

**Operations:**
- **GET** all notes for paper:
  ```sql
  SELECT * FROM papers WHERE paper_id = ? ORDER BY created_at DESC;
  ```
- **CREATE** note:
  ```sql
  INSERT INTO papers (id, paper_id, note_id, page, tags, content)
  VALUES (uuid(), ?, uuid(), ?, ?, ?);
  ```
- **UPDATE** note:
  ```sql
  UPDATE papers SET page = ?, tags = ?, content = ?, updated_at = CURRENT_TIMESTAMP
  WHERE note_id = ?;
  ```
- **DELETE** note:
  ```sql
  DELETE FROM papers WHERE note_id = ?;
  ```

**API Endpoints:**
- `GET /papers/{paper_id}/notes` → Fetch all notes
- `POST /papers/{paper_id}/notes` → Create note
- `PUT /notes/{note_id}` → Update note
- `DELETE /notes/{note_id}` → Delete note

---

## Backend Router Pattern

### Example: Papers Router

**routers/papers/endpoint.py**
```python
from fastapi import APIRouter, Depends
from .service import PaperService
from .model import NoteCreate, NoteUpdate, NoteResponse

router = APIRouter(prefix="/papers", tags=["papers"])

def get_service() -> PaperService:
    """Dependency injection for paper service."""
    return PaperService()

@router.get("/{paper_id}/notes", response_model=list[NoteResponse])
def get_notes(paper_id: str, service: PaperService = Depends(get_service)):
    """Get all notes for a paper.
    
    Args:
        paper_id: UUID of the paper.
        service: Injected paper service.
        
    Returns:
        List of notes for the paper.
    """
    return service.get_notes(paper_id)

@router.post("/{paper_id}/notes", response_model=NoteResponse)
def create_note(paper_id: str, note: NoteCreate, service: PaperService = Depends(get_service)):
    """Create a new note for a paper."""
    return service.create_note(paper_id, note)
```

**routers/papers/service.py**
```python
from repositories.paper_repository import PaperRepository
from .model import NoteCreate, NoteUpdate, NoteResponse

class PaperService:
    """Service layer for paper operations."""
    
    def __init__(self):
        """Initialize service with repository."""
        self.repository = PaperRepository()
    
    def get_notes(self, paper_id: str) -> list[NoteResponse]:
        """Retrieve all notes for a paper.
        
        Args:
            paper_id: UUID of the paper.
            
        Returns:
            List of note objects.
        """
        return self.repository.find_notes_by_paper(paper_id)
    
    def create_note(self, paper_id: str, note: NoteCreate) -> NoteResponse:
        """Create a new note.
        
        Args:
            paper_id: UUID of the paper.
            note: Note data to create.
            
        Returns:
            Created note object.
        """
        return self.repository.insert_note(paper_id, note)
```

**routers/papers/model.py**
```python
from pydantic import BaseModel
from datetime import datetime

class NoteCreate(BaseModel):
    """Model for creating a note."""
    page: str = ""
    tags: list[str] = []
    content: str

class NoteUpdate(BaseModel):
    """Model for updating a note."""
    page: str | None = None
    tags: list[str] | None = None
    content: str | None = None

class NoteResponse(BaseModel):
    """Model for note response."""
    id: str
    note_id: str
    paper_id: str
    page: str
    tags: list[str]
    content: str
    created_at: datetime
    updated_at: datetime
```

---

## User Flow

1. **Dashboard** → Click "+ Add Paper" → **Search Modal**
2. **Search Modal** → Search arXiv → Click "Add" → **Paper Page**
3. **Paper Page** → View PDF + Manage Notes
4. **Paper Page** → Click "Back" → **Dashboard**

---

## Pages & Features

### 1. Dashboard Page (`/dashboard`)

**Layout:**
```
┌─────────────────────────────────────────────┐
│  Research Copilot              [+ Add Paper]│
│                                              │
│  My Papers                                  │
│  ┌────────────────────────────────────────┐ │
│  │ 📄 Paper Title                         │ │
│  │ Authors: Name 1, Name 2                │ │
│  │ Year: 2025 | Notes: 5                  │ │
│  │                      [Open] [Delete]   │ │
│  └────────────────────────────────────────┘ │
└─────────────────────────────────────────────┘
```

**Features:**
- Display all saved papers
- Show paper metadata (title, authors, year, note count)
- Open paper → Navigate to Paper Page
- Delete paper → Remove from database
- Add Paper button → Open Search Modal

**Status:** ✅ Implemented

---

### 2. Search Modal (Overlay on Dashboard)

**Layout:**
```
╔═══════════════════════════════════════╗
║  Search Papers                  [X]   ║
║  ┌─────────────────────┐  [Search]   ║
║  │ Enter keywords...   │             ║
║  └─────────────────────┘             ║
║                                       ║
║  Results:                            ║
║  ┌─────────────────────────────────┐ ║
║  │ 📄 Paper Title                  │ ║
║  │ Authors: Name 1, Name 2         │ ║
║  │ Year: 2025                      │ ║
║  │ Summary: Abstract text...       │ ║
║  │                        [Add]    │ ║
║  └─────────────────────────────────┘ ║
╚═══════════════════════════════════════╝
```

**Features:**
- Search input field
- Call backend `/search` endpoint
- Display results with metadata
- Add button → Save paper to database → Navigate to Paper Page

**API Integration:**
```
GET /search?query=RAG&max_results=10
```

**Status:** ✅ Implemented

---

### 3. Paper Page (`/paper/[id]`)

**Layout:**
```
┌─────────────────────────────────────────────┐
│  ← Back    Paper Title                      │
├──────────────────────────║──────────────────┤
│  PDF VIEWER              ║  Notes           │
│  [- 100% +]              ║  [+ Add Note]    │
│  [PDF Content]           ║                  │
│                          ║  ┌─────────────┐ │
│                          ║  │ Page: 3     │ │
│                          ║  │ methodology │ │
│                          ║  │ Note text...│ │
│                          ║  │ [Edit][Del] │ │
│                          ║  └─────────────┘ │
└──────────────────────────║──────────────────┘
                           ↕ (Draggable)
```

**Features:**
- **Left Panel**: PDF Viewer with zoom controls (+/- buttons, 50%-200%)
- **Right Panel**: Notes list
- **Draggable Divider**: Drag to adjust panel widths (20%-80% range)
- Back button → Navigate to Dashboard
- PDF displays directly from arXiv without downloading

**Status:** ✅ Implemented

---

### 4. Add/Edit Note Modal (Right Side Overlay)

**Layout:**
```
┌──────────────────────────║──────────────────┐
│  PDF VIEWER              ║ Add Note    [X]  │
│  (Still Visible)         ║                  │
│                          ║ Page Number:     │
│                          ║ ┌──────────────┐ │
│                          ║ │ 1, 3-5       │ │
│                          ║ └──────────────┘ │
│                          ║                  │
│                          ║ Tags:            │
│                          ║ ┌──────────────┐ │
│                          ║ │ methodology  │ │
│                          ║ └──────────────┘ │
│                          ║ [methodology]    │
│                          ║                  │
│                          ║ Note:            │
│                          ║ ┌──────────────┐ │
│                          ║ │ BlockNote    │ │
│                          ║ │ Editor       │ │
│                          ║ └──────────────┘ │
│                          ║                  │
│                          ║ [Cancel] [Save]  │
└──────────────────────────║──────────────────┘
```

**Features:**

#### Page Number Field
Supports multiple formats:
- Empty/Not specified: `""` → Applies to entire paper
- Single page: `"3"` → Page 3
- Multiple pages: `"1, 3, 5"` → Pages 1, 3, and 5
- Range: `"1-5"` → Pages 1 through 5
- Combined: `"1, 3-5, 10"` → Pages 1, 3, 4, 5, and 10

**Validation:**
- Parse input on blur/save
- Show error for invalid formats
- Store as string in database

#### Tags Field
- Input: Comma-separated text (`"methodology, important, steps"`)
- Auto-parse on blur: Split by comma, trim whitespace
- Display as **badges/pills** (colored capsules) below input
- Each tag is clickable to remove
- Store as array in database: `["methodology", "important", "steps"]`

**UI Example:**
```
Tags: methodology, important
[methodology] [important] [steps]
```

**Styling:** Use Tailwind CSS badge classes

#### Note Field
- **Rich Text Editor**: BlockNote (https://www.blocknotejs.org/)
- Supports markdown-style editing:
  - Headings: `# Heading`
  - Lists: `- Item` or `1. Item`
  - Bold: `**text**`
  - Italic: `*text*`
  - Code: `` `code` ``
  - Links: `[text](url)`
- Store as JSON in database
- Display rendered content in note cards (read-only BlockNoteView)

**Save Behavior:**
- Click "Save" → Show confirmation dialog: "Save this note?" (overlays only right panel)
- On confirm → Save to database → Close modal → Refresh notes list

**Modal Behavior:**
- Modal overlays only the right panel (notes section)
- PDF viewer remains visible on the left
- Confirmation dialog also constrained to right panel

**Status:** ✅ Implemented

---

## Data Contract

### Overview
This section defines the exact data structures used across Frontend, Backend API, and Database to ensure consistency.

---

### 1. Paper (Dashboard Item)

**Frontend TypeScript:**
```typescript
interface Paper {
  id: string;              // Paper UUID
  paper_id: string;        // Same as id (for consistency)
  title: string;
  authors: string[];
  year: number;
  published: string;       // ISO 8601 format
  summary: string;
  doi: string | null;
  publisher: string;       // "arxiv"
  entry_id: string;        // "http://arxiv.org/abs/2504.04915v1"
  pdf_url: string;         // "http://arxiv.org/pdf/2504.04915v1"
  created_at: string;      // ISO 8601 format
  note_count?: number;     // Optional, calculated field
}
```

**Backend Pydantic:**
```python
from pydantic import BaseModel
from datetime import datetime

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
```

**Database (DuckDB):**
```sql
-- dashboards table
id VARCHAR PRIMARY KEY           -- UUID
paper_id VARCHAR                 -- UUID
paper_info JSON                  -- PaperInfo structure
created_at TIMESTAMP

-- paper_info JSON:
{
  "title": "string",
  "year": 2025,
  "published": "2025-04-07T10:52:22+00:00",
  "authors": ["string"],
  "summary": "string",
  "doi": "string" | null,
  "publisher": "arxiv",
  "entry_id": "string",
  "pdf_url": "string"
}
```

**API Endpoints:**
```
GET /dashboard
Response: { papers: PaperResponse[] }

POST /dashboard
Request: { paper_info: PaperInfo }
Response: PaperResponse

DELETE /dashboard/{paper_id}
Response: { success: boolean }
```

---

### 2. Note

**Frontend TypeScript:**
```typescript
interface Note {
  id: string;              // Row UUID
  note_id: string;         // Note UUID
  paper_id: string;        // Foreign key
  page: string;            // "", "1", "1,3", "1-5"
  tags: string[];          // ["methodology", "important"]
  content: string;         // BlockNote JSON string
  created_at: string;      // ISO 8601 format
  updated_at: string;      // ISO 8601 format
}

interface NoteCreate {
  page: string;
  tags: string[];
  content: string;
}

interface NoteUpdate {
  page?: string;
  tags?: string[];
  content?: string;
}
```

**Backend Pydantic:**
```python
from pydantic import BaseModel
from datetime import datetime

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
    created_at: str  # ISO 8601
    updated_at: str  # ISO 8601
```

**Database (DuckDB):**
```sql
-- papers table
id VARCHAR PRIMARY KEY           -- Row UUID
paper_id VARCHAR                 -- Foreign key to dashboards.paper_id
note_id VARCHAR                  -- Note UUID
page VARCHAR                     -- "", "1", "1,3", "1-5"
tags JSON                        -- ["methodology", "important"]
content TEXT                     -- BlockNote JSON string
created_at TIMESTAMP
updated_at TIMESTAMP
```

**API Endpoints:**
```
GET /papers/{paper_id}/notes
Response: { notes: NoteResponse[] }

POST /papers/{paper_id}/notes
Request: NoteCreate
Response: NoteResponse

PUT /notes/{note_id}
Request: NoteUpdate
Response: NoteResponse

DELETE /notes/{note_id}
Response: { success: boolean }
```

---

### 3. Search Result (arXiv)

**Frontend TypeScript:**
```typescript
interface SearchResult {
  id: string;              // Short arXiv ID ("2504.04915")
  title: string;
  authors: string[];
  year: number;
  published: string;       // ISO 8601 format
  summary: string;
  entry_id: string;        // "http://arxiv.org/abs/2504.04915v1"
  doi: string | null;
}
```

**Backend Pydantic:**
```python
class SearchResult(BaseModel):
    """Search result from arXiv."""
    id: str              # Short ID
    title: str
    authors: list[str]
    year: int
    published: str       # ISO 8601
    summary: str
    entry_id: str
    doi: str | None = None

class SearchResponse(BaseModel):
    """Response for search endpoint."""
    results: list[SearchResult]
```

**API Endpoint:**
```
GET /search?query=RAG&max_results=10
Response: SearchResponse
```

---

### 4. User (MVP)

**Database (DuckDB):**
```sql
-- users table
user_id VARCHAR PRIMARY KEY      -- 'admin' for MVP
username VARCHAR                 -- 'bank'
password VARCHAR                 -- '555' (plain text for MVP)
```

**Note:** User authentication is out of scope for MVP. All operations use `user_id = 'admin'`.

---

### Field Specifications

#### Date/Time Format
- **Standard**: ISO 8601 format
- **Example**: `"2025-04-07T10:52:22+00:00"`
- **Frontend**: Use `new Date().toISOString()`
- **Backend**: Use `datetime.isoformat()`

#### UUID Format
- **Standard**: UUID v4
- **Example**: `"550e8400-e29b-41d4-a716-446655440000"`
- **Frontend**: Use `crypto.randomUUID()`
- **Backend**: Use `uuid.uuid4()`
- **Database**: Store as `VARCHAR`

#### Page Number Format
- **Type**: `string`
- **Valid formats**:
  - Empty: `""`
  - Single: `"3"`
  - Multiple: `"1, 3, 5"`
  - Range: `"1-5"`
  - Combined: `"1, 3-5, 10"`
- **Storage**: Store as-is (string)
- **Display**: Parse and show formatted

#### Tags Format
- **Type**: `string[]` (array)
- **Storage**: JSON array in database
- **Input**: Comma-separated string
- **Example**: `["methodology", "important", "key-finding"]`

#### Content Format (BlockNote)
- **Type**: `string`
- **Format**: BlockNote JSON or HTML
- **Storage**: TEXT in database
- **Example**: `'{"type":"doc","content":[...]}'`

---

### Validation Rules

#### Paper
- `title`: Required, max 500 chars
- `authors`: Required, min 1 author
- `year`: Required, 1900-2100
- `summary`: Required, max 5000 chars
- `entry_id`: Required, valid URL
- `pdf_url`: Required, valid URL

#### Note
- `page`: Optional, validate format on save
- `tags`: Optional, max 10 tags, each max 50 chars
- `content`: Required, min 1 char

---

### Error Responses

**Standard Error Format:**
```typescript
interface ErrorResponse {
  error: string;           // Error type
  message: string;         // Human-readable message
  details?: any;           // Optional details
}
```

**Backend Pydantic:**
```python
class ErrorResponse(BaseModel):
    """Standard error response."""
    error: str
    message: str
    details: dict | None = None
```

**HTTP Status Codes:**
- `200` - Success
- `201` - Created
- `400` - Bad Request (validation error)
- `404` - Not Found
- `500` - Internal Server Error

---

### Data Flow Example

**Adding a Paper:**
1. Frontend searches: `GET /search?query=RAG`
2. Backend returns: `SearchResponse` with `SearchResult[]`
3. User clicks "Add"
4. Frontend sends: `POST /dashboard` with `PaperInfo`
5. Backend creates UUID, stores in `dashboards` table
6. Backend returns: `PaperResponse`
7. Frontend navigates to: `/paper/{paper_id}`

**Creating a Note:**
1. User fills form in Note Modal
2. Frontend sends: `POST /papers/{paper_id}/notes` with `NoteCreate`
3. Backend creates UUIDs, stores in `papers` table
4. Backend returns: `NoteResponse`
5. Frontend updates notes list

---

## Data Models

### Paper
```typescript
interface Paper {
  id: string;              // arXiv ID (e.g., "2504.04915")
  title: string;
  authors: string[];
  year: number;
  summary: string;
  entry_id: string;        // arXiv URL
  pdf_url: string;         // PDF download URL
  published: string;       // ISO date
  created_at: string;      // When added to dashboard
}
```

### Note
```typescript
interface Note {
  id: string;              // UUID
  paper_id: string;        // Foreign key to Paper
  page: string;            // "1", "1,3", "1-5", or ""
  tags: string[];          // ["methodology", "important"]
  content: string;         // BlockNote JSON or HTML
  created_at: string;
  updated_at: string;
}
```

---

## API Endpoints

### Backend (FastAPI)

#### Search Papers
```
GET /search?query=RAG&max_results=10
Response: { results: Paper[] }
```

#### Papers CRUD
```
POST /papers          - Add paper to dashboard
GET /papers           - Get all papers
GET /papers/{id}      - Get single paper
DELETE /papers/{id}   - Delete paper
```

#### Notes CRUD
```
POST /papers/{id}/notes       - Create note
GET /papers/{id}/notes        - Get all notes for paper
PUT /notes/{id}               - Update note
DELETE /notes/{id}            - Delete note
```

---

## Frontend Components

### Core Components
- `SearchModal.tsx` - Search and add papers (full-screen overlay)
- `PaperCard.tsx` - Display paper in dashboard
- `PdfViewer.tsx` - PDF rendering with zoom controls (react-pdf)
- `NoteCard.tsx` - Display note with tags and read-only BlockNote content
- `NoteModal.tsx` - Add/edit note form (overlays right panel only)
- Custom draggable divider - Split view with mouse drag support

### UI Libraries
- **Tailwind CSS** - Styling
- **@blocknote/react** - Rich text editor core
- **@blocknote/mantine** - BlockNote UI components
- **react-pdf** - PDF viewer
- **axios** - API client

---

## Implementation Notes

### Page Number Parsing
```typescript
function parsePageNumbers(input: string): number[] {
  if (!input.trim()) return [];
  
  const parts = input.split(',').map(p => p.trim());
  const pages: number[] = [];
  
  for (const part of parts) {
    if (part.includes('-')) {
      const [start, end] = part.split('-').map(Number);
      for (let i = start; i <= end; i++) pages.push(i);
    } else {
      pages.push(Number(part));
    }
  }
  
  return [...new Set(pages)].sort((a, b) => a - b);
}
```

### Tag Parsing
```typescript
function parseTags(input: string): string[] {
  return input
    .split(',')
    .map(tag => tag.trim())
    .filter(tag => tag.length > 0);
}
```

### Tag Display (Badge/Pill)
```tsx
<div className="flex gap-2">
  {tags.map(tag => (
    <span key={tag} className="px-2 py-1 bg-blue-100 text-blue-800 rounded-full text-sm">
      {tag}
    </span>
  ))}
</div>
```

---

## MVP Scope

### In Scope
✅ Dashboard with paper list
✅ Search modal with arXiv integration
✅ Paper page with PDF viewer
✅ Draggable divider between PDF and Notes panels (20%-80% range)
✅ PDF zoom controls (+/- buttons, 50%-200%)
✅ CRUD notes with page numbers, tags, BlockNote editor
✅ Tag parsing and badge display
✅ BlockNote rich text editor (JSON storage)
✅ Note modal overlays only right panel (PDF remains visible)
✅ Read-only BlockNote display in note cards

### Out of Scope (Future)
❌ User authentication
❌ Multi-user support
❌ Cloud storage
❌ PDF annotations/highlights
❌ Export notes
❌ Search within papers
❌ Collections/folders

---

## Development Phases

### Phase 1: Backend API
1. Setup FastAPI project
2. Implement `/search` endpoint
3. Create database models (Paper, Note)
4. Implement CRUD endpoints

### Phase 2: Frontend Core
1. Setup Next.js project
2. Create Dashboard page
3. Implement Search modal
4. Integrate with backend API

### Phase 3: Paper Viewer
1. Create Paper page layout
2. Integrate react-pdf viewer
3. Implement resizable panels
4. Create notes list UI

### Phase 4: Notes System
1. Create Note modal with BlockNote
2. Implement page number parsing
3. Implement tag parsing and badges
4. Connect CRUD operations to backend

### Phase 5: Polish
1. Add loading states
2. Error handling
3. Confirmation dialogs
4. Responsive design
5. Testing

---

## Success Criteria

- ✅ User can search and add papers from arXiv
- ✅ User can view PDF in browser
- ✅ User can create notes with flexible page references
- ✅ User can add multiple tags displayed as badges
- ✅ User can write notes in markdown format
- ✅ User can edit and delete notes
- ✅ User can resize PDF/Notes panels
- ✅ All data persists in database
