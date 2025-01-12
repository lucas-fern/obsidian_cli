# obs/backup.py
import sys
from datetime import datetime
from pathlib import Path


def backup_note(
    vault_code: str, vault_path: Path, filename: str, backup_dir: Path
) -> None:
    """
    Creates a timestamped backup of the note before editing.

    Example of final backup path:
        backup_dir / P / 2025-01-22-T15-22-MyNote.md

    If the original file doesn't exist, we won't create a backup.
    """
    file_path = vault_path / f"{filename}.md"
    if not file_path.exists():
        print(f"Warning: Cannot back up non-existing file '{file_path}'.")
        return

    # Read existing file content
    try:
        content = file_path.read_text(encoding="utf-8")
    except Exception as e:
        print(f"Error reading file for backup: {e}")
        return

    # Ensure subdirectory for vault code exists
    vault_backup_dir = backup_dir / vault_code
    vault_backup_dir.mkdir(parents=True, exist_ok=True)

    # Create a timestamped backup filename
    timestamp = datetime.now().strftime("%Y-%m-%d-T%H-%M")
    backup_filename = f"{timestamp}-{filename}.md"
    backup_path = vault_backup_dir / backup_filename

    # Write content to the backup file
    try:
        backup_path.write_text(content, encoding="utf-8")
        print(f"Backed up '{filename}.md' to '{backup_path}'")
    except Exception as e:
        print(f"Error writing backup file '{backup_path}': {e}")
