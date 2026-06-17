"use client";

import dynamic from "next/dynamic";

const MCPGraph = dynamic(() => import("./MCPGraph"), { ssr: false });

export default function MCPGraphClient() {
  return <MCPGraph />;
}
