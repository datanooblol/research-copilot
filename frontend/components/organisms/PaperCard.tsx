import { Paper } from '@/types';
import Button from '@/components/atoms/Button';

interface PaperCardProps {
  paper: Paper;
  onOpen: () => void;
  onDelete: () => void;
}

export default function PaperCard({ paper, onOpen, onDelete }: PaperCardProps) {
  return (
    <div className="p-4 border border-gray-200 rounded-lg bg-white hover:shadow-md transition-shadow">
      <h3 className="text-lg font-semibold mb-2">{paper.title}</h3>
      <p className="text-sm text-gray-600 mb-2">
        Authors: {paper.authors.join(', ')}
      </p>
      <p className="text-sm text-gray-600 mb-3">
        Year: {paper.year} | Notes: {paper.note_count || 0}
      </p>
      <div className="flex gap-2">
        <Button onClick={onOpen}>Open</Button>
        <Button variant="danger" onClick={onDelete}>Delete</Button>
      </div>
    </div>
  );
}
