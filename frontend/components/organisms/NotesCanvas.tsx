'use client';

import { useCallback, useState, useEffect } from 'react';
import ReactFlow, {
  Node,
  Edge,
  Controls,
  Background,
  useNodesState,
  useEdgesState,
  NodeChange,
  applyNodeChanges,
} from 'reactflow';
import 'reactflow/dist/style.css';
import { Note } from '@/types';
import CanvasNoteCard from './CanvasNoteCard';

const nodeTypes = {
  noteCard: CanvasNoteCard,
};

interface NotesCanvasProps {
  notes: Note[];
  onUpdateNote: (noteId: string, data: { page?: string; tags?: string[]; content?: string }) => Promise<void>;
  onUpdatePosition: (noteId: string, x: number, y: number, width?: number, height?: number) => Promise<void>;
  onDeleteNote: (noteId: string) => Promise<void>;
}

export default function NotesCanvas({ notes, onUpdateNote, onUpdatePosition, onDeleteNote }: NotesCanvasProps) {
  const [nodes, setNodes, onNodesChange] = useNodesState([]);
  const [edges] = useEdgesState([]);
  const [selectedNodeId, setSelectedNodeId] = useState<string | null>(null);

  useEffect(() => {
    const flowNodes: Node[] = notes.map(note => ({
      id: note.note_id,
      type: 'noteCard',
      position: { x: note.position_x, y: note.position_y },
      data: { 
        note,
        onUpdate: onUpdateNote,
        onDelete: onDeleteNote,
        isSelected: selectedNodeId === note.note_id,
      },
      style: {
        width: note.width,
        height: note.height,
      },
    }));
    setNodes(flowNodes);
  }, [notes, selectedNodeId]);

  const handleNodesChange = useCallback(
    (changes: NodeChange[]) => {
      setNodes((nds) => {
        const updatedNodes = applyNodeChanges(changes, nds);
        
        changes.forEach((change) => {
          if (change.type === 'position' && change.position && !change.dragging) {
            const node = nds.find(n => n.id === change.id);
            if (node) {
              onUpdatePosition(
                change.id,
                change.position.x,
                change.position.y,
                node.style?.width as number,
                node.style?.height as number
              );
            }
          }
          if (change.type === 'dimensions' && change.dimensions) {
            const node = nds.find(n => n.id === change.id);
            if (node) {
              onUpdatePosition(
                change.id,
                node.position.x,
                node.position.y,
                change.dimensions.width,
                change.dimensions.height
              );
            }
          }
        });
        
        return updatedNodes;
      });
    },
    [onUpdatePosition]
  );

  const handleNodeClick = useCallback((_: React.MouseEvent, node: Node) => {
    setSelectedNodeId(node.id);
  }, []);

  const handlePaneClick = useCallback(() => {
    setSelectedNodeId(null);
  }, []);

  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      if (selectedNodeId && (e.key === 'Delete' || e.key === 'Backspace')) {
        const activeElement = document.activeElement;
        if (activeElement?.tagName !== 'INPUT' && activeElement?.tagName !== 'TEXTAREA' && !activeElement?.hasAttribute('contenteditable')) {
          e.preventDefault();
          onDeleteNote(selectedNodeId);
          setSelectedNodeId(null);
        }
      }
    };

    window.addEventListener('keydown', handleKeyDown);
    return () => window.removeEventListener('keydown', handleKeyDown);
  }, [selectedNodeId, onDeleteNote]);

  return (
    <div className="w-full h-full">
      <ReactFlow
        nodes={nodes}
        edges={edges}
        onNodesChange={handleNodesChange}
        onNodeClick={handleNodeClick}
        onPaneClick={handlePaneClick}
        nodeTypes={nodeTypes}
        fitView
        minZoom={0.1}
        maxZoom={2}
      >
        <Controls />
        <Background />
      </ReactFlow>
    </div>
  );
}
