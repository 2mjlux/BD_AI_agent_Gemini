import os
from google.genai import types
from pathlib import Path

ALLOWED_DIR = Path("calculator/pkg").resolve()
PROTECTED_FILE = Path("calculator/main.py").resolve()

def _is_allowed_target(working_directory: str, file_path: str) -> (bool, str):
    """
    Enforce:
    - Target must be inside working_directory (your original sandbox)
    - Target must be under calculator/pkg
    - Target must not be calculator/main.py
    """
    abs_working_directory = Path(working_directory).resolve()
    abs_target = (abs_working_directory / file_path).resolve()

    # 1) Must be inside working_directory
    try:
        common = os.path.commonpath([str(abs_working_directory), str(abs_target)])
    except Exception:
        return False, f'Error: Invalid path "{file_path}"'
    if Path(common) != abs_working_directory:
        return False, f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'

    # 2) Block protected file
    if abs_target == PROTECTED_FILE:
        return False, f'Error: Refusing to write to protected file: "{file_path}"'

    # 3) Allow only under calculator/pkg
    if not (abs_target == ALLOWED_DIR or ALLOWED_DIR in abs_target.parents):
        return False, f'Error: Refusing to write outside allowlist (calculator/pkg): "{file_path}"'

    return True, str(abs_target)

def _content_sanity_ok(content: str) -> bool:
    """
    Basic guard against trivial nukes like `print(3)`.
    Allow if code looks non-trivial.
    """
    text = (content or "").strip()
    if len(text) < 30 and "class " not in text and "def " not in text:
        return False
    return True



def write_file(working_directory, file_path, content):
    combined_file_path = os.path.join(working_directory, file_path)
    abs_working_directory = os.path.abspath(working_directory)
    abs_combined_file_path = os.path.abspath(combined_file_path)
    if os.path.commonpath([abs_working_directory, abs_combined_file_path])!=abs_working_directory:
        return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
    try:
        parent_dir = os.path.dirname(abs_combined_file_path)
        if not os.path.exists(parent_dir):
            os.makedirs(parent_dir)
        with open(abs_combined_file_path, "w") as f:
            f.write(content)
        return(f'Successfully wrote to "{file_path}" ({len(content)} characters written)')
    except Exception as e:
        return f"Error: {str(e)}"
            
            
# Building function declaration (schema)
schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Writes specified content to the specified file path.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The file path to read the file from, relative to the working directory. Generates error message if not provided.",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="The content to be written into the file",
            )
        },
    ),
)
