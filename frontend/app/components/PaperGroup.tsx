"use client";

import { memo } from "react";
import { NodeResizer } from "reactflow";

function PaperGroup({ data }: { data: any }) {
  return (
    <>
      <NodeResizer minWidth={400} minHeight={300} />
      <div
        style={{
          padding: "20px",
          border: "3px dashed #9ca3af",
          borderRadius: "12px",
          background: "rgba(243, 244, 246, 0.5)",
          width: "100%",
          height: "100%",
        }}
      >
        <input
          type="text"
          value={data.label || "Paper Title"}
          onChange={(e) => data.onNameChange?.(e.target.value)}
          style={{
            fontSize: "18px",
            fontWeight: "bold",
            border: "none",
            background: "transparent",
            marginBottom: "10px",
            width: "100%",
            outline: "none",
          }}
          placeholder="Enter paper title..."
        />
        <div style={{ fontSize: "12px", color: "#6b7280", marginBottom: "10px" }}>
          Drag notes into this area or assign notes to "{data.label}"
        </div>
      </div>
    </>
  );
}

export default memo(PaperGroup);
