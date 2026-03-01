'use client';

import { useState, useMemo } from 'react';
import { Document, Page, pdfjs } from 'react-pdf';
import 'react-pdf/dist/Page/AnnotationLayer.css';
import 'react-pdf/dist/Page/TextLayer.css';

pdfjs.GlobalWorkerOptions.workerSrc = `//unpkg.com/pdfjs-dist@${pdfjs.version}/build/pdf.worker.min.mjs`;

interface PdfViewerProps {
  url: string;
}

export default function PdfViewer({ url }: PdfViewerProps) {
  const [numPages, setNumPages] = useState<number>(0);
  const [scale, setScale] = useState(1.0);
  const file = useMemo(() => ({ url }), [url]);

  if (!url) return <div className="h-full flex items-center justify-center">Loading PDF...</div>;

  return (
    <div className="h-full flex flex-col bg-gray-100">
      <div className="flex gap-2 p-2 bg-white border-b">
        <button onClick={() => setScale(s => Math.max(0.5, s - 0.1))} className="px-3 py-1 bg-gray-200 rounded hover:bg-gray-300">-</button>
        <span className="px-3 py-1">{Math.round(scale * 100)}%</span>
        <button onClick={() => setScale(s => Math.min(2.0, s + 0.1))} className="px-3 py-1 bg-gray-200 rounded hover:bg-gray-300">+</button>
      </div>
      <div className="flex-1 overflow-auto p-4">
        <Document
          file={file}
          onLoadSuccess={({ numPages }) => setNumPages(numPages)}
          className="flex flex-col items-center gap-4"
        >
          {Array.from(new Array(numPages), (_, index) => (
            <Page key={`page_${index + 1}`} pageNumber={index + 1} scale={scale} />
          ))}
        </Document>
      </div>
    </div>
  );
}
