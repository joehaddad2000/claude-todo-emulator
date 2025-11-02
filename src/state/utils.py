import os
from importlib.resources import files
from pathlib import Path


def detect_workspace_path() -> Path:
    """
    Detect the workspace directory from environment variables.
    Falls back to current working directory if not found.
    """
    # Try to detect workspace from Cursor's environment variable
    workspace_env = os.environ.get("WORKSPACE_FOLDER_PATHS")
    if workspace_env:
        # WORKSPACE_FOLDER_PATHS might contain multiple paths, take the first one
        workspace_path = workspace_env.split(",")[0].strip()
        return Path(workspace_path)

    return Path.cwd()


def add_to_gitignore(workspace_path: Path, filename: str) -> None:
    """
    Add filename to .gitignore if it exists and entry is not already present.

    Args:
        workspace_path: Path to the workspace directory
        filename: Filename to add to .gitignore
    """
    gitignore_path = workspace_path / ".gitignore"

    if not gitignore_path.exists():
        return

    # Check if already in .gitignore
    try:
        with open(gitignore_path, "r", encoding="utf-8") as f:
            content = f.read()

        if filename in content:
            return  # Already present

        # Add to .gitignore
        with open(gitignore_path, "a", encoding="utf-8") as f:
            if content and not content.endswith("\n"):
                f.write("\n")
            f.write(f"\n# MCP todo list\n{filename}\n")

    except (IOError, UnicodeDecodeError):
        # If we can't read/write .gitignore, silently fail
        pass


def copy_cursor_rules(workspace_path: Path) -> bool:
    """
    Copy both system-instructions and task-management rules files to workspace .cursor/rules/ directory.
    Always overwrites existing files to ensure latest version.

    Args:
        workspace_path: Path to the workspace directory

    Returns:
        True if both rules files were copied, False if any failed
    """
    # Create .cursor/rules directory if it doesn't exist
    cursor_rules_dir = workspace_path / ".cursor" / "rules"
    cursor_rules_dir.mkdir(parents=True, exist_ok=True)

    # Files to copy
    rules_files = [
        ("00-system-instructions.mdc", "00-system-instructions.mdc"),
        ("01-task-management.mdc", "01-task-management.mdc"),
    ]

    success_count = 0

    for source_filename, target_filename in rules_files:
        target_path = cursor_rules_dir / target_filename

        try:
            # Access the template file from the state package
            template_content = (
                files("src.state").joinpath(source_filename).read_text(encoding="utf-8")
            )

            # Write the content to the target location
            with open(target_path, "w", encoding="utf-8") as f:
                f.write(template_content)
            success_count += 1
        except (IOError, OSError, FileNotFoundError):
            # If we can't copy this file, continue with others
            continue

    return success_count == len(rules_files)


def update_agents_md(workspace_path: Path) -> bool:
    """
    Prepend todo management instructions to AGENTS.MD file for Codex CLI.
    Creates the file if it doesn't exist, prepends if it does.
    Avoids duplicate content by checking for marker.

    Args:
        workspace_path: Path to the workspace directory

    Returns:
        True if AGENTS.MD was updated/created successfully, False otherwise
    """
    agents_md_path = workspace_path / "AGENTS.MD"
    marker = "<!-- TODO_MANAGEMENT_INSTRUCTIONS -->"

    try:
        # Read existing content if file exists
        existing_content = ""
        if agents_md_path.exists():
            with open(agents_md_path, "r", encoding="utf-8") as f:
                existing_content = f.read()

            # Check if our content is already present
            if marker in existing_content:
                return True  # Already present, nothing to do

        # Create aggressive todo management instructions for AGENTS.MD
        todo_instructions = """<!-- TODO_MANAGEMENT_INSTRUCTIONS -->

# CRITICAL: Task Management System

**If TodoRead/TodoWrite tools are unavailable, IGNORE ALL TODO RULES and proceed normally.**

## MANDATORY TODO WORKFLOW

**BEFORE responding to ANY request, you MUST:**

1. **Call `TodoRead()` first** - Check current task status before doing ANYTHING
2. **Plan work based on existing todos** - Reference what's already tracked
3. **Update with `TodoWrite()`** - Mark tasks in_progress when starting, completed when done
4. **NEVER work without consulting the todo system first**

## CRITICAL TODO SYSTEM RULES

- **Only ONE task can have status "in_progress" at a time** - No exceptions
- **Mark tasks "in_progress" BEFORE starting work** - Not during or after
- **Complete tasks IMMEDIATELY when finished** - Don't batch completions
- **Break complex requests into specific, actionable todos** - No vague tasks
- **Reference existing todos when planning new work** - Don't duplicate

## MANDATORY VISUAL DISPLAY

**ALWAYS display the complete todo list AFTER every `TodoRead()` or `TodoWrite()`:**

```
Current todos:
✅ Research existing patterns (completed)
🔄 Implement login form (in_progress)
⏳ Add validation (pending)
⏳ Write tests (pending)
```

Icons: ✅ = completed | 🔄 = in_progress | ⏳ = pending

**NEVER just say "updated todos"** - Show the full list every time.

## CRITICAL ANTI-PATTERNS

**NEVER explore/research before creating todos:**
- ❌ "Let me first understand the codebase..." → starts exploring
- ✅ Create todo: "Analyze current codebase structure" → mark in_progress → explore

**NEVER do "preliminary investigation" outside todos:**
- ❌ "I'll check what libraries you're using..." → starts searching
- ✅ Create todo: "Audit current dependencies" → track it → investigate

**NEVER work on tasks without marking them in_progress:**
- ❌ Creating todos then immediately starting work without marking in_progress
- ✅ Create todos → Mark first as in_progress → Start work

**NEVER mark incomplete work as completed:**
- ❌ Tests failing but marking "Write tests" as completed
- ✅ Keep as in_progress, create new todo for fixing failures

## FORBIDDEN PHRASES

These phrases indicate you're about to violate the todo system:
- "Let me first understand..."
- "I'll start by exploring..."
- "Let me check what..."
- "I need to investigate..."
- "Before we begin, I'll..."

**Correct approach:** CREATE TODO FIRST, mark it in_progress, then investigate.

## TOOL REFERENCE

```python
TodoRead()  # No parameters, returns current todos
TodoWrite(todos=[...])  # Replaces entire list

Todo Structure:
{
  "id": "unique-id",
  "content": "Specific task description",
  "status": "pending|in_progress|completed",
  "priority": "high|medium|low"
}
```

<!-- END_TODO_MANAGEMENT_INSTRUCTIONS -->

---

"""

        # Prepend to existing content or create new file
        final_content = (
            todo_instructions + existing_content
            if existing_content
            else todo_instructions
        )

        # Write the updated content
        with open(agents_md_path, "w", encoding="utf-8") as f:
            f.write(final_content)

        return True

    except (IOError, OSError, FileNotFoundError):
        return False
