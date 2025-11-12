# python
import os
import sys

print("Probe start")

# 1) Show which calculator/main.py will run
calc_main_path = os.path.abspath("calculator/main.py")
print("Expected calculator/main.py path:", calc_main_path)

# 2) Print its contents (first 200 chars)
try:
    with open(calc_main_path, "r") as f:
        content = f.read()
    print("--- calculator/main.py content (first 200 chars) ---")
    print(content[:200].replace("\n", "\\n"))
    print("---------------------------------------------------")
except Exception as e:
    print("Error reading calculator/main.py:", e)

# 3) Try to run it via uv as the CLI does
print("Running: uv run calculator/main.py \"3 + 7 * 2\"")
print("---- OUTPUT BELOW ----")
