# Notes MCP Server

A Model Context Protocol (MCP) server for managing notes with an interactive web dashboard.

## Features

- **Note Management**: Create and list notes via MCP tools
- **Interactive Dashboard**: Web-based UI accessible through ChatGPT
- **Widget Rendering**: Dashboard loads via MCP widget resources

## Setup

### 1. Backend Setup
```bash
cd backend
uv sync
uv run python server.py
```

### 2. Ngrok Setup  
```bash
ngrok http 8000
```

### 3. Frontend Build
If you change any frontend files, rebuild the widget bundle:
```bash
cd frontend
npm install
npm run build
```
The server serves the widget from `frontend/dist/index.html`.

### 4. Add Sample Data (Optional)
```bash
cd backend
uv run python demo_data.py
```

## Usage

### MCP Tools (via ChatGPT)
- `create_note(title, content)` - Create a new note
- `list_notes()` - List all notes
- `open_dashboard()` - Open the dashboard widget

### Web Dashboard
- Visit `/dashboard` for the interactive UI
- Auto-loads notes on page load

## Files

- `server.py` - Main MCP server with web routes
- `database.py` - SQLite database operations  
- `notes.db` - SQLite database file
- `frontend/dist/index.html` - Dashboard UI bundle

## Architecture

The server combines:
- **FastMCP**: For MCP tool functionality
- **Starlette**: For web routes and API endpoints  
- **SQLite**: For note storage
- **Static HTML**: For the dashboard UI

The `open_dashboard` tool returns a widget response so ChatGPT can render the dashboard inline.

## Quick Start

Try these sample prompts with ChatGPT:

```
Create a note titled "Meeting Notes" with content "Discussed Q4 goals and project timelines"
```

```
Open my notes dashboard
```

For more examples, see [SAMPLE_PROMPTS.md](./SAMPLE_PROMPTS.md)
