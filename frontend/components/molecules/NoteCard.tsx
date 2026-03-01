import { Note } from '@/types';
import Badge from '@/components/atoms/Badge';
import Button from '@/components/atoms/Button';
import { useCreateBlockNote } from '@blocknote/react';
import { BlockNoteView } from '@blocknote/mantine';
import '@blocknote/core/fonts/inter.css';
import '@blocknote/mantine/style.css';

interface NoteCardProps {
  note: Note;
  onEdit: () => void;
  onDelete: () => void;
}

export default function NoteCard({ note, onEdit, onDelete }: NoteCardProps) {
  const editor = useCreateBlockNote({
    initialContent: JSON.parse(note.content),
    editable: false,
  });

  return (
    <div className="p-4 border border-gray-200 rounded-lg bg-white">
      {note.page && <div className="text-sm text-gray-600 mb-2">Page: {note.page}</div>}
      {note.tags.length > 0 && (
        <div className="flex flex-wrap gap-2 mb-2">
          {note.tags.map(tag => (
            <Badge key={tag}>{tag}</Badge>
          ))}
        </div>
      )}
      <div className="mb-3 pointer-events-none">
        <BlockNoteView editor={editor} theme="light" />
      </div>
      <div className="flex gap-2">
        <Button variant="secondary" onClick={onEdit} className="text-sm px-3 py-1">Edit</Button>
        <Button variant="danger" onClick={onDelete} className="text-sm px-3 py-1">Delete</Button>
      </div>
    </div>
  );
}
