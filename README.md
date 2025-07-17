# 🌤️ Weather MCP Tool

This is an MCP (Model Context Protocol) server that provides weather alerts and forecasts using the U.S. National Weather Service API.

It supports two tools:
- `get_alerts`: Returns active weather alerts for a given U.S. state.
- `get_forecast`: Returns a 5-period weather forecast for a given location (latitude & longitude).

> Built with FastMCP and httpx  
> Designed to be used with Claude or any other MCP-compatible client.

---

## How to Run

1. Clone the repository:
   ```bash
   git clone https://github.com/<your-username>/weather-mcp.git
   cd weather-mcp

To get started, you need to install uv on your computer and make sure FastMCP and httpx are available.

Then, follow these steps to create your project folder and set up the environment:

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
