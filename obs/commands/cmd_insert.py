# obs/commands/insert_cmd.py
import sys
from pathlib import Path

from openai import OpenAI


def insert_file(
    vault_path: Path, filename: str, user_instruction: str, openai_api_key: str
):
    """
    Load the file, let GPT-4o decide where to insert new content, and save the file.
    """
    file_path = vault_path / f"{filename}.md"
    if not file_path.exists():
        print(f"Error: File '{file_path}' does not exist.")
        sys.exit(1)

    original_content = file_path.read_text(encoding="utf-8")

    system_message = (
        "You are a helpful assistant specialized in editing Markdown documents. "
        "You will be given the content of an existing markdown document, along with instructions on adding or modifying content. "
        "You must read the first message from the user, containing the current document content, "
        "then follow the user's instructions to update it in their second message.\n\n"
        "You must follow the below guidelines:\n"
        "1. Output ONLY markdown content, with no additional commentary, discussion, or follow-up.\n"
        "2. Maintain correct and valid Markdown structure.\n"
        "    - You may use features from Obsidian's markdown syntax such as [[wikilinks]] and admonitions.\n"
        "3. Do NOT escape the Markdown content in your response with any delimiters such as ```markdown or ---.\n"
        "4. Avoid modifying any existing content that the user has not explicitly asked you to change.\n"
        "5. Maintain formatting that is consistent with the existing content (e.g. indentation, heading structure, use of lists).\n\n"
        "The user will now send one message with the current document content, "
        "followed by another message with instructions on how to update it. Follow their instructions closely"
    )

    user_instruction = (
        "Instructions to update above document content:\n\n" + user_instruction
    )

    # Create a new OpenAI client instance
    client = OpenAI(api_key=openai_api_key)

    try:
        completion = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "developer", "content": system_message},
                {"role": "user", "content": original_content},
                {"role": "user", "content": user_instruction},
            ],
            temperature=0.5,
        )
        new_content = completion.choices[0].message.content
    except Exception as e:
        print(f"Error calling OpenAI API: {e}")
        sys.exit(1)

    try:
        file_path.write_text(new_content, encoding="utf-8")
        print(f"Inserted content and updated file at: {file_path}")
    except Exception as e:
        print(f"Error writing file '{file_path}': {e}")
        sys.exit(1)
