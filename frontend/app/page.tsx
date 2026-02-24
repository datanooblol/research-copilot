"use client";

import { useCallback } from "react";
import ReactFlow, {
  Node,
  Edge,
  addEdge,
  Connection,
  useNodesState,
  useEdgesState,
  Background,
  Controls,
} from "reactflow";
import "reactflow/dist/style.css";
import NoteNode from "./components/NoteNode";
import PaperGroup from "./components/PaperGroup";

const nodeTypes = {
  noteNode: NoteNode,
  paperGroup: PaperGroup,
};

const initialNodes: Node[] = [
  {
    id: "1",
    type: "noteNode",
    position: { x: 250, y: 100 },
    data: { label: "Note 1" },
  },
];

const initialEdges: Edge[] = [];

export default function Home() {
  const [nodes, setNodes, onNodesChange] = useNodesState(initialNodes);
  const [edges, setEdges, onEdgesChange] = useEdgesState(initialEdges);

  const onConnect = useCallback(
    (params: Connection) => setEdges((eds) => addEdge(params, eds)),
    [setEdges]
  );

  const onNodeDragStop = useCallback(
    (_: any, node: Node) => {
      // Check if note is dropped inside a group
      if (node.type === "noteNode") {
        const groupNode = nodes.find(
          (n) =>
            n.type === "paperGroup" &&
            node.position.x >= n.position.x &&
            node.position.x <= n.position.x + 600 &&
            node.position.y >= n.position.y &&
            node.position.y <= n.position.y + 400
        );

        if (groupNode) {
          // Set parent and adjust position to be relative
          setNodes((nds) =>
            nds.map((n) =>
              n.id === node.id
                ? {
                    ...n,
                    parentNode: groupNode.id,
                    extent: "parent" as const,
                    position: {
                      x: node.position.x - groupNode.position.x,
                      y: node.position.y - groupNode.position.y,
                    },
                  }
                : n
            )
          );
        } else if (node.parentNode) {
          // Remove parent if dragged outside
          setNodes((nds) =>
            nds.map((n) =>
              n.id === node.id
                ? { ...n, parentNode: undefined, extent: undefined }
                : n
            )
          );
        }
      }
    },
    [nodes, setNodes]
  );

  const addPaperGroup = useCallback(() => {
    const newId = `group-${Date.now()}`;
    const newNode: Node = {
      id: newId,
      type: "paperGroup",
      position: { x: Math.random() * 400, y: Math.random() * 300 },
      data: {
        label: `Paper ${Math.floor(nodes.length / 2) + 1}`,
        onNameChange: (newName: string) => {
          setNodes((nds) =>
            nds.map((node) =>
              node.id === newId
                ? { ...node, data: { ...node.data, label: newName } }
                : node
            )
          );
        },
      },
      style: { zIndex: -1, width: 600, height: 400 },
    };
    setNodes((nds) => [...nds, newNode]);
  }, [nodes.length, setNodes]);

  const addNote = useCallback(() => {
    const newId = `${Date.now()}`;
    const groups = nodes.filter((n) => n.type === "paperGroup");
    const newNode: Node = {
      id: newId,
      type: "noteNode",
      position: { x: Math.random() * 500, y: Math.random() * 500 },
      data: {
        label: `Note ${nodes.length + 1}`,
        type: "general",
        assignedGroup: "",
        availableGroups: groups.map((g) => ({ id: g.id, label: g.data.label })),
        onTypeChange: (newType: string) => {
          setNodes((nds) =>
            nds.map((node) =>
              node.id === newId
                ? { ...node, data: { ...node.data, type: newType } }
                : node
            )
          );
        },
        onGroupAssign: (groupId: string) => {
          const targetGroup = nodes.find((n) => n.id === groupId);
          if (targetGroup) {
            setNodes((nds) =>
              nds.map((node) =>
                node.id === newId
                  ? {
                      ...node,
                      parentNode: groupId,
                      extent: "parent" as const,
                      position: { x: 50, y: 50 },
                      data: { ...node.data, assignedGroup: groupId },
                    }
                  : node
              )
            );
          } else if (groupId === "") {
            setNodes((nds) =>
              nds.map((node) =>
                node.id === newId
                  ? {
                      ...node,
                      parentNode: undefined,
                      extent: undefined,
                      data: { ...node.data, assignedGroup: "" },
                    }
                  : node
              )
            );
          }
        },
      },
    };
    setNodes((nds) => [...nds, newNode]);
  }, [nodes, setNodes]);

  return (
    <div style={{ width: "100vw", height: "100vh" }}>
      <button
        onClick={addPaperGroup}
        style={{
          position: "absolute",
          top: "10px",
          left: "130px",
          zIndex: 10,
          padding: "10px 20px",
          background: "#6b7280",
          color: "white",
          border: "none",
          borderRadius: "4px",
          cursor: "pointer",
          fontWeight: "bold",
        }}
      >
        + Add Paper Group
      </button>
      <button
        onClick={addNote}
        style={{
          position: "absolute",
          top: "10px",
          left: "10px",
          zIndex: 10,
          padding: "10px 20px",
          background: "#1a192b",
          color: "white",
          border: "none",
          borderRadius: "4px",
          cursor: "pointer",
          fontWeight: "bold",
        }}
      >
        + Add Note
      </button>
      <ReactFlow
        nodes={nodes}
        edges={edges}
        onNodesChange={onNodesChange}
        onEdgesChange={onEdgesChange}
        onConnect={onConnect}
        onNodeDragStop={onNodeDragStop}
        nodeTypes={nodeTypes}
        fitView
        minZoom={0.1}
        maxZoom={4}
      >
        <Background />
        <Controls />
      </ReactFlow>
    </div>
  );
}
