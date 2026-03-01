'use client';

import { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { Paper } from '@/types';
import { getDashboardPapers, deletePaper } from '@/lib/api';
import Button from '@/components/atoms/Button';
import PaperCard from '@/components/organisms/PaperCard';
import SearchModal from '@/components/organisms/SearchModal';

export default function DashboardPage() {
  const [papers, setPapers] = useState<Paper[]>([]);
  const [loading, setLoading] = useState(true);
  const [showSearch, setShowSearch] = useState(false);
  const router = useRouter();

  useEffect(() => {
    loadPapers();
  }, []);

  const loadPapers = async () => {
    try {
      const data = await getDashboardPapers();
      setPapers(data);
    } catch (error) {
      console.error('Failed to load papers:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleDelete = async (paperId: string) => {
    if (!confirm('Delete this paper?')) return;
    try {
      await deletePaper(paperId);
      setPapers(papers.filter(p => p.paper_id !== paperId));
    } catch (error) {
      console.error('Failed to delete paper:', error);
    }
  };

  if (loading) return <div className="p-8">Loading...</div>;

  return (
    <div className="min-h-screen bg-gray-50 p-8">
      <div className="max-w-6xl mx-auto">
        <div className="flex justify-between items-center mb-8">
          <h1 className="text-3xl font-bold">Research Copilot</h1>
          <Button onClick={() => setShowSearch(true)}>+ Add Paper</Button>
        </div>
        <h2 className="text-2xl font-semibold mb-4">My Papers</h2>
        <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
          {papers.map(paper => (
            <PaperCard
              key={paper.paper_id}
              paper={paper}
              onOpen={() => router.push(`/paper/${paper.paper_id}`)}
              onDelete={() => handleDelete(paper.paper_id)}
            />
          ))}
        </div>
        {papers.length === 0 && (
          <p className="text-gray-500 text-center mt-8">No papers yet. Click "Add Paper" to get started.</p>
        )}
      </div>
      {showSearch && <SearchModal onClose={() => setShowSearch(false)} />}
    </div>
  );
}
