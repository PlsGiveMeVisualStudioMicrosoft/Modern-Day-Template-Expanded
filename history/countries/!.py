import os
import re

FOLDER = r"C:\Users\User\Documents\Paradox Interactive\Hearts of Iron IV\mod\Modern Day Template Expanded\history\countries"

def remove_create_country_leader_blocks(text):
    """
    Removes all create_country_leader = { ... } blocks,
    handling nested braces correctly.
    """
    result = []
    i = 0
    removed = 0

    while i < len(text):
        # Look for the keyword
        match = re.search(r'create_country_leader\s*=\s*\{', text[i:])
        if not match:
            result.append(text[i:])
            break

        # Append everything before this block
        result.append(text[i : i + match.start()])

        # Walk forward counting braces to find the end of the block
        block_start = i + match.start()
        brace_pos = i + match.end() - 1  # position of the opening '{'
        depth = 1
        j = brace_pos + 1

        while j < len(text) and depth > 0:
            if text[j] == '{':
                depth += 1
            elif text[j] == '}':
                depth -= 1
            j += 1

        # j now points just past the closing '}'
        # Also consume a trailing newline if present
        if j < len(text) and text[j] == '\n':
            j += 1

        removed += 1
        i = j  # skip past the block

    return ''.join(result), removed


def process_folder(folder):
    txt_files = [f for f in os.listdir(folder) if f.endswith('.txt')]
    if not txt_files:
        print("No .txt files found in the folder.")
        return

    total_removed = 0
    files_changed = 0

    for filename in sorted(txt_files):
        filepath = os.path.join(folder, filename)
        with open(filepath, 'r', encoding='utf-8-sig') as f:
            original = f.read()

        cleaned, count = remove_create_country_leader_blocks(original)

        if count > 0:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(cleaned)
            print(f"  [{filename}]  removed {count} block(s)")
            total_removed += count
            files_changed += 1
        else:
            print(f"  [{filename}]  nothing to remove")

    print(f"\nDone. {total_removed} block(s) removed across {files_changed} file(s).")


if __name__ == "__main__":
    if not os.path.isdir(FOLDER):
        print(f"ERROR: Folder not found:\n  {FOLDER}")
        print("Edit the FOLDER variable at the top of this script.")
    else:
        print(f"Scanning: {FOLDER}\n")
        process_folder(FOLDER)
    input("\nPress Enter to exit...")