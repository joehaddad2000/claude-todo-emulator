<general_rules>
- **Tool Development**: When creating new MCP tools, always first check the `/src/tools/` directory to see if a similar tool exists. If creating a new tool, place it in `/src/tools/` and follow the existing pattern of thin wrappers around state management functions.
- **State Management**: When adding state management functions, use the `/src/state/` directory. Follow the singleton pattern established by the `store` instance in `/src/state/store.py`. All state operations should go through the centralized store.
- **Type Annotations**: Use Python 3.11+ modern type hints consistently:
  - `list[T]` instead of `List[T]`
  - `dict[K, V]` instead of `Dict[K, V]`
  - `str | None` instead of `Optional[str]`
  - Full type annotations required for all functions and class attributes
- **Business Rules Enforcement**: Always enforce these critical business rules in validation:
  - Only one todo can have status "in_progress" at a time
  - All todo IDs must be unique within the list
  - Required fields: id, content, status, priority
- **Code Quality**: Always run `make lint` and `make format` before committing changes. The project uses ruff for both linting and formatting.
- **Development Commands**: Use `make setup` or `uv sync` to install dependencies, `make clean` to remove cache files, and `uv run python -m src.server` to run the MCP server directly.
</general_rules>

<repository_structure>
This is a FastMCP-based Model Context Protocol server with a layered architecture:

**MCP Server Layer** (`/src/server.py`):
- FastMCP entry point with two main tools: `TodoRead()` and `TodoWrite(params)`
- Handles error responses and acts as the public API
- Manages server lifecycle and initialization

**Tool Layer** (`/src/tools/`):
- `todo_read.py` - Returns current todos (no parameters required)
- `todo_write.py` - Replaces entire todo list with validation
- Thin wrappers that delegate to the state management layer

**State Management Layer** (`/src/state/`):
- `store.py` - Singleton store pattern with auto-initialization
- `validators.py` - Enforces business rules and type validation
- `persistence.py` - File-based storage with atomic writes
- `utils.py` - Workspace detection and Cursor rules integration

**Type Definitions** (`/src/types.py`):
- TypedDict definitions for Todo, TaskStore, and API responses
- Enums for TodoStatus and TodoPriority

**Data Flow**: MCP Client → Server Tools → State Store → Validation → Persistence Layer

**Key Features**:
- Project-scoped todos (each workspace gets its own `.mcp-todos.json`)
- Automatic workspace detection via environment variables
- Atomic file writes for data integrity
- Auto-copying of Cursor rules to `.cursor/rules/` directory
</repository_structure>

<dependencies_and_installation>
- **Package Manager**: This project uses `uv` as the modern Python package manager
- **Python Version**: Requires Python 3.11 or higher
- **Installation**: Run `uv sync` or `make setup` to install all dependencies
- **Main Dependency**: FastMCP framework (`fastmcp>=2.8.1`) for MCP server functionality
- **Lock File**: Dependencies are locked in `uv.lock` for reproducible builds
- **Virtual Environment**: `uv` automatically manages the virtual environment
</dependencies_and_installation>

<testing_instructions>
**Current State**: Testing framework is not yet implemented in this repository.

**Planned Testing Setup**:
- **Framework**: pytest will be used when testing is implemented
- **Test Execution**: Run tests via `uv run python -m pytest`
- **Test Coverage Areas** (when implemented):
  - Validation logic in `/src/state/validators.py`
  - State management operations in `/src/state/store.py`
  - Persistence mechanisms and atomic writes
  - Tool functionality and error handling
  - Business rule enforcement (single in-progress task, unique IDs)

**Testing Guidelines** (for future implementation):
- Test files should mirror the source structure
- Focus on testing business logic and validation rules
- Mock file system operations for persistence tests
- Ensure error handling paths are covered
</testing_instructions>

<pull_request_formatting>
</pull_request_formatting>
