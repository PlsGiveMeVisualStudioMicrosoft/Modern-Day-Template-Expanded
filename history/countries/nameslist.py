"""
List Files in Folder
=====================
Prints the names of all files in the specified folder.
"""

import os

FOLDER = r"C:\Users\User\Documents\Paradox Interactive\Hearts of Iron IV\mod\Modern Day Template Expanded\history\countries"

def main():
    if not os.path.isdir(FOLDER):
        print(f"ERROR: Folder not found:\n  {FOLDER}")
        input("\nPress Enter to exit.")
        return

    files = sorted(f for f in os.listdir(FOLDER) if os.path.isfile(os.path.join(FOLDER, f)))

    if not files:
        print("No files found.")
        input("\nPress Enter to exit.")
        return

    print(f"Found {len(files)} file(s) in:\n  {FOLDER}\n")
    for f in files:
        print(f)

    input(f"\n{len(files)} files listed. Press Enter to exit.")

if __name__ == "__main__":
    main()