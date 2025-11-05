import os
from google.genai import types


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
