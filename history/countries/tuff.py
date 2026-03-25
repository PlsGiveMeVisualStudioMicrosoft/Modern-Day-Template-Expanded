import os
import re

FOLDER = r"C:\Users\User\Documents\Paradox Interactive\Hearts of Iron IV\mod\Modern Day Template Expanded\history\countries"

def remove_add_ideas_blocks(text):
    """
    Removes all add_ideas = { ... } blocks (multi-line) and
    add_ideas = single_value lines from HOI4 script files.
    """
    result = []
    i = 0
    lines = text.splitlines(keepends=True)

    while i < len(lines):
        line = lines[i]
        stripped = line.strip()

        # Match: add_ideas = { (multi-line block)
        if re.match(r'add_ideas\s*=\s*\{', stripped):
            depth = stripped.count('{') - stripped.count('}')
            if depth <= 0:
                # Opening and closing brace on the same line — skip it
                i += 1
                continue
            # Skip lines until the block closes
            i += 1
            while i < len(lines) and depth > 0:
                depth += lines[i].count('{') - lines[i].count('}')
                i += 1
            continue

        # Match: add_ideas = some_single_value (no braces)
        if re.match(r'add_ideas\s*=\s*\S+', stripped) and '{' not in stripped:
            i += 1
            continue

        result.append(line)
        i += 1

    return ''.join(result)


def process_folder(folder):
    if not os.path.isdir(folder):
        print(f"ERROR: Folder not found: {folder}")
        return

    files = [f for f in os.listdir(folder) if f.endswith('.txt')]
    if not files:
        print("No .txt files found in the folder.")
        return

    for filename in files:
        filepath = os.path.join(folder, filename)
        with open(filepath, 'r', encoding='utf-8-sig') as f:
            original = f.read()

        modified = remove_add_ideas_blocks(original)

        if modified != original:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(modified)
            print(f"  Modified: {filename}")
        else:
            print(f"  No changes: {filename}")

    print("\nDone.")


if __name__ == "__main__":
    process_folder(FOLDER)