# obs/cli.py
import sys
from pathlib import Path

from obs.commands.cmd_append import append_file
from obs.commands.cmd_create import create_file
from obs.commands.cmd_insert import insert_file
from obs.config import load_config


def main():
    """
    Entry point: usage:
        obs [vault_code] create [filename] [content]
        obs [vault_code] append [filename] [instruction]
        obs [vault_code] insert [filename] [instruction]
    """
    if len(sys.argv) < 5:
        print("Usage: obs [vault] [create|append|insert] [filename] [command]")
        sys.exit(1)

    vault_code = sys.argv[1]
    action = sys.argv[2].lower()
    filename = sys.argv[3]
    command_text = " ".join(sys.argv[4:])  # combine everything after the filename

    config = load_config()
    vaults = config.get("vaults", {})
    openai_api_key = config.get("openai_api_key", None)

    # Validate vault
    if vault_code not in vaults:
        print(f"Error: Vault code '{vault_code}' not found in config.")
        sys.exit(1)
    vault_path = Path(vaults[vault_code]).expanduser()
    if not vault_path.exists():
        print(f"Error: Vault path '{vault_path}' does not exist on disk.")
        sys.exit(1)

    # Dispatch
    if action == "create":
        create_file(vault_path, filename, command_text)
    elif action == "append":
        if not openai_api_key:
            print("Error: No OpenAI API key found in config.")
            sys.exit(1)
        append_file(vault_path, filename, command_text, openai_api_key)
    elif action == "insert":
        if not openai_api_key:
            print("Error: No OpenAI API key found in config.")
            sys.exit(1)
        insert_file(vault_path, filename, command_text, openai_api_key)
    else:
        print(f"Error: Unrecognized action '{action}'. Use create, append, or insert.")
        sys.exit(1)


if __name__ == "__main__":
    main()
