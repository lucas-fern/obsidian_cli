# obs/cli.py
import sys
from pathlib import Path

from obs.backup import backup_note
from obs.commands.cmd_append import append_file
from obs.commands.cmd_create import create_file
from obs.commands.cmd_create_org import create_org
from obs.commands.cmd_create_person import create_person
from obs.commands.cmd_insert import insert_file
from obs.commands.cmd_insert_crm import insert_file_crm
from obs.config import load_config


def main():
    """
    Entry point: usage:
        obs [vault_code] create [filename] [content (optional)]
        obs [vault_code] append [filename] [instruction]
        obs [vault_code] insert [filename] [instruction]
    """
    # Minimal argument check (need at least vault_code and action)
    if len(sys.argv) < 3:
        print("Usage: obs [vault] [create|append|insert] [filename] [command]")
        sys.exit(1)

    vault_code = sys.argv[1]
    action = sys.argv[2].lower()
    # For 'create', filename is mandatory, content is optional
    # For 'append' or 'insert', both filename and command are mandatory
    filename = sys.argv[3] if len(sys.argv) > 3 else ""
    command_text = " ".join(sys.argv[4:]) if len(sys.argv) > 4 else ""

    # Load config and vault data
    config = load_config()
    vaults = config.get("vaults", {})
    openai_api_key = config.get("openai_api_key", None)
    backup_dir_str = config.get("backup_dir", None)

    # Validate vault existence
    if vault_code not in vaults:
        print(f"Error: Vault code '{vault_code}' not found in config.")
        sys.exit(1)
    vault_path = Path(vaults[vault_code]).expanduser()
    if not vault_path.exists():
        print(f"Error: Vault path '{vault_path}' does not exist on disk.")
        sys.exit(1)

    # Require backup_dir
    if not backup_dir_str:
        print("Error: No 'backup_dir' specified in config.")
        sys.exit(1)

    backup_dir = Path(backup_dir_str) if backup_dir_str else None

    # Single check for actions that require the OpenAI API key
    # 'create' does NOT require a key, 'append'/'insert' DO require it
    if not openai_api_key:
        print("Error: No OpenAI API key found in config.")
        sys.exit(1)

    # Dispatch
    match action:
        case "create":
            # For create, require at least filename (command_text is optional)
            if not filename:
                print("Usage: obs [vault] create [filename] (optional content)")
                sys.exit(1)

            # Check if vault code is "C" (custom logic for org vs. person)
            if vault_code.upper() == "C":
                create_person(vault_path, filename, command_text)
            else:
                create_file(vault_path, filename, command_text)

        case "append":
            # For append, filename + command_text are mandatory
            if not filename or not command_text:
                print("Usage: obs [vault] append [filename] [instruction]")
                sys.exit(1)
            backup_note(vault_code, vault_path, filename, backup_dir)
            append_file(vault_path, filename, command_text, openai_api_key)

        case "insert":
            # For insert, filename + command_text are mandatory
            if not filename or not command_text:
                print("Usage: obs [vault] insert [filename] [instruction]")
                sys.exit(1)

            backup_note(vault_code, vault_path, filename, backup_dir)
            if vault_code.upper() == "C":
                insert_file_crm(vault_path, filename, command_text, openai_api_key)
            else:
                insert_file(vault_path, filename, command_text, openai_api_key)

        case _:
            print(
                f"Error: Unrecognized action '{action}'. Use create, append, or insert."
            )
            sys.exit(1)


if __name__ == "__main__":
    main()
