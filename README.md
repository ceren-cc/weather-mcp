# 🌤️ Weather MCP Tool

This is an MCP (Model Context Protocol) server that provides weather alerts and forecasts using the U.S. National Weather Service API.

It supports two tools:
- `get_alerts`: Returns active weather alerts for a given U.S. state.
- `get_forecast`: Returns a 5-period weather forecast for a given location (latitude & longitude).

> Built with FastMCP and httpx  
> Designed to be used with Claude or any other MCP-compatible client.

---

## Clone the repository:
   ```bash
   git clone https://github.com/<your-username>/weather-mcp.git
   cd weather-mcp
   ```

---

## Set up the environment

To get started, make sure you have uv installed and that your Python version is 3.11.

And you also need FastMCP and httpx are available.

Then run the following steps:
- mkdir <folder_name>
- cd <folder_name>
- uv venv --python=3.11
- source .venv/bin/activate
- uv init --no-workspace
- uv add "mcp[cli]" httpx

⚠️ Note: These steps require Python version 3.11 to work properly. You may need to install it manually if your system uses a different version.

---

## How to add your MCP Tool to Claude
1. Open Claude, go to Settings → Developer.
2. Click on Edit Config.
3. From the list of files, open claude_desktop_config.json.
4. Add the following JSON structure to configure the MCP server:
```JSON
{
  "mcpServers": {
    "Weather": {
      "command": "<path-to-uv>",
      "args": [
        "run",
        "--with",
        "mcp[cli]",
        "mcp",
        "run",
        "<path-to-your-main.py>"
      ]
    }
  }
}
```

- Replace <path-to-uv> with the full path to your uv binary.

Example (on macOS):

"/Users/yourname/.local/bin/uv"

- Replace <path-to-your-main.py> with the full path to your main.py file.

Example:

"/Users/yourname/Projects/weather-mcp/main.py"

5. Save the config file. Claude will now recognize and run your local MCP.

---

## Adding multiple MCP Tools
If you want to run more than one MCP at the same time, structure your config like this:

```JSON
{
  "mcpServers": {
    "Weather": {
      "command": "<path-to-uv>",
      "args": [
        "run",
        "--with",
        "mcp[cli]",
        "mcp",
        "run",
        "<path-to-weather-main.py>"
      ]
    },
    "Sticky Notes": {
      "command": "<path-to-uv>",
      "args": [
        "run",
        "--with",
        "mcp[cli]",
        "mcp",
        "run",
        "<path-to-notes-main.py>"
      ]
    }
  }
}
```

📌 Tip: If you're unsure about the exact path, use the which uv or realpath main.py command in your terminal.