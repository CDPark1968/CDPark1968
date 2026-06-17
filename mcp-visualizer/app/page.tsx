import MCPGraphClient from "./components/MCPGraphClient";

export default function Home() {
  return (
    <div style={{ display: "flex", flexDirection: "column", height: "100vh", background: "#0f172a" }}>
      <header style={{
        padding: "16px 24px",
        borderBottom: "1px solid #1e293b",
        display: "flex",
        alignItems: "center",
        justifyContent: "space-between",
        flexShrink: 0,
      }}>
        <div>
          <h1 style={{ color: "#e2e8f0", fontSize: 20, fontWeight: 700, margin: 0 }}>
            MCP App Visualizer
          </h1>
          <p style={{ color: "#64748b", fontSize: 13, margin: "2px 0 0" }}>
            Model Context Protocol server connections
          </p>
        </div>
        <div style={{ display: "flex", gap: 16, alignItems: "center" }}>
          <div style={{ display: "flex", alignItems: "center", gap: 6 }}>
            <div style={{ width: 8, height: 8, borderRadius: "50%", background: "#22c55e", boxShadow: "0 0 6px #22c55e" }} />
            <span style={{ color: "#94a3b8", fontSize: 13 }}>7 servers connected</span>
          </div>
        </div>
      </header>
      <main style={{ flex: 1, minHeight: 0 }}>
        <MCPGraphClient />
      </main>
    </div>
  );
}
