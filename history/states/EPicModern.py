import re
from pathlib import Path

# ===== CONFIG =====

STATES_DIR = Path(
    r"C:\Users\User\Documents\Paradox Interactive\Hearts of Iron IV\mod\Modern Day Template\history\states"
)

# All transfer_state / transfer_state_to effects (ANNEXATIONS EXCLUDED)
STATE_TRANSFERS = {

    # Africa
    #PRC

    #Vietnam and friends
        72: "POL",
        444: "PAK",
        998: "BRM",
        694: "GDL",
        635: "TAH",
        734: "TAH",
        286: "VIN",
        1017: "VIN",
        671: "VIN",
        670: "LAO",
        741: "CAM",

    # Europe (Eastern)


    #Europe (Balkan)


    # Asia


    # Middle East


}

# ===== REGEX =====

STATE_ID_RE = re.compile(r"^(\d{1,4})")
OWNER_RE = re.compile(r"owner\s*=\s*[A-Z]{3}")
CONTROLLER_RE = re.compile(r"controller\s*=\s*[A-Z]{3}")
CORE_RE = re.compile(r"add_core_of\s*=\s*([A-Z]{3})")

# ===== HELPERS =====

def extract_state_id(filename):
    match = STATE_ID_RE.match(filename)
    return int(match.group(1)) if match else None


def rewrite_history(history, new_tag):
    # Replace or insert owner
    if OWNER_RE.search(history):
        history = OWNER_RE.sub(f"owner = {new_tag}", history, count=1)
    else:
        history = history.replace(
            "history = {",
            f"history = {{\n\t\towner = {new_tag}",
            1
        )

    # Replace or insert controller
    if CONTROLLER_RE.search(history):
        history = CONTROLLER_RE.sub(f"controller = {new_tag}", history, count=1)
    else:
        history = history.replace(
            "history = {",
            f"history = {{\n\t\tcontroller = {new_tag}",
            1
        )

    # Remove existing cores (OPTIONAL, uncomment if you want clean borders)
    # history = CORE_RE.sub("", history)

    # Ensure new core exists
    if f"add_core_of = {new_tag}" not in history:
        history = history.replace(
            "history = {",
            f"history = {{\n\t\tadd_core_of = {new_tag}",
            1
        )

    return history


def process_file(path, new_owner):
    text = path.read_text(encoding="utf-8")

    history_start = re.search(r"history\s*=\s*\{", text)
    if not history_start:
        return

    start = history_start.start()
    brace_count = 0

    for i in range(start, len(text)):
        if text[i] == "{":
            brace_count += 1
        elif text[i] == "}":
            brace_count -= 1
            if brace_count == 0:
                end = i + 1
                break
    else:
        return

    history_block = text[start:end]
    new_history = rewrite_history(history_block, new_owner)

    new_text = text[:start] + new_history + text[end:]
    path.write_text(new_text, encoding="utf-8")


# ===== MAIN =====

def main():
    for file in STATES_DIR.glob("*.txt"):
        state_id = extract_state_id(file.name)
        if state_id in STATE_TRANSFERS:
            new_owner = STATE_TRANSFERS[state_id]
            process_file(file, new_owner)
            print(f"State {state_id}: owner/controller/core → {new_owner}")


if __name__ == "__main__":
    main()