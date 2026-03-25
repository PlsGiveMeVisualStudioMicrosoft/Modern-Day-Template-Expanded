import os

FOLDER = r"C:\Users\User\Documents\Paradox Interactive\Hearts of Iron IV\mod\Modern Day Template Expanded\history\countries"

def remove_1939_block(text):
    target = "1939.1.1"
    i = 0
    length = len(text)
    result = []

    while i < length:
        if text.startswith(target, i):
            j = i + len(target)

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

            # Found the block, now count braces
            brace_count = 1
            j += 1

            while j < length and brace_count > 0:
                if text[j] == "{":
                    brace_count += 1
                elif text[j] == "}":
                    brace_count -= 1
                j += 1

            # Skip the entire block
            i = j
        else:
            result.append(text[i])
            i += 1

    return "".join(result)

for filename in os.listdir(FOLDER):
    if not filename.lower().endswith(".txt"):
        continue

    path = os.path.join(FOLDER, filename)

    with open(path, "r", encoding="utf-8") as f:
        original = f.read()

    modified = remove_1939_block(original)

    if original != modified:
        with open(path, "w", encoding="utf-8") as f:
            f.write(modified)
        print(f"Edited: {filename}")
    else:
        print(f"No 1939 block found: {filename}")