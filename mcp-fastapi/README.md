# MCP + FastAPI Template

## Setup

```bash
python -m venv .venv
source .venv/bin/activate       # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

## Run the API

```bash
uvicorn app.api:app --host 0.0.0.0 --port 8000 --reload
```

API docs available at: http://127.0.0.1:8000/docs (local)

From another device on the same network, use:
`http://<your-ip>:8000/docs`

Data is now persisted locally in SQLite at `local.db`.

## API Endpoints

| Method | Route                    | Description       |
|--------|--------------------------|-------------------|
| GET    | /items                   | List all items    |
| GET    | /items/{id}              | Get item by ID    |
| POST   | /items                   | Create item       |
| POST   | /items/{id}/clone        | Clone item by ID  |
| DELETE | /items/{id}              | Delete item by ID |

## MCP Server

The MCP server in `app/mcp_server.py` exposes all API routes as tools
callable by AI assistants (VS Code Copilot agent mode, Claude Desktop, etc.).

**Requires the FastAPI server to be running first.**

Run standalone (for debugging):
```bash
python app/mcp_server.py
```

## VS Code Integration

The `.vscode/mcp.json` file registers the MCP server automatically.

1. Open this folder in VS Code
2. Open GitHub Copilot chat in **Agent mode**
3. Click the tools icon → the 5 tools will appear
  (list_items, get_item, create_item, clone_item, delete_item)

## Add to Claude Desktop

In `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "fastapi-mcp": {
      "command": "/absolute/path/to/.venv/bin/python",
      "args": ["/absolute/path/to/app/mcp_server.py"]
    }
  }
}
```

## Project Structure

```
mcp-fastapi/
├── app/
│   ├── api.py          # FastAPI routes
│   ├── db.py           # SQLAlchemy engine/session setup
│   ├── models.py       # SQLAlchemy ORM models
│   └── mcp_server.py   # MCP server (wraps the API)
├── .vscode/
│   └── mcp.json        # VS Code MCP registration
├── requirements.txt
├── local.db            # SQLite database file (created on first run)
└── README.md
```
