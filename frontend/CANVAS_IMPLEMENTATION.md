# Canvas-Based Notes Implementation

## Overview
The frontend has been upgraded from a linear notes list to a Miro-style canvas-based notes system using ReactFlow.

## Changes Made

### 1. Dependencies Added
- `reactflow` - For canvas-based note positioning and dragging

### 2. Type Updates (`types/index.ts`)
- Added position fields to `Note` interface:
  - `position_x: number`
  - `position_y: number`
  - `width: number`
  - `height: number`
- Added optional position fields to `NoteCreate`
- Created `NotePositionUpdate` interface for position updates

### 3. API Updates (`lib/api.ts`)
- Added `updateNotePosition()` function for PATCH `/notes/{note_id}/position`

### 4. New Components

#### `NotesCanvas.tsx` (Organism)
- Infinite 2D canvas using ReactFlow
- Pan and zoom controls
- Drag and drop note cards
- Keyboard deletion (select card + Delete/Backspace)
- Auto-saves position changes on drag end
- Handles node selection state

#### `CanvasNoteCard.tsx` (Organism)
- Custom ReactFlow node component
- Inline editing for all fields (no modal)
- Click-to-edit interaction:
  - Page field: Click to edit, supports "", "1", "1,3", "1-5"
  - Tags field: Click to edit comma-separated tags
  - Content field: BlockNote editor with auto-save on blur
- Visual selection indicator (blue border when selected)
- Yellow sticky-note styling

### 5. Updated Components

#### `app/paper/[id]/page.tsx`
- Removed `NoteModal` and linear notes list
- Added `NotesCanvas` component
- Simplified note creation (random position on canvas)
- Updated handlers for inline editing
- Add Note button positioned in top-right corner

#### `app/layout.tsx`
- Added Mantine CSS imports
- Wrapped app with `MantineProvider` for BlockNote
- Converted to client component

## Features

### Canvas Interactions
- **Pan**: Click and drag on empty canvas space
- **Zoom**: Use mouse wheel or zoom controls
- **Move Note**: Drag note card by header or empty space
- **Edit Field**: Click inside any field to edit inline
- **Delete Note**: Click card background (not in field) + press Delete/Backspace
- **Add Note**: Click "+ Add Note" button (creates at random position)

### Inline Editing
- **Page Field**: Click to edit, press Enter to save, Escape to cancel
- **Tags Field**: Click to edit, press Enter to save, Escape to cancel
- **Content Field**: Click to edit with BlockNote, auto-saves on blur
- No modal required - all editing happens directly on the card

### Auto-Save
- Position changes save automatically when drag ends
- Content saves on blur (clicking outside the editor)
- Page and tags save on Enter or blur

## Backend Compatibility
The backend already supports all required fields and endpoints:
- `POST /papers/{paper_id}/notes` - Accepts position fields
- `PATCH /notes/{note_id}/position` - Updates position and size
- `PUT /notes/{note_id}` - Updates content, page, tags

## Testing
1. Start backend: `cd backend && uvicorn main:app --reload`
2. Start frontend: `cd frontend && npm run dev`
3. Navigate to a paper page
4. Click "+ Add Note" to create notes
5. Drag notes around the canvas
6. Click fields to edit inline
7. Select a note and press Delete to remove it

## Future Enhancements
- Resize notes by dragging edges/corners
- Connect notes with lines/arrows
- Group notes together
- Search/filter notes on canvas
- Export canvas as image
