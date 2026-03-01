# research-copilot

A visual research tool for reading PDFs and taking interconnected notes on an infinite canvas.

## Concept

**Split-view interface:**
- **Left pane**: PDF viewer for reading research papers
- **Right pane**: Miro-like infinite canvas for visual note-taking

## Features

### PDF Viewer
- Upload and display PDF documents
- Navigate pages, zoom, search
- Read research papers side-by-side with notes

### Canvas (Miro-like)
- **Infinite canvas**: Pan and zoom freely
- **Note nodes**: Draggable cards containing rich text
- **Rich text editor**: BlockNote integration (Notion-like editing)
  - Headings, lists, code blocks, formatting
  - Embedded in each note node
- **Note types/tags**: Categorize notes (e.g., Objective, Methodology, Key Finding, Question)
  - Color-coded by type
  - Filter and organize visually
- **Connections**: Drag to link notes together
  - Visual arrows showing relationships between concepts
  - Label connections

## Tech Stack (Planned)

### Frontend
- **Next.js 14** (App Router)
- **react-pdf** or **@react-pdf-viewer/core** - PDF rendering
- **react-flow** - Canvas and node management
- **@blocknote/react** - Rich text editor

### Backend
- **FastAPI** (Python) - API server
- **SQLite** or JSON - Data persistence

### Data Model
```
Document:
  - id
  - filename
  - pdf_path
  - upload_date
  - canvas_state:
    - nodes: [{id, type, position, blockNoteContent, tags}]
    - edges: [{source, target, label}]
```

## Use Case

1. Upload a research paper (PDF)
2. Read the paper on the left pane
3. Create note nodes on the canvas as you read
4. Tag notes by type (methodology, findings, questions, etc.)
5. Connect related concepts by dragging links between notes
6. Build a visual knowledge graph of the paper

## Similar Tools
- Heptabase
- Scrintal
- Obsidian Canvas

## Current Status

This repository currently contains a TUI (Terminal UI) prototype for managing research papers. The vision is to evolve into the web-based canvas tool described above.
