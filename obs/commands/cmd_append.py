# obs/commands/append_cmd.py
import sys
from pathlib import Path

from openai import OpenAI


def append_file(
    vault_path: Path, filename: str, user_instruction: str, openai_api_key: str
):
    """
    Load the file from vault_path/filename.md, then request GPT-4o to append content to the end.
    """
    file_path = vault_path / f"{filename}.md"
    if not file_path.exists():
        print(f"Error: File '{file_path}' does not exist.")
        sys.exit(1)

    original_content = file_path.read_text(encoding="utf-8")

    system_message = (
        "You are a helpful assistant specialized in editing Markdown documents. "
        "You will be given the content of an existing markdown document, along with instructions on appending content. "
        "You must read the first message from the user, containing the current document content, "
        "then follow the user's instructions to write new content to append to the end of the note.\n\n"
        "You must follow the below guidelines:\n"
        "1. Your response must be a continuation of the existing file, such that concatenating the original content with your response results in a valid Markdown document.\n"
        "2. Output ONLY markdown content, with no additional commentary, discussion, or follow-up.\n"
        "3. Maintain correct and valid Markdown structure.\n"
        "    - You may use features from Obsidian's markdown syntax such as [[wikilinks]] and admonitions.\n"
        "    - Your response will be concatenated on a NEW LINE at the end of the existing content, account for this in your response.\n"
        "4. Do NOT escape the Markdown content in your response with any delimiters such as ```markdown or ---.\n"
        "5. Do not try to modify or restate existing content. Your response with be joined onto the end to produce the final document.\n"
        "6. Maintain formatting that is consistent with the existing content (e.g. indentation, heading structure, use of lists).\n\n"
        "The user will now send one message with the current document content, "
        "followed by another message with instructions on what to append. Follow their instructions closely."
    )

    user_instruction = (
        "Instructions on what to append to the above document:\n\n" + user_instruction
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

    # Save the new content to the file
    new_content = original_content + "\n" + new_content
    try:
        file_path.write_text(new_content, encoding="utf-8")
        print(f"Appended content and updated file at: {file_path}")
    except Exception as e:
        print(f"Error writing file '{file_path}': {e}")
        sys.exit(1)
