import os
import re

folder = r"C:\Users\User\Documents\Paradox Interactive\Hearts of Iron IV\mod\Modern Day Template Expanded\common\decisions\categories"

flag_line = "\t\thas_global_flag = reenable_vanilla_decisions\n"

for root, dirs, files in os.walk(folder):
    for file in files:
        if file.endswith(".txt"):
            path = os.path.join(root, file)

            with open(path, "r", encoding="utf-8") as f:
                lines = f.readlines()

            new_lines = []
            inside_allowed = False
            brace_depth = 0
            flag_present = False

            for line in lines:

                # Fix existing country flag
                line = line.replace(
                    "has_country_flag = reenable_vanilla_decisions",
                    "has_global_flag = reenable_vanilla_decisions"
                )

                stripped = line.strip()

                if re.match(r'allowed\s*=\s*\{', stripped):
                    inside_allowed = True
                    brace_depth = 1
                    flag_present = False
                    new_lines.append(line)
                    continue

                if inside_allowed:
                    brace_depth += line.count("{")
                    brace_depth -= line.count("}")

                    if "has_global_flag = reenable_vanilla_decisions" in line:
                        flag_present = True

                    if brace_depth == 0:
                        if not flag_present:
                            new_lines.append(flag_line)
                        inside_allowed = False

                new_lines.append(line)

            with open(path, "w", encoding="utf-8") as f:
                f.writelines(new_lines)

print("Finished. All flags converted and allowed blocks updated.")