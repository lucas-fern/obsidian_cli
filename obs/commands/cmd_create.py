# obs/commands/create_cmd.py
import sys
from pathlib import Path


def create_file(vault_path: Path, filename: str, content: str):
    """
    Create a new markdown file in the specified vault with the given content.
    """
    file_path = vault_path / f"{filename}.md"

    if file_path.exists():
        print(f"Error: File '{file_path}' already exists.")
        sys.exit(1)

    try:
        file_path.write_text(content, encoding="utf-8")
        print(f"Created file at: {file_path}")
    except Exception as e:
        print(f"Error creating file '{file_path}': {e}")
        sys.exit(1)
