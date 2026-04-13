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
