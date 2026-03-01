'use client';

import { useState, useRef, useEffect } from 'react';
import { Handle, Position, NodeProps } from 'reactflow';
import { Note } from '@/types';
import Badge from '@/components/atoms/Badge';
import { useCreateBlockNote } from '@blocknote/react';
import { BlockNoteView } from '@blocknote/mantine';
import '@blocknote/mantine/style.css';

interface CanvasNoteCardData {
  note: Note;
  onUpdate: (noteId: string, data: { page?: string; tags?: string[]; content?: string }) => Promise<void>;
  onDelete: (noteId: string) => Promise<void>;
  isSelected: boolean;
}

export default function CanvasNoteCard({ data }: NodeProps<CanvasNoteCardData>) {
  const { note, onUpdate, isSelected } = data;
  const [isEditingPage, setIsEditingPage] = useState(false);
  const [isEditingTags, setIsEditingTags] = useState(false);
  const [pageValue, setPageValue] = useState(note.page);
  const [tagsValue, setTagsValue] = useState(note.tags.join(', '));
  const pageInputRef = useRef<HTMLInputElement>(null);
  const tagsInputRef = useRef<HTMLInputElement>(null);

  const editor = useCreateBlockNote({
    initialContent: note.content ? JSON.parse(note.content) : undefined,
  });

  useEffect(() => {
    if (isEditingPage && pageInputRef.current) {
      pageInputRef.current.focus();
    }
  }, [isEditingPage]);

  useEffect(() => {
    if (isEditingTags && tagsInputRef.current) {
      tagsInputRef.current.focus();
    }
  }, [isEditingTags]);

  const handlePageSave = async () => {
    if (pageValue !== note.page) {
      await onUpdate(note.note_id, { page: pageValue });
    }
    setIsEditingPage(false);
  };

  const handleTagsSave = async () => {
    const newTags = tagsValue.split(',').map(t => t.trim()).filter(t => t);
    if (JSON.stringify(newTags) !== JSON.stringify(note.tags)) {
      await onUpdate(note.note_id, { tags: newTags });
    }
    setIsEditingTags(false);
  };

  const handleContentBlur = async () => {
    const content = JSON.stringify(editor.document);
    if (content !== note.content) {
      await onUpdate(note.note_id, { content });
    }
  };

  return (
    <div 
      className={`bg-yellow-100 rounded-lg shadow-md border-2 ${isSelected ? 'border-blue-500' : 'border-yellow-200'} h-full flex flex-col`}
      style={{ minWidth: '250px', minHeight: '150px' }}
    >
      <div className="p-3 border-b border-yellow-200 bg-yellow-50 rounded-t-lg cursor-move">
        {isEditingPage ? (
          <input
            ref={pageInputRef}
            type="text"
            value={pageValue}
            onChange={(e) => setPageValue(e.target.value)}
            onBlur={handlePageSave}
            onKeyDown={(e) => {
              if (e.key === 'Enter') handlePageSave();
              if (e.key === 'Escape') {
                setPageValue(note.page);
                setIsEditingPage(false);
              }
            }}
            className="w-full px-2 py-1 text-sm border rounded"
            placeholder="Page (e.g., 1, 1-5, 1,3)"
          />
        ) : (
          <div 
            onClick={() => setIsEditingPage(true)}
            className="text-sm font-medium cursor-text hover:bg-yellow-100 px-2 py-1 rounded"
          >
            {note.page ? `Page: ${note.page}` : 'Click to add page'}
          </div>
        )}
      </div>

      <div className="p-3 border-b border-yellow-200">
        {isEditingTags ? (
          <input
            ref={tagsInputRef}
            type="text"
            value={tagsValue}
            onChange={(e) => setTagsValue(e.target.value)}
            onBlur={handleTagsSave}
            onKeyDown={(e) => {
              if (e.key === 'Enter') handleTagsSave();
              if (e.key === 'Escape') {
                setTagsValue(note.tags.join(', '));
                setIsEditingTags(false);
              }
            }}
            className="w-full px-2 py-1 text-sm border rounded"
            placeholder="Tags (comma-separated)"
          />
        ) : (
          <div 
            onClick={() => setIsEditingTags(true)}
            className="cursor-text hover:bg-yellow-100 px-2 py-1 rounded min-h-[28px]"
          >
            {note.tags.length > 0 ? (
              <div className="flex flex-wrap gap-1">
                {note.tags.map((tag, i) => (
                  <Badge key={i}>{tag}</Badge>
                ))}
              </div>
            ) : (
              <span className="text-sm text-gray-500">Click to add tags</span>
            )}
          </div>
        )}
      </div>

      <div className="flex-1 overflow-auto p-3">
        <div onBlur={handleContentBlur}>
          <BlockNoteView editor={editor} theme="light" />
        </div>
      </div>
    </div>
  );
}
