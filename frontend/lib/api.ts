import axios from 'axios';
import { Paper, Note, NoteCreate, NoteUpdate, SearchResult } from '@/types';

const api = axios.create({
  baseURL: 'http://localhost:8000',
});

export const searchPapers = async (query: string, maxResults = 10) => {
  const { data } = await api.get<{ results: SearchResult[] }>('/search', {
    params: { query, max_results: maxResults },
  });
  return data.results;
};

export const getDashboardPapers = async () => {
  const { data } = await api.get<{ papers: Paper[] }>('/dashboard');
  return data.papers;
};

export const addPaperToDashboard = async (paperInfo: any) => {
  const { data } = await api.post<Paper>('/dashboard', { paper_info: paperInfo });
  return data;
};

export const deletePaper = async (paperId: string) => {
  const { data } = await api.delete<{ success: boolean }>(`/dashboard/${paperId}`);
  return data;
};

export const getNotes = async (paperId: string) => {
  const { data } = await api.get<{ notes: Note[] }>(`/papers/${paperId}/notes`);
  return data.notes;
};

export const createNote = async (paperId: string, note: NoteCreate) => {
  const { data } = await api.post<Note>(`/papers/${paperId}/notes`, note);
  return data;
};

export const updateNote = async (noteId: string, note: NoteUpdate) => {
  const { data } = await api.put<Note>(`/notes/${noteId}`, note);
  return data;
};

export const deleteNote = async (noteId: string) => {
  const { data } = await api.delete<{ success: boolean }>(`/notes/${noteId}`);
  return data;
};
