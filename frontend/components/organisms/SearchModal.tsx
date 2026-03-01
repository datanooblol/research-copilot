'use client';

import { useState } from 'react';
import { SearchResult } from '@/types';
import { searchPapers, addPaperToDashboard } from '@/lib/api';
import Input from '@/components/atoms/Input';
import Button from '@/components/atoms/Button';
import { useRouter } from 'next/navigation';

interface SearchModalProps {
  onClose: () => void;
}

export default function SearchModal({ onClose }: SearchModalProps) {
  const [query, setQuery] = useState('');
  const [results, setResults] = useState<SearchResult[]>([]);
  const [loading, setLoading] = useState(false);
  const router = useRouter();

  const handleSearch = async () => {
    if (!query.trim()) return;
    setLoading(true);
    try {
      const data = await searchPapers(query);
      setResults(data);
    } catch (error) {
      console.error('Search failed:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleAdd = async (result: SearchResult) => {
    try {
      const paper = await addPaperToDashboard({
        title: result.title,
        year: result.year,
        published: result.published,
        authors: result.authors,
        summary: result.summary,
        doi: result.doi,
        publisher: 'arxiv',
        entry_id: result.entry_id,
        pdf_url: result.pdf_url,
      });
      router.push(`/paper/${paper.paper_id}`);
      onClose();
    } catch (error) {
      console.error('Failed to add paper:', error);
    }
  };

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div className="bg-white rounded-lg p-6 w-full max-w-2xl max-h-[80vh] overflow-y-auto">
        <div className="flex justify-between items-center mb-4">
          <h2 className="text-2xl font-bold">Search Papers</h2>
          <button onClick={onClose} className="text-2xl">&times;</button>
        </div>
        <div className="flex gap-2 mb-4">
          <Input
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            onKeyDown={(e) => e.key === 'Enter' && handleSearch()}
            placeholder="Enter keywords..."
          />
          <Button onClick={handleSearch} disabled={loading}>
            {loading ? 'Searching...' : 'Search'}
          </Button>
        </div>
        <div className="space-y-4">
          {results.map(result => (
            <div key={result.id} className="p-4 border border-gray-200 rounded-lg">
              <h3 className="font-semibold mb-2">{result.title}</h3>
              <p className="text-sm text-gray-600 mb-1">Authors: {result.authors.join(', ')}</p>
              <p className="text-sm text-gray-600 mb-2">Year: {result.year}</p>
              <p className="text-sm text-gray-700 mb-3">{result.summary.slice(0, 200)}...</p>
              <Button onClick={() => handleAdd(result)}>Add</Button>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
