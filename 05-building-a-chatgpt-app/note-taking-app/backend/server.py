from typing import List, Dict, Any
from pathlib import Path

import mcp.types as types
from mcp.server.fastmcp import FastMCP
from starlette.responses import HTMLResponse
from starlette.routing import Route
import database

database.init_db()

WIDGET_URI = "ui://widget/notes.html"
MIME_TYPE = "text/html+skybridge"

def _load_widget_html() -> str:
    """Load the React notes widget HTML."""
    try:
        current_dir = Path(__file__).resolve().parent
        react_build_path = current_dir / ".." / "frontend" / "dist" / "index.html"
        if react_build_path.exists():
            return react_build_path.read_text(encoding="utf-8")
        
        return "<h1>Error: Widget not found. Please run 'npm run build' in the frontend directory.</h1>"
    except Exception as e:
        return f"<h1>Error loading widget: {str(e)}</h1>"

def _tool_meta() -> Dict[str, Any]:
    """Tool metadata following the ChatGPT Apps SDK pattern."""
    return {
        "openai/outputTemplate": WIDGET_URI,
        "openai/toolInvocation/invoking": "Loading notes...",
        "openai/toolInvocation/invoked": "Notes loaded", 
        "openai/widgetAccessible": True,
        "openai/widgetPrefersBorder": True,
        "openai/widgetDomain": "https://chatgpt.com",
        "openai/widgetCSP": {
            "connect_domains": ["https://chatgpt.com"],
            "resource_domains": ["https://*.oaistatic.com"]
        }
    }

mcp = FastMCP(
    name="NoteTakerPro",
    stateless_http=True,
)

def _fetch_note_summaries() -> List[Dict[str, Any]]:
    notes = database.execute_query("SELECT id, title, content, created_at FROM notes")
    return [
        {
            "id": note["id"],
            "title": note["title"],
            "content": note["content"],
            "created_at": note["created_at"],
        }
        for note in notes
    ]

@mcp.tool()
def create_note(title: str, content: str) -> types.CallToolResult:
    """Create a new note with a title and content."""
    
    try:
        title = title.strip()
        content = content.strip()
        recent_notes = database.execute_query(
            "SELECT id, title, content FROM notes WHERE title = ? AND content = ? ORDER BY created_at DESC LIMIT 1",
            (title, content)
        )
        if recent_notes:
            structured_notes = _fetch_note_summaries()
            return types.CallToolResult(
                content=[types.TextContent(
                    type="text", 
                    text=f"Note '{title}' already exists (ID {recent_notes[0]['id']})"
                )],
                structuredContent={"notes": structured_notes, "count": len(structured_notes)},
                _meta={"openai/outputTemplate": WIDGET_URI, "openai/widgetAccessible": True}
            )
        
        
        note_id = database.execute_query(
            "INSERT INTO notes (title, content) VALUES (?, ?)",
            (title, content)
        )
        
        structured_notes = _fetch_note_summaries()
        
        result = types.CallToolResult(
            content=[types.TextContent(
                type="text", 
                text=f"Created note '{title}' with ID {note_id}"
            )],
            structuredContent={"notes": structured_notes, "count": len(structured_notes)},
            _meta={"openai/outputTemplate": WIDGET_URI, "openai/widgetAccessible": True}
        )
        return result
        
    except Exception as e:
        return types.CallToolResult(
            content=[types.TextContent(type="text", text=f"Error creating note: {str(e)}")],
            isError=True
        )



@mcp.tool()
def list_notes() -> types.CallToolResult:
    """List all notes metadata (id, title)."""
    
    try:
        structured_notes = _fetch_note_summaries()
        
        message = f"Found {len(structured_notes)} notes" if structured_notes else "No notes found"
        
        result = types.CallToolResult(
            content=[types.TextContent(
                type="text", 
                text=message
            )],
            structuredContent={"notes": structured_notes, "count": len(structured_notes)},
            _meta={"openai/outputTemplate": WIDGET_URI, "openai/widgetAccessible": True}
        )
        return result
    except Exception as e:
        return types.CallToolResult(
            content=[types.TextContent(type="text", text=f"Error retrieving notes: {str(e)}")],
            isError=True
        )



@mcp._mcp_server.list_resources()
async def _list_resources() -> List[types.Resource]:
    """List available resources including the widget."""
    resources = [
        types.Resource(
            name="Notes Widget",
            title="AI Notes Dashboard",
            uri=WIDGET_URI,
            description="Interactive notes management widget built with React",
            mimeType=MIME_TYPE,
            _meta={
                "openai/widgetPrefersBorder": True,
                "openai/widgetDomain": "https://chatgpt.com",
                "openai/widgetCSP": {
                    "connect_domains": ["https://chatgpt.com"],
                    "resource_domains": ["https://*.oaistatic.com"]
                }
            },
        )
    ]
    return resources

async def _handle_read_resource(req: types.ReadResourceRequest) -> types.ServerResult:
    """Handle resource read requests for the widget."""
    
    if str(req.params.uri) != WIDGET_URI:
        return types.ServerResult(
            types.ReadResourceResult(
                contents=[],
                _meta={"error": f"Unknown resource: {req.params.uri}"},
            )
        )

    html_content = _load_widget_html()
    
    contents = [
        types.TextResourceContents(
            uri=WIDGET_URI,
            mimeType=MIME_TYPE,
            text=html_content,
            _meta={
                "openai/widgetPrefersBorder": True,
                "openai/widgetDomain": "https://chatgpt.com",
                "openai/widgetCSP": {
                    "connect_domains": ["https://chatgpt.com"],
                    "resource_domains": ["https://*.oaistatic.com"]
                }
            },
        )
    ]

    return types.ServerResult(types.ReadResourceResult(contents=contents))


@mcp.tool()
async def open_dashboard() -> types.CallToolResult:
    """Open the interactive notes dashboard widget."""
    try:
        notes = database.execute_query("SELECT id, title, content, created_at FROM notes")
        notes_count = len(notes)

        meta = _tool_meta()
        meta["openai/toolInvocation/invoking"] = "Opening dashboard"
        meta["openai/toolInvocation/invoked"] = "Opened dashboard"

        return types.CallToolResult(
            content=[
                types.TextContent(
                    type="text",
                    text=(
                        "Your Notes Dashboard is available."
                    ),
                )
            ],
            _meta=meta,
        )
    except Exception as e:
        error_msg = f"Error opening dashboard: {str(e)}"
        return types.CallToolResult(
            content=[types.TextContent(type="text", text=error_msg)],
            isError=True,
        )

@mcp._mcp_server.list_tools()
async def _list_tools() -> List[types.Tool]:
    """List available tools."""
    return [
        types.Tool(
            name="create_note",
            title="Create Note",
            description="Create a new note with a title and content.",
            inputSchema={
                "type": "object",
                "properties": {
                    "title": {"type": "string"},
                    "content": {"type": "string"},
                },
                "required": ["title", "content"],
                "additionalProperties": False,
            },
            _meta=_tool_meta(),
        ),
        types.Tool(
            name="list_notes",
            title="List Notes",
            description="List all notes.",
            inputSchema={
                "type": "object",
                "properties": {},
                "additionalProperties": False,
            },
            _meta=_tool_meta(),
        ),
        types.Tool(
            name="open_dashboard",
            title="Open Notes Dashboard",
            description="Open the interactive notes dashboard widget.",
            inputSchema={
                "type": "object",
                "properties": {},
                "additionalProperties": False,
            },
            _meta=_tool_meta(),
        ),
    ]

mcp._mcp_server.request_handlers[types.ReadResourceRequest] = _handle_read_resource

async def dashboard_page(request):
    """Serve the dashboard HTML page."""
    html_content = _load_widget_html()
    return HTMLResponse(html_content)


app = mcp.streamable_http_app()

dashboard_routes = [
    Route("/dashboard", dashboard_page),
]

for route in dashboard_routes:
    app.routes.append(route)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
