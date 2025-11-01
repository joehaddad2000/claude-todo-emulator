from contextlib import asynccontextmanager
from typing import Any

from fastmcp import FastMCP

from .state.store import store
from .state.utils import copy_cursor_rules, update_agents_md
from .state.validators import ValidationError
from .tools.todo_read import todo_read
from .tools.todo_write import todo_write


@asynccontextmanager
async def lifespan(app: FastMCP):
    """Initialize store on startup to ensure .mcp-todos.json exists"""
    # Startup
    await store.initialize()

    # Force creation of the file and all associated setup if it doesn't exist
    if not store.persistence.file_path.exists():
        # Writing an empty todo list will trigger:
        # 1. Creation of .mcp-todos.json
        # 2. Adding to .gitignore
        # 3. Copying Cursor rules
        await store.write_todos([])

    # Always ensure rules files are up to date
    copy_cursor_rules(store.persistence.workspace_path)
    update_agents_md(store.persistence.workspace_path)

    yield

    # Shutdown (nothing to do)


# Create the MCP server
mcp = FastMCP(
    "Task Manager",
    instructions="Manages persistent todo lists with TodoRead and TodoWrite tools. TodoRead returns current todos, TodoWrite replaces entire list.",
    lifespan=lifespan,
)


@mcp.tool
async def TodoRead() -> dict[str, Any]:
    """
    Read the current task list.

    Returns a list of todos with their current state.
    """
    try:
        return await todo_read()
    except Exception as e:
        return {
            "error": {
                "code": "READ_ERROR",
                "message": f"Failed to read todos: {str(e)}",
            }
        }


@mcp.tool
async def TodoWrite(todos: list[dict[str, Any]]) -> dict[str, Any]:
    """
    Update the entire task list (complete replacement).

    Parameters:
        todos: List of todo items, each containing:
            - id: Unique identifier for the task
            - content: Task description
            - status: Current status (pending, in_progress, completed)
            - priority: Task priority (high, medium, low)
            - metadata: Optional additional data

    Returns success status and count of todos written.
    """
    try:
        return await todo_write({"todos": todos})
    except ValidationError as e:
        return {"error": {"code": "VALIDATION_ERROR", "message": str(e)}}
    except Exception as e:
        return {
            "error": {
                "code": "WRITE_ERROR",
                "message": f"Failed to write todos: {str(e)}",
            }
        }


def main():
    mcp.run()


if __name__ == "__main__":
    main()
