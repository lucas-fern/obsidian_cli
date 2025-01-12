# obs/commands/create_cmd.py
import sys
from pathlib import Path

PERSON_TEMPLATE = """# {name}

## Details

### Personal

- **Email:** 
- **Phone Number:**
- **Address:**
- **Birthday:**

### Professional 

- **Education:**
- **Company/organisation:**
- **Role:**

## Relationships

- **Partner:**

### Family

- **Parents:**
- **Children:**

#### Pets
 

### Network


## Conversations and Events


## Notes


## Gifts

**Gift ideas:**

**Gifts given:**


## Tasks

"""


def create_person(vault_path: Path, filename: str, content: str):
    """
    Create a new CRM person file at the specified location.
    """
    file_path = vault_path / f"{filename}.md"

    if file_path.exists():
        print(f"Error: File '{file_path}' already exists.")
        sys.exit(1)

    try:
        file_path.write_text(PERSON_TEMPLATE.format(name=filename), encoding="utf-8")
        print(f"Created file at: {file_path}")

    except Exception as e:
        print(f"Error creating file '{file_path}': {e}")
        sys.exit(1)
