'use client';

import { useState, useEffect } from 'react';
import { useRouter, useParams } from 'next/navigation';
import { Note, NoteCreate } from '@/types';
import { getNotes, createNote, updateNote, deleteNote, getDashboardPapers, updateNotePosition } from '@/lib/api';
import Button from '@/components/atoms/Button';
import PdfViewer from '@/components/organisms/PdfViewer';
import NotesCanvas from '@/components/organisms/NotesCanvas';

export default function PaperPage() {
  const params = useParams();
  const router = useRouter();
  const paperId = params.id as string;
  
  const [notes, setNotes] = useState<Note[]>([]);
  const [loading, setLoading] = useState(true);
  const [pdfUrl, setPdfUrl] = useState('');
  const [leftWidth, setLeftWidth] = useState(60);
  const [isDragging, setIsDragging] = useState(false);

  useEffect(() => {
    loadNotes();
    loadPaperInfo();
  }, [paperId]);

  useEffect(() => {
    const handleMouseMove = (e: MouseEvent) => {
      if (isDragging) {
        const newWidth = (e.clientX / window.innerWidth) * 100;
        if (newWidth > 20 && newWidth < 80) {
          setLeftWidth(newWidth);
        }
      }
    };

    const handleMouseUp = () => {
      setIsDragging(false);
    };

    if (isDragging) {
      document.addEventListener('mousemove', handleMouseMove);
      document.addEventListener('mouseup', handleMouseUp);
    }

    return () => {
      document.removeEventListener('mousemove', handleMouseMove);
      document.removeEventListener('mouseup', handleMouseUp);
    };
  }, [isDragging]);

  const loadPaperInfo = async () => {
    try {
      const papers = await getDashboardPapers();
      const paper = papers.find(p => p.paper_id === paperId);
      if (paper) {
        setPdfUrl(paper.pdf_url);
      }
    } catch (error) {
      console.error('Failed to load paper info:', error);
    } finally {
      setLoading(false);
    }
  };

  const loadNotes = async () => {
    try {
      const data = await getNotes(paperId);
      setNotes(data);
    } catch (error) {
      console.error('Failed to load notes:', error);
    }
  };

  const handleSaveNote = async (noteId: string, data: { page?: string; tags?: string[]; content?: string }) => {
    try {
      await updateNote(noteId, data);
      await loadNotes();
    } catch (error) {
      console.error('Failed to save note:', error);
    }
  };

  const handleUpdatePosition = async (noteId: string, x: number, y: number, width?: number, height?: number) => {
    try {
      await updateNotePosition(noteId, { position_x: x, position_y: y, width, height });
    } catch (error) {
      console.error('Failed to update position:', error);
    }
  };

  const handleDeleteNote = async (noteId: string) => {
    if (!confirm('Delete this note?')) return;
    try {
      await deleteNote(noteId);
      await loadNotes();
    } catch (error) {
      console.error('Failed to delete note:', error);
    }
  };

  const handleAddNote = async () => {
    try {
      const randomX = Math.random() * 500;
      const randomY = Math.random() * 500;
      await createNote(paperId, {
        page: '',
        tags: [],
        content: JSON.stringify([{ type: 'paragraph', content: [] }]),
        position_x: randomX,
        position_y: randomY,
        width: 300,
        height: 200,
      });
      await loadNotes();
    } catch (error) {
      console.error('Failed to create note:', error);
    }
  };

  const handleMouseDown = () => {
    setIsDragging(true);
  };

  if (loading) return <div className="p-8">Loading...</div>;

  return (
    <div className="h-screen flex flex-col">
      <div className="bg-white border-b p-4 flex items-center gap-4">
        <Button variant="secondary" onClick={() => router.push('/dashboard')}>← Back</Button>
        <h1 className="text-xl font-semibold">Paper Viewer</h1>
      </div>
      <div className="flex h-full relative">
        <div style={{ width: `${leftWidth}%` }} className="min-w-0">
          <PdfViewer url={pdfUrl} />
        </div>
        <div 
          className="w-2 bg-gray-300 hover:bg-gray-400 cursor-col-resize flex-shrink-0"
          onMouseDown={handleMouseDown}
        />
        <div style={{ width: `${100 - leftWidth}%` }} className="min-w-0 relative bg-gray-50">
          <div className="absolute top-4 right-4 z-10">
            <Button onClick={handleAddNote}>+ Add Note</Button>
          </div>
          <NotesCanvas
            notes={notes}
            onUpdateNote={handleSaveNote}
            onUpdatePosition={handleUpdatePosition}
            onDeleteNote={handleDeleteNote}
          />
        </div>
      </div>
    </div>
  );
}
