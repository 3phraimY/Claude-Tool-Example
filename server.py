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
    #print(write_text_file("test.txt", "Hello direct test!"))
    mcp.run()    