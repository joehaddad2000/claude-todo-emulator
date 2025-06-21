import json
from datetime import datetime
from pathlib import Path

from ..types import TaskStore
from .utils import add_to_gitignore, copy_cursor_rules, detect_workspace_path


class FilePersistence:
    """File-based persistence using JSON"""

    def __init__(self, workspace_path: str | None = None):
        if workspace_path:
            workspace_dir = Path(workspace_path)
        else:
            workspace_dir = detect_workspace_path()

        self.file_path = workspace_dir / ".mcp-todos.json"
        self.workspace_path = workspace_dir

    async def load(self) -> TaskStore:
        """Load task store from file, creating default if not exists"""
        if not self.file_path.exists():
            # Return default empty store
            return {
                "lastModified": datetime.now().isoformat(),
                "todos": [],
            }

        try:
            with open(self.file_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                # Ensure all required fields are present
                return {
                    "lastModified": data.get(
                        "lastModified", datetime.now().isoformat()
                    ),
                    "todos": data.get("todos", []),
                }
        except (json.JSONDecodeError, IOError):
            # If file is corrupted, just return empty store
            return {
                "lastModified": datetime.now().isoformat(),
                "todos": [],
            }

    async def save(self, store: TaskStore) -> None:
        """Save task store to file with atomic write"""
        is_first_time = not self.file_path.exists()

        # Write to temporary file first (atomic write)
        temp_path = self.file_path.with_suffix(".json.tmp")

        try:
            with open(temp_path, "w", encoding="utf-8") as f:
                json.dump(store, f, indent=2, ensure_ascii=False)

            # Atomic rename
            temp_path.replace(self.file_path)

            # First-time setup actions
            if is_first_time:
                # Add to .gitignore
                add_to_gitignore(self.workspace_path, ".mcp-todos.json")

                # Auto-copy Cursor rules file
                copy_cursor_rules(self.workspace_path)

        except Exception:
            # Clean up temp file if something went wrong
            if temp_path.exists():
                temp_path.unlink()
            raise

    async def clear(self) -> None:
        """Remove the state file"""
        if self.file_path.exists():
            self.file_path.unlink()
