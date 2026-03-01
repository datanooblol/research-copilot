'use client';

import { useState, useEffect } from 'react';
import { useRouter, useParams } from 'next/navigation';
import { Note, NoteCreate } from '@/types';
import { getNotes, createNote, updateNote, deleteNote, getDashboardPapers } from '@/lib/api';
import Button from '@/components/atoms/Button';
import NoteCard from '@/components/molecules/NoteCard';
import NoteModal from '@/components/organisms/NoteModal';
import PdfViewer from '@/components/organisms/PdfViewer';

export default function PaperPage() {
  const params = useParams();
  const router = useRouter();
  const paperId = params.id as string;
  
  const [notes, setNotes] = useState<Note[]>([]);
  const [loading, setLoading] = useState(true);
  const [showNoteModal, setShowNoteModal] = useState(false);
  const [editingNote, setEditingNote] = useState<Note | undefined>();
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

  const handleSaveNote = async (data: NoteCreate) => {
    try {
      if (editingNote) {
        await updateNote(editingNote.note_id, data);
      } else {
        await createNote(paperId, data);
      }
      await loadNotes();
      setShowNoteModal(false);
      setEditingNote(undefined);
    } catch (error) {
      console.error('Failed to save note:', error);
    }
  };

  const handleDeleteNote = async (noteId: string) => {
    if (!confirm('Delete this note?')) return;
    try {
      await deleteNote(noteId);
      setNotes(notes.filter(n => n.note_id !== noteId));
    } catch (error) {
      console.error('Failed to delete note:', error);
    }
  };

  const openEditModal = (note: Note) => {
    setEditingNote(note);
    setShowNoteModal(true);
  };

  const openAddModal = () => {
    setEditingNote(undefined);
    setShowNoteModal(true);
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
        <div style={{ width: `${100 - leftWidth}%` }} className="min-w-0 relative">
          <div className="h-full overflow-auto bg-white p-4">
            <div className="flex justify-between items-center mb-4">
              <h2 className="text-xl font-semibold">Notes</h2>
              <Button onClick={openAddModal}>+ Add Note</Button>
            </div>
            <div className="space-y-4">
              {notes.map(note => (
                <NoteCard
                  key={note.note_id}
                  note={note}
                  onEdit={() => openEditModal(note)}
                  onDelete={() => handleDeleteNote(note.note_id)}
                />
              ))}
            </div>
            {notes.length === 0 && (
              <p className="text-gray-500 text-center mt-8">No notes yet. Click "Add Note" to get started.</p>
            )}
          </div>
          {showNoteModal && (
            <div className="absolute inset-0 bg-white z-10">
              <NoteModal
                note={editingNote}
                onSave={handleSaveNote}
                onClose={() => {
                  setShowNoteModal(false);
                  setEditingNote(undefined);
                }}
              />
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
