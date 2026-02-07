# Docs Getting Started

*Documentation: E2E Test Documentation*

---

## Getting Started

**Source:** http://127.0.0.1:24427/docs/getting-started

# Getting Started
This guide will help you set up the project from scratch in under 5 minutes.
## Prerequisites
Before you begin, make sure you have the following installed:
* Node.js 18 or higher
* Python 3.10 or higher
* Docker (optional, for containerized deployment)
## Installation
Install the package using npm:
```bash
npm install anydocs-mcp
cd anydocs-mcp
npm run build
```
## Quick Start
Create a configuration file and start the server:
```javascript
import { createServer } from 'anydocs-mcp';
const server = createServer({
  docsPath: './docs',
  port: 3000
});
server.start();
console.log('MCP server running on port 3000');
```
## Verify Installation
Run the health check to make sure everything is working:
```bash
curl http://localhost:3000/health
# Expected: {"status": "ok", "docs_loaded": true}
```
If you see the expected output, congratulations! You're ready to start using AnyDocsMCP.

---

