# Research Copilot Frontend

Next.js 14+ frontend for the Research Copilot application.

## Setup

```bash
npm install
```

## Development

```bash
npm run dev
```

Open [http://localhost:3000](http://localhost:3000)

## Architecture

- **Design Tokens**: `tokens/` - colors, spacing, typography, shadows, breakpoints
- **Atomic Design**: `components/` - atoms, molecules, organisms, templates
- **Pages**: `app/` - dashboard, paper/[id]
- **API Client**: `lib/api.ts` - axios-based backend communication
- **Types**: `types/index.ts` - TypeScript interfaces

## Features

- Search and add papers from arXiv
- PDF viewer with resizable panels
- Rich text notes with BlockNote editor
- Tag management with badges
- Page number references (e.g., "1", "1,3", "1-5")
