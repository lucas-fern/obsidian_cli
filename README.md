# Obsidian CLI

A command-line tool to manage Obsidian vault notes using GPT-4 for automated text insertion.  
Features:

- **Create** a new note  
- **Append** new content to the end of an existing note via GPT-4  
- **Insert** content anywhere in an existing note, letting GPT-4 decide the best location

## Installation

1. **Clone** this repository or download the code:
   ```bash
   git clone https://github.com/yourusername/obsidian-cli.git
   cd obsidian-cli
   ```

2. **Install** the package (adjust your Python environment as needed):
   ```bash
   pip install .
   ```

3. This exposes a new command called `obs`.

## Configuration

Create a YAML file at `~/.obs_config.yaml` with the following structure:

```yaml
vaults:
  P: /Users/yourusername/Documents/obsidian/personal
  W: /Users/yourusername/Documents/obsidian/work
openai_api_key: "sk-your-openai-key"
```

- **vaults**: A mapping from vault code (e.g., `P`, `W`) to a local folder path.  
- **openai_api_key**: Your secret OpenAI API key (required for `append` and `insert`).

## Usage

```bash
obs [vault] [create|append|insert] [filename] [command]
```

1. **Create**  
   ```bash
   obs P create MyNote "This is the content of my new note"
   ```
   - Creates a new file called `MyNote.md` in the `P` vault directory with the given text.

2. **Append**  
   ```bash
   obs P append MyNote "Add a summary of the above content"
   ```
   - Reads `MyNote.md` from the `P` vault.
   - Sends your instruction to GPT-4 to generate appended content.
   - Saves the updated content back to `MyNote.md`.

3. **Insert**  
   ```bash
   obs P insert MyNote "Include a new heading 'Key Points' with a bullet list"
   ```
   - Reads `MyNote.md` from the `P` vault.
   - Sends your instruction to GPT-4, requesting it to insert content at the best place in the file.
   - Saves the updated file with GPT-4’s modifications.

## Example `.obs_config.yaml`

```yaml
vaults:
  P: /Users/jane_doe/ObsidianVaults/personal
  W: /Users/jane_doe/ObsidianVaults/work
openai_api_key: "sk-123456789abcdef"
```

## Development

- **Run from source** without installing:
  ```bash
  python -m obs.cli P create TestFile "Hello World"
  ```

- **Extend**: Add new commands by creating new files (e.g., `obs/commands/cmd_new.py`) and referencing them in `cli.py`.

## License

[MIT License](LICENSE)