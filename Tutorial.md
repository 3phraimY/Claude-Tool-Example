# Connecting MCP to Claude Desktop Tutorial

## 1. Creating Local MCP Server

server.py:

```
# must run pip install fastmcp

from fastmcp import FastMCP
from pathlib import Path
import os

mcp = FastMCP("FileWriter")

@mcp.tool()
def write_text_file(filename: str, content: str):
    """Creates a text file in the user's Downloads folder and writes a message inside it."""

    # Write to downloads folder
    downloads_path = Path.home() / "Downloads"

    safe_filename = os.path.basename(filename)
    full_path = downloads_path / safe_filename

    try:
        with open(full_path, "w", encoding="utf-8") as f:
            f.write(content)
        return f"Successfully wrote message to {full_path}"
    except Exception as e:
        return f"Error writing file: {str(e)}"

if __name__ == "__main__":
    #print(write_text_file("test.txt", "Hello direct test!3"))
    mcp.run()
```

the function `write_text_file` accepts a `filename` and `content` parameters and creates the text file in the Downloads folder.
<br>
<br>
MCP - Model Context Protocol <br>
MCP provides access to this function to Claude. Note that there is a comment within the `"""..."""` this comment is NOT for the benefit of the developer, but for the LLM which has access to this function. MCP allows this function to become a `tool` which Claude can access and use. To the LLM this tool appears stripped of its logic essentially like this:

```
def write_text_file(filename: str, content: str):
    """Creates a text file in the user's Downloads folder and writes a message inside it."""
```

Claude can choose when it seems necessary to use this tool based on the name and description provide. We will also further define its use in the skill section.

## 2. Add Local MCP Server to Claude

Navigate to `File>Settings>Developer` select `Edit Config` and open the `claude_desktop_config.json` file in a text editor. We will add an `mcpServers` section to this config file:

```
{
  "preferences": {
    "coworkScheduledTasksEnabled": false,
    "ccdScheduledTasksEnabled": false,
    "coworkWebSearchEnabled": true,
    "sidebarMode": "chat"
  },
  "mcpServers": {
    "file-writer": {
      "command": "python",
      "args": ["##replace with absolute path to server.py file containing tool##"]
    }
  }
}
```

Now restart Claude to apply the latest config (may have to kill via task manager). Returning back to `File>Settings>Developer` area, there should be a tool named `file-writer` displayed. It is correctly working if the tool is in the `running` state. Claude will automatically startup and close down the MCP server so there is no need to have a terminal running the server.py file. Check logs for any potential issues. (Only problem I had was not having fastMCP installed to the python installation Claude was using).
<br><br>
You have successfully added a `tool` to Claude. It can now use this tool at its discretion.

## 3. Add Skill to Claude

Rather than relying solely on Claude figuring out when to use this skill, we can more explicitly define its use of a tool.
<br><br>
SKILL.md:

```
---
name: text-file-creator
description: Expert skill for generating and saving text files to the local system.
allowed-tools: [write_text_file]
---

# Text File Creator Skill

Use this skill when a user wants to "save," "export," or "write" a message to a physical file.

## Execution Steps:

1. Ask the user for a filename if they haven't provided one (default to `note.txt`).
2. Draft the message clearly.
3. Call the `write_text_file` tool to save the content.
4. Confirm to the user exactly where the file was saved.

```

Upload this skill by navigating to `Customize>Skills>+>Create skill>Upload a skill` and dragging the SKILL.md file above into the dropbox. Now a new skill should appear in the dropdown `text-file-creator`.
<br><br>
This skill can now be called explicitly using the`/text-file-creator`command. However, ideally, we have adequately described when to use the `file-writer` tool by providing some scenarios of when to use this tool. Additionally, this skill provides step-by-step instructions on how to make use of this tool.
