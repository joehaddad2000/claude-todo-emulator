<!-- TODO_MANAGEMENT_INSTRUCTIONS -->

# Task Management

This project uses MCP TodoRead/TodoWrite tools for task tracking.

## Core Rules

**BEFORE responding to any request:**

1. Call `TodoRead()` to check current task status
2. Update progress with `TodoWrite()` when starting/completing tasks

**Status Management:**

- Only ONE task can have status "in_progress" at a time
- Mark tasks "in_progress" BEFORE starting work
- Complete tasks IMMEDIATELY when finished (don't batch)
- Break complex requests into specific, actionable todos

**Visual Display (Required):**
Always show the complete todo list after every TodoRead/TodoWrite:

```
Current todos:
✅ Research patterns (completed)
🔄 Implement feature (in_progress)
⏳ Add tests (pending)
```

Icons: ✅ = completed, 🔄 = in_progress, ⏳ = pending

**Tool Reference:**

```python
TodoRead()  # No parameters, returns current todos
TodoWrite(todos=[...])  # Replaces entire list

Todo Structure:
{
  "id": "unique-id",
  "content": "specific task description",
  "status": "pending|in_progress|completed",
  "priority": "high|medium|low"
}
```

<!-- END_TODO_MANAGEMENT_INSTRUCTIONS -->
