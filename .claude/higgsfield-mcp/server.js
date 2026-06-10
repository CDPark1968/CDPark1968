#!/usr/bin/env node
import { Server } from "@modelcontextprotocol/sdk/server/index.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import {
  CallToolRequestSchema,
  ListToolsRequestSchema,
} from "@modelcontextprotocol/sdk/types.js";
import { execFile } from "node:child_process";
import { promisify } from "node:util";

const execFileAsync = promisify(execFile);

async function runHF(args) {
  const hfPath = process.env.HF_BIN || "higgsfield";
  try {
    const { stdout, stderr } = await execFileAsync(hfPath, [...args, "--json"], {
      timeout: 120_000,
      env: { ...process.env },
    });
    return { ok: true, output: stdout || stderr };
  } catch (err) {
    return { ok: false, output: err.stderr || err.message };
  }
}

const server = new Server(
  { name: "higgsfield", version: "1.0.0" },
  { capabilities: { tools: {} } }
);

server.setRequestHandler(ListToolsRequestSchema, async () => ({
  tools: [
    {
      name: "hf_auth_token",
      description: "Print the current Higgsfield access token",
      inputSchema: { type: "object", properties: {} },
    },
    {
      name: "hf_auth_login",
      description: "Start browser-based device login for Higgsfield (prints a URL to visit)",
      inputSchema: { type: "object", properties: {} },
    },
    {
      name: "hf_model_list",
      description: "List all available Higgsfield AI models",
      inputSchema: {
        type: "object",
        properties: {
          video: { type: "boolean", description: "List only video models" },
          image: { type: "boolean", description: "List only image models" },
        },
      },
    },
    {
      name: "hf_generate_create",
      description: "Create an image or video generation job",
      inputSchema: {
        type: "object",
        required: ["model"],
        properties: {
          model: { type: "string", description: "Model name (e.g. nano_banana_2)" },
          prompt: { type: "string", description: "Text prompt" },
          image: { type: "string", description: "Upload ID of an input image" },
          negative_prompt: { type: "string", description: "Negative prompt" },
          width: { type: "number" },
          height: { type: "number" },
          steps: { type: "number" },
          seed: { type: "number" },
        },
      },
    },
    {
      name: "hf_generate_get",
      description: "Get details / status of a generation job",
      inputSchema: {
        type: "object",
        required: ["job_id"],
        properties: {
          job_id: { type: "string" },
        },
      },
    },
    {
      name: "hf_generate_wait",
      description: "Poll a generation job until it finishes and return the result",
      inputSchema: {
        type: "object",
        required: ["job_id"],
        properties: {
          job_id: { type: "string" },
        },
      },
    },
    {
      name: "hf_generate_list",
      description: "List recent generation jobs",
      inputSchema: {
        type: "object",
        properties: {
          limit: { type: "number", description: "Max number of jobs to return" },
        },
      },
    },
    {
      name: "hf_generate_cost",
      description: "Estimate the credit cost for a generation job without running it",
      inputSchema: {
        type: "object",
        required: ["model"],
        properties: {
          model: { type: "string" },
          prompt: { type: "string" },
        },
      },
    },
    {
      name: "hf_upload",
      description: "Upload a local file and return its upload ID for use in generation",
      inputSchema: {
        type: "object",
        required: ["file_path"],
        properties: {
          file_path: { type: "string", description: "Absolute path to the file to upload" },
        },
      },
    },
    {
      name: "hf_account",
      description: "Show Higgsfield account credits and recent transactions",
      inputSchema: { type: "object", properties: {} },
    },
  ],
}));

server.setRequestHandler(CallToolRequestSchema, async (req) => {
  const { name, arguments: args = {} } = req.params;

  let result;

  switch (name) {
    case "hf_auth_token":
      result = await runHF(["auth", "token"]);
      break;

    case "hf_auth_login":
      result = await runHF(["auth", "login"]);
      break;

    case "hf_model_list": {
      const flags = [];
      if (args.video) flags.push("--video");
      if (args.image) flags.push("--image");
      result = await runHF(["model", "list", ...flags]);
      break;
    }

    case "hf_generate_create": {
      const flags = [];
      if (args.prompt) flags.push("--prompt", args.prompt);
      if (args.image) flags.push("--image", args.image);
      if (args.negative_prompt) flags.push("--negative-prompt", args.negative_prompt);
      if (args.width) flags.push("--width", String(args.width));
      if (args.height) flags.push("--height", String(args.height));
      if (args.steps) flags.push("--steps", String(args.steps));
      if (args.seed) flags.push("--seed", String(args.seed));
      result = await runHF(["generate", "create", args.model, ...flags]);
      break;
    }

    case "hf_generate_get":
      result = await runHF(["generate", "get", args.job_id]);
      break;

    case "hf_generate_wait":
      result = await runHF(["generate", "wait", args.job_id]);
      break;

    case "hf_generate_list": {
      const flags = [];
      if (args.limit) flags.push("--limit", String(args.limit));
      result = await runHF(["generate", "list", ...flags]);
      break;
    }

    case "hf_generate_cost": {
      const flags = [];
      if (args.prompt) flags.push("--prompt", args.prompt);
      result = await runHF(["generate", "cost", args.model, ...flags]);
      break;
    }

    case "hf_upload":
      result = await runHF(["upload", args.file_path]);
      break;

    case "hf_account":
      result = await runHF(["account"]);
      break;

    default:
      return {
        content: [{ type: "text", text: `Unknown tool: ${name}` }],
        isError: true,
      };
  }

  return {
    content: [{ type: "text", text: result.output }],
    isError: !result.ok,
  };
});

const transport = new StdioServerTransport();
await server.connect(transport);
