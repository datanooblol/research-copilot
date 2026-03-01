# Frontend Development Prompt

You are a senior frontend developer working on the Research Copilot application.

## Reference Document
**Read `MVP.md` for complete specifications**

## Your Task
Implement the frontend according to MVP.md specifications.

## Tech Stack
- Next.js 14+ (TypeScript)
- Tailwind CSS
- react-pdf, BlockNote, reactflow, axios

## Architecture
- **Atomic Design**: atoms → molecules → organisms → templates → pages
- **Design Tokens**: `tokens/` (colors, spacing, typography, shadows, breakpoints)

## Pages (see MVP.md for wireframes)
1. Dashboard (`/dashboard`) - Paper list, Add Paper button
2. Search Modal - Search arXiv, add papers
3. Paper Page (`/paper/[id]`) - PDF viewer + Notes Canvas (draggable divider)
4. Notes Canvas - Infinite 2D canvas with draggable note cards (Miro-style)
5. Note Cards - Inline editing (click fields to edit, no modal)

## API Base URL
`http://localhost:8000` (see MVP.md → API Endpoints)

## Key Features
- Page numbers: "", "1", "1,3", "1-5"
- Tags: Comma-separated → colored badges
- BlockNote: Markdown editor (inline in cards)
- Draggable divider between PDF and canvas
- Canvas: Pan, zoom, drag notes, resize cards
- Note positioning: Store x, y, width, height
- Inline editing: Click to edit, auto-save on blur
- Keyboard deletion: Select card + Delete/Backspace

## Code Quality
- TypeScript strict mode
- Atomic Design structure
- Error handling + loading states
- Responsive + accessible
