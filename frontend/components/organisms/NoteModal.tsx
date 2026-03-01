'use client';

import { useState, useEffect } from 'react';
import { Note, NoteCreate } from '@/types';
import Input from '@/components/atoms/Input';
import Button from '@/components/atoms/Button';
import TagInput from '@/components/molecules/TagInput';
import { useCreateBlockNote } from '@blocknote/react';
import { BlockNoteView } from '@blocknote/mantine';
import '@blocknote/core/fonts/inter.css';
import '@blocknote/mantine/style.css';

interface NoteModalProps {
  note?: Note;
  onSave: (data: NoteCreate) => void;
  onClose: () => void;
}

export default function NoteModal({ note, onSave, onClose }: NoteModalProps) {
  const [page, setPage] = useState(note?.page || '');
  const [tags, setTags] = useState<string[]>(note?.tags || []);
  const [showConfirm, setShowConfirm] = useState(false);

  const editor = useCreateBlockNote({
    initialContent: note?.content ? JSON.parse(note.content) : undefined,
  });

  const handleSave = async () => {
    const content = JSON.stringify(editor.document);
    onSave({ page, tags, content });
  };

  return (
    <div className="relative h-full">
      <div className="h-full flex flex-col bg-white p-6 overflow-y-auto">
        <div className="flex justify-between items-center mb-4">
          <h2 className="text-2xl font-bold">{note ? 'Edit Note' : 'Add Note'}</h2>
          <button onClick={onClose} className="text-2xl">&times;</button>
        </div>
        <div className="space-y-4 flex-1">
          <div>
            <label className="block text-sm font-medium mb-1">Page Number</label>
            <Input
              value={page}
              onChange={(e) => setPage(e.target.value)}
              placeholder="e.g., 1, 3-5, 10"
            />
          </div>
          <div>
            <label className="block text-sm font-medium mb-1">Tags</label>
            <TagInput value={tags} onChange={setTags} />
          </div>
          <div className="flex-1">
            <label className="block text-sm font-medium mb-1">Note</label>
            <div className="border border-gray-300 rounded-md">
              <BlockNoteView editor={editor} theme="light" />
            </div>
          </div>
          <div className="flex gap-2 justify-end">
            <Button variant="secondary" onClick={onClose}>Cancel</Button>
            <Button onClick={() => setShowConfirm(true)}>Save</Button>
          </div>
        </div>
      </div>
      {showConfirm && (
        <div className="absolute inset-0 bg-black bg-opacity-50 flex items-center justify-center z-10">
          <div className="bg-white rounded-lg p-6 max-w-sm">
            <h3 className="text-lg font-semibold mb-4">Save this note?</h3>
            <div className="flex gap-2 justify-end">
              <Button variant="secondary" onClick={() => setShowConfirm(false)}>Cancel</Button>
              <Button onClick={handleSave}>Confirm</Button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
