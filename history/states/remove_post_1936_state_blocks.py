import os
import re

FOLDER = r"C:\Users\User\Documents\Paradox Interactive\Hearts of Iron IV\mod\Modern Day Template Expanded\history\states"

DATE_PATTERN = re.compile(r"(\d{4})\.(\d{1,2})\.(\d{1,2})")

CUTOFF = (1936, 1, 1)

def is_after_cutoff(year, month, day):
    return (year, month, day) > CUTOFF

def remove_future_blocks(text):
    i = 0
    length = len(text)
    result = []

    while i < length:
        match = DATE_PATTERN.match(text, i)
        if not match:
            result.append(text[i])
            i += 1
            continue

        year, month, day = map(int, match.groups())
        j = match.end()

        # Skip whitespace
        while j < length and text[j].isspace():
            j += 1

        # Must be followed by '='
        if j >= length or text[j] != "=":
            result.append(text[i])
            i += 1
            continue

        j += 1
        while j < length and text[j].isspace():
            j += 1

        # Must be followed by '{'
        if j >= length or text[j] != "{":
            result.append(text[i])
            i += 1
            continue

        # Decide whether to delete
        delete_block = is_after_cutoff(year, month, day)

        brace_count = 1
        j += 1

        while j < length and brace_count > 0:
            if text[j] == "{":
                brace_count += 1
            elif text[j] == "}":
                brace_count -= 1
            j += 1

        if not delete_block:
            result.append(text[i:j])

        i = j

    return "".join(result)

for filename in os.listdir(FOLDER):
    if not filename.lower().endswith(".txt"):
        continue

    path = os.path.join(FOLDER, filename)

    with open(path, "r", encoding="utf-8") as f:
        original = f.read()

    modified = remove_future_blocks(original)

    if original != modified:
        with open(path, "w", encoding="utf-8") as f:
            f.write(modified)
        print(f"Edited: {filename}")
    else:
        print(f"No post-1936 blocks: {filename}")