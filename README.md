[![MseeP.ai Security Assessment Badge](https://mseep.net/pr/joehaddad2000-claude-todo-emulator-badge.png)](https://mseep.ai/app/joehaddad2000-claude-todo-emulator)

# Claude Todo MCP Server

[![PyPI Version](https://img.shields.io/pypi/v/claude-todo-emulator.svg)](https://pypi.org/project/claude-todo-emulator/)
[![PyPI Downloads](https://static.pepy.tech/badge/claude-todo-emulator)](https://pepy.tech/projects/claude-todo-emulator)

**Add persistent task management to any AI coding assistant in Cursor, Windsurf, and other IDEs.**

This MCP server replicates Claude Code's todo system, giving your AI assistant the ability to:

- Track complex multi-step tasks across sessions
- Break down large features into manageable pieces
- Remember progress when you switch between projects
- Enforce single in-progress task focus

## Quick Start

**No installation required!** Just add this to your MCP configuration:

### Cursor IDE

Create `.cursor/mcp.json` in your project root:

```json
{
  "mcpServers": {
    "task-manager": {
      "command": "uvx",
      "args": ["claude-todo-emulator"]
    }
  }
}
```

### Codex CLI

Create `config.toml` at your project root:

```toml
[mcp_servers.task-manager]
command = "uvx"
args = ["claude-todo-emulator"]
```

### Other IDEs

Add the JSON configuration above to your MCP settings file.

**Restart your IDE** and try: _"Create a todo list for adding user authentication"_

The system automatically downloads the package and sets up everything on first use!

## What You Get

Once configured, your AI assistant will automatically:

**Create todos for complex tasks:**

```
You: "Add dark mode support with user preferences"
AI: "I'll create a todo list for this multi-step feature:
- ✅ Add theme context and state management
- 🔄 Create dark mode CSS variables and styles
- ⏳ Build settings UI for theme switching
- ⏳ Add persistence to localStorage
- ⏳ Update existing components for theme support"
```

**Track progress visually:**

```
You: "What's the status on the authentication system?"
AI: "Current authentication tasks:
- ✅ Set up JWT middleware
- ✅ Create login/signup endpoints
- 🔄 Building user profile management (in progress)
- ⏳ Add password reset flow
- ⏳ Implement role-based permissions"
```

**Maintain focus:**

```
You: "Let's also add email notifications"
AI: "I'll add that to the todo list, but let me finish the current user profile task first to maintain focus."
```

### API Reference

**TodoRead**

- Parameters: None
- Returns: `{todos: Todo[]}`

**TodoWrite**

- Parameters: `{todos: Todo[]}`
- Returns: `{success: boolean, count: number}`

**Todo Schema**

```typescript
{
  id: string;
  content: string;
  status: "pending" | "in_progress" | "completed";
  priority: "high" | "medium" | "low";
  created_at: string;
  updated_at: string;
  metadata?: object;
}
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Add tests for new functionality
4. Submit a pull request

## License

MIT License - see LICENSE file for details.

## Related Projects

- [Model Context Protocol](https://modelcontextprotocol.io/)
- [FastMCP](https://gofastmcp.com/)
- [Claude Code](https://www.anthropic.com/claude-code)
