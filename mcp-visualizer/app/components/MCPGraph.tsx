"use client";

import { useCallback, useState } from "react";
import ReactFlow, {
  Node,
  Edge,
  Controls,
  MiniMap,
  Background,
  BackgroundVariant,
  useNodesState,
  useEdgesState,
  addEdge,
  Connection,
  NodeTypes,
} from "reactflow";

const SERVER_COLORS: Record<string, string> = {
  filesystem: "#3b82f6",
  github: "#8b5cf6",
  notion: "#06b6d4",
  airtable: "#10b981",
  gmail: "#ef4444",
  calendar: "#f59e0b",
  claude: "#f97316",
};

interface MCPServer {
  id: string;
  name: string;
  type: string;
  status: "connected" | "connecting" | "disconnected";
  tools: string[];
  description: string;
}

const MCP_SERVERS: MCPServer[] = [
  {
    id: "claude-code-remote",
    name: "Claude Code Remote",
    type: "claude",
    status: "connected",
    tools: ["list_repos", "add_repo", "send_later"],
    description: "Remote execution environment management",
  },
  {
    id: "github",
    name: "GitHub",
    type: "github",
    status: "connected",
    tools: ["get_file_contents", "push_files", "create_pull_request", "list_issues", "add_issue_comment"],
    description: "GitHub repository operations",
  },
  {
    id: "notion",
    name: "Notion",
    type: "notion",
    status: "connected",
    tools: ["notion-fetch", "notion-create-pages", "notion-search", "notion-update-page"],
    description: "Notion workspace integration",
  },
  {
    id: "airtable",
    name: "Airtable",
    type: "airtable",
    status: "connected",
    tools: ["list_bases", "list_tables_for_base", "create_records_for_table", "search_records"],
    description: "Airtable database operations",
  },
  {
    id: "gmail",
    name: "Gmail",
    type: "gmail",
    status: "connected",
    tools: ["search_threads", "get_thread", "create_draft", "list_labels"],
    description: "Gmail email management",
  },
  {
    id: "google-calendar",
    name: "Google Calendar",
    type: "calendar",
    status: "connected",
    tools: ["list_calendars", "list_events", "create_event", "update_event"],
    description: "Google Calendar scheduling",
  },
  {
    id: "google-drive",
    name: "Google Drive",
    type: "filesystem",
    status: "connected",
    tools: ["search_files", "read_file_content", "create_file", "download_file_content"],
    description: "Google Drive file operations",
  },
];

function ServerNode({ data }: { data: MCPServer & { selected: boolean; onSelect: (id: string) => void } }) {
  const color = SERVER_COLORS[data.type] ?? "#64748b";
  const statusColors = {
    connected: "#22c55e",
    connecting: "#f59e0b",
    disconnected: "#ef4444",
  };

  return (
    <div
      onClick={() => data.onSelect(data.id)}
      className="cursor-pointer"
      style={{
        background: "#1e293b",
        border: `2px solid ${data.selected ? "#ffffff" : color}`,
        borderRadius: "12px",
        padding: "12px 16px",
        minWidth: "180px",
        boxShadow: data.selected ? `0 0 20px ${color}60` : `0 0 10px ${color}30`,
        transition: "all 0.2s",
      }}
    >
      <div className="flex items-center gap-2 mb-1">
        <div
          style={{
            width: 8,
            height: 8,
            borderRadius: "50%",
            background: statusColors[data.status],
            boxShadow: `0 0 6px ${statusColors[data.status]}`,
          }}
        />
        <span style={{ color, fontWeight: 700, fontSize: 13 }}>{data.name}</span>
      </div>
      <div style={{ color: "#64748b", fontSize: 11 }}>{data.tools.length} tools</div>
    </div>
  );
}

const nodeTypes: NodeTypes = { server: ServerNode };

function buildGraph(servers: MCPServer[], selectedId: string | null, onSelect: (id: string) => void) {
  const centerX = 500;
  const centerY = 300;
  const radius = 250;

  const nodes: Node[] = [
    {
      id: "claude",
      type: "server",
      position: { x: centerX - 90, y: centerY - 40 },
      data: {
        id: "claude",
        name: "Claude Code",
        type: "claude",
        status: "connected",
        tools: ["All MCP Tools"],
        description: "AI assistant orchestrating all MCP servers",
        selected: selectedId === "claude",
        onSelect,
      },
    },
    ...servers.map((server, i) => {
      const angle = (i / servers.length) * 2 * Math.PI - Math.PI / 2;
      return {
        id: server.id,
        type: "server",
        position: {
          x: centerX + radius * Math.cos(angle) - 90,
          y: centerY + radius * Math.sin(angle) - 40,
        },
        data: { ...server, selected: selectedId === server.id, onSelect },
      };
    }),
  ];

  const edges: Edge[] = servers.map((server) => ({
    id: `claude-${server.id}`,
    source: "claude",
    target: server.id,
    style: {
      stroke: SERVER_COLORS[server.type] ?? "#64748b",
      strokeWidth: selectedId === server.id ? 3 : 1.5,
      opacity: selectedId && selectedId !== server.id ? 0.3 : 0.8,
    },
    animated: server.status === "connected",
  }));

  return { nodes, edges };
}

interface SidebarProps {
  server: MCPServer | null;
  onClose: () => void;
}

function Sidebar({ server, onClose }: SidebarProps) {
  if (!server) return null;
  const color = SERVER_COLORS[server.type] ?? "#64748b";

  return (
    <div
      style={{
        position: "absolute",
        right: 16,
        top: 16,
        bottom: 16,
        width: 280,
        background: "#1e293b",
        border: `1px solid ${color}40`,
        borderRadius: 12,
        padding: 20,
        zIndex: 10,
        overflowY: "auto",
        boxShadow: `0 0 30px ${color}20`,
      }}
    >
      <div className="flex justify-between items-start mb-4">
        <div>
          <div style={{ color, fontWeight: 700, fontSize: 16 }}>{server.name}</div>
          <div style={{ color: "#64748b", fontSize: 12, marginTop: 4 }}>{server.description}</div>
        </div>
        <button onClick={onClose} style={{ color: "#64748b", fontSize: 18, lineHeight: 1 }}>✕</button>
      </div>

      <div style={{ marginBottom: 16 }}>
        <div style={{ color: "#94a3b8", fontSize: 11, fontWeight: 600, textTransform: "uppercase", letterSpacing: 1, marginBottom: 8 }}>
          Status
        </div>
        <div style={{
          display: "inline-flex", alignItems: "center", gap: 6,
          background: "#0f172a", borderRadius: 6, padding: "4px 10px",
        }}>
          <div style={{
            width: 6, height: 6, borderRadius: "50%",
            background: server.status === "connected" ? "#22c55e" : "#ef4444",
          }} />
          <span style={{ color: "#e2e8f0", fontSize: 12, textTransform: "capitalize" }}>{server.status}</span>
        </div>
      </div>

      <div>
        <div style={{ color: "#94a3b8", fontSize: 11, fontWeight: 600, textTransform: "uppercase", letterSpacing: 1, marginBottom: 8 }}>
          Tools ({server.tools.length})
        </div>
        <div style={{ display: "flex", flexDirection: "column", gap: 6 }}>
          {server.tools.map((tool) => (
            <div
              key={tool}
              style={{
                background: "#0f172a",
                borderRadius: 6,
                padding: "6px 10px",
                color: "#94a3b8",
                fontSize: 12,
                fontFamily: "monospace",
                border: `1px solid ${color}20`,
              }}
            >
              {tool}
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}

export default function MCPGraph() {
  const [selectedId, setSelectedId] = useState<string | null>(null);

  const selectedServer = selectedId
    ? MCP_SERVERS.find((s) => s.id === selectedId) ?? null
    : null;

  const { nodes: initialNodes, edges: initialEdges } = buildGraph(MCP_SERVERS, selectedId, setSelectedId);
  const [nodes, , onNodesChange] = useNodesState(initialNodes);
  const [edges, , onEdgesChange] = useEdgesState(initialEdges);

  const onConnect = useCallback(
    (params: Connection) => {
      // read-only graph
      void params;
    },
    []
  );

  const refreshedNodes = nodes.map((n) => ({
    ...n,
    data: { ...n.data, selected: n.id === selectedId, onSelect: setSelectedId },
  }));

  const refreshedEdges = edges.map((e) => ({
    ...e,
    style: {
      ...e.style,
      strokeWidth: selectedId === e.target ? 3 : 1.5,
      opacity: selectedId && selectedId !== e.target ? 0.3 : 0.8,
    },
  }));

  return (
    <div style={{ width: "100%", height: "100%", position: "relative" }}>
      <ReactFlow
        nodes={refreshedNodes}
        edges={refreshedEdges}
        onNodesChange={onNodesChange}
        onEdgesChange={onEdgesChange}
        onConnect={onConnect}
        nodeTypes={nodeTypes}
        fitView
        minZoom={0.3}
        maxZoom={2}
      >
        <Background variant={BackgroundVariant.Dots} color="#1e293b" gap={20} />
        <Controls />
        <MiniMap
          nodeColor={(n) => SERVER_COLORS[(n.data as MCPServer).type] ?? "#64748b"}
          maskColor="rgba(15,23,42,0.8)"
        />
      </ReactFlow>

      <Sidebar
        server={selectedServer}
        onClose={() => setSelectedId(null)}
      />

      <div style={{
        position: "absolute",
        bottom: 16,
        left: "50%",
        transform: "translateX(-50%)",
        color: "#475569",
        fontSize: 12,
        pointerEvents: "none",
      }}>
        {selectedId ? "Click background to deselect" : "Click a server node to see tools"}
      </div>
    </div>
  );
}
