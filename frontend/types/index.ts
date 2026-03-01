export interface Paper {
  id: string;
  paper_id: string;
  title: string;
  authors: string[];
  year: number;
  published: string;
  summary: string;
  doi: string | null;
  publisher: string;
  entry_id: string;
  pdf_url: string;
  created_at: string;
  note_count?: number;
}

export interface Note {
  id: string;
  note_id: string;
  paper_id: string;
  page: string;
  tags: string[];
  content: string;
  created_at: string;
  updated_at: string;
}

export interface NoteCreate {
  page: string;
  tags: string[];
  content: string;
}

export interface NoteUpdate {
  page?: string;
  tags?: string[];
  content?: string;
}

export interface SearchResult {
  id: string;
  title: string;
  authors: string[];
  year: number;
  published: string;
  summary: string;
  entry_id: string;
  pdf_url: string;
  doi: string | null;
}
