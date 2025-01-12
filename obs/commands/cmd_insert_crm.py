# obs/commands/insert_cmd.py
import sys
from pathlib import Path

from openai import OpenAI


def insert_file_crm(
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
        "You maintain a Customer Relationship Management (CRM) system for the user. "
        "You will be given the content of an existing document in the CRM, along with information to insert into it. "
        "You must read the first message from the user, containing the current document, "
        "then insert the information from the user's second message by deciding where it should be placed "
        "and how it should be formatted into the existing document.\n\n"
        "You are provided a sample document in the following developer message, and must adhere to this structure. "
        "You must follow the below guidelines:\n"
        "1. Output ONLY markdown content, with no additional commentary, discussion, or follow-up.\n"
        "2. Maintain correct and valid Markdown structure.\n"
        "    - You must use features from Obsidian's markdown syntax such as [[wikilinks]] as they appear in the sample document.\n"
        "        - Specifically, [[wikilinks]] are used to link together companies, organisations, people (using [[Fistname Lastname]]), and cities (e.g. [[Melbourne]]).\n"
        "        - However, you should only link names of people when the full first and last name is known.\n"
        "3. Do NOT escape the Markdown content in your response with any delimiters such as ```markdown or ---.\n"
        "4. Avoid modifying any existing content that the user has not explicitly asked you to change.\n"
        "5. Maintain formatting that is consistent with the existing content (e.g. indentation, heading structure, use of lists).\n"
        "6. You may reword the content provided by the user to fit the structure, content, and format of the document.\n"
        "7. You must return the entire document with the new content inserted, your response will overwrite the existing file.\n\n"
        "The following message contains a sample CRM contact for John Doe. The user will then send a real CRM contact, "
        "and finally a piece of information for you to insert into the document at the appropriate location. "
        "Follow their instructions closely."
    )

    sample_crm_contact = (
        "# John Doe\n"
        "\n"
        "## Details\n"
        "\n"
        "### Personal\n"
        "\n"
        "- **Email:** jdoe@gmail.com\n"
        "- **Phone Number:** (+61) 456 789 123\n"
        "- **Address:** 42 Main Street, Carlton, [[Melbourne]], VIC, 3053, Australia\n"
        "- **Birthday:** March 1st, 2000\n"
        "\n"
        "### Professional \n"
        "\n"
        "- **Education:**\n"
        "	- Bachelor of Science - Data Science\n"
        "	- Master of Science - Computer Science (AI)\n"
        "- **Company/organisation:**\n"
        "	- [[Coca Cola]]\n"
        "- **Role:**\n"
        "	- Lead Data Scientist\n"
        "\n"
        "## Relationships\n"
        "\n"
        "- **Partner:** [[Jane Doe]]\n"
        "\n"
        "### Family\n"
        "\n"
        "- **Parents:** \n"
        "	- [[Bob Doe]] (father)\n"
        "	- [[Jill Doe]] (mother)\n"
        "- **Children:**\n"
        "	- [[Jimmy Doe]] (son)\n"
        "- **Siblings:**\n"
        "	- [[Jack Doe]] (brother)\n"
        "\n"
        "#### Pets\n"
        "\n"
        "- Jimbob (goldfish)\n"
        "- Penjamin (golden retriever)\n"
        "\n"
        "### Network\n"
        "\n"
        "- [[Kevin Rudd]] (manager)\n"
        "- [[Julia Gillard]] (ex-lover)\n"
        "\n"
        "## Conversations and Events\n"
        "\n"
        "### [[2024-12-10]]\n"
        "\n"
        "- Went for a river cruise with John and [[Jane Doe]]\n"
        "- Discussed their new dog Penjamin, which they picked up on [[2024-12-05]]\n"
        "- Crashed boat\n"
        "\n"
        "### [[2024-08-28]]\n"
        "\n"
        "- Went for dinner with John at Burger King\n"
        "- Discussed his recent breakup with [[Julia Gillard]]\n"
        "\n"
        "## Notes\n"
        "\n"
        "- Kevin barracks for the Geelong football club\n"
        "- Kevin's favourite ice-cream flavour is mint choc-chip\n"
        "\n"
        "## Gifts\n"
        "\n"
        "**Gift ideas:**\n"
        "- Voucher for trapeze class\n"
        "- How to Make Friends and Influence People (book)\n"
        "\n"
        "**Gifts given:**\n"
        "- Jimbob (goldfish)\n"
        "- Lego set of the Eiffel tower\n"
        "\n"
        "## Tasks\n"
        "\n"
        "- [x] Buy Eiffel tower lego set for John\n"
        "- [x] Book river cruise\n"
        "- [ ] Pay insurance claim for crashed river cruise\n"
    )

    user_instruction = (
        f"Content to insert into {filename}'s CRM contact:\n\n" + user_instruction
    )

    # Create a new OpenAI client instance
    client = OpenAI(api_key=openai_api_key)

    try:
        completion = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "developer", "content": system_message},
                {"role": "developer", "content": sample_crm_contact},
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
