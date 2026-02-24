"use client";

import { memo } from "react";
import { Handle, Position } from "reactflow";

const noteTypes = [
  { value: "objective", label: "Objective", color: "#3b82f6" },
  { value: "methodology", label: "Methodology", color: "#10b981" },
  { value: "finding", label: "Key Finding", color: "#f59e0b" },
  { value: "question", label: "Question", color: "#ef4444" },
  { value: "general", label: "General", color: "#6b7280" },
];

function NoteNode({ data }: { data: any }) {
  const currentType = noteTypes.find((t) => t.value === data.type) || noteTypes[4];

  return (
    <div
      style={{
        padding: "10px",
        border: `2px solid ${currentType.color}`,
        borderRadius: "8px",
        background: "white",
        minWidth: "300px",
        minHeight: "200px",
      }}
    >
      <Handle type="target" position={Position.Top} />
      <div style={{ marginBottom: "8px", display: "flex", justifyContent: "space-between", alignItems: "center" }}>
        <span style={{ fontWeight: "bold" }}>{data.label}</span>
        <select
          style={{
            padding: "4px 8px",
            borderRadius: "4px",
            border: `1px solid ${currentType.color}`,
            background: currentType.color,
            color: "white",
            fontSize: "12px",
            cursor: "pointer",
          }}
          value={data.type || "general"}
          onChange={(e) => data.onTypeChange?.(e.target.value)}
        >
          {noteTypes.map((type) => (
            <option key={type.value} value={type.value}>
              {type.label}
            </option>
          ))}
        </select>
      </div>
      <div style={{ marginBottom: "8px", display: "flex", gap: "8px", alignItems: "center" }}>
        <label style={{ fontSize: "12px", color: "#666" }}>Assign to:</label>
        <select
          style={{
            padding: "4px 8px",
            border: "1px solid #ddd",
            borderRadius: "4px",
            fontSize: "12px",
            flex: 1,
          }}
          value={data.assignedGroup || ""}
          onChange={(e) => data.onGroupAssign?.(e.target.value)}
        >
          <option value="">None</option>
          {data.availableGroups?.map((group: any) => (
            <option key={group.id} value={group.id}>
              {group.label}
            </option>
          ))}
        </select>
      </div>
      <div style={{ marginBottom: "8px", display: "flex", gap: "8px", alignItems: "center" }}>
        <label style={{ fontSize: "12px", color: "#666" }}>Page:</label>
        <input
          type="text"
          placeholder="e.g., 5 or 3-7"
          defaultValue={data.page || ""}
          style={{
            padding: "4px 8px",
            border: "1px solid #ddd",
            borderRadius: "4px",
            fontSize: "12px",
            width: "80px",
          }}
        />
      </div>
      <textarea
        style={{
          width: "100%",
          minHeight: "150px",
          border: "1px solid #ddd",
          borderRadius: "4px",
          padding: "8px",
          fontFamily: "inherit",
          resize: "none",
        }}
        placeholder="Type your notes here..."
        defaultValue={data.content || ""}
      />
      <Handle type="source" position={Position.Bottom} />
    </div>
  );
}

export default memo(NoteNode);
