import os
from config import MAX_CHARS

def get_file_content(working_directory, file_path):
    combined_file_path = os.path.join(working_directory, file_path)
    abs_working_directory = os.path.abspath(working_directory)
    abs_combined_file_path = os.path.abspath(combined_file_path)
    if os.path.commonpath([abs_working_directory, abs_combined_file_path])!=abs_working_directory:
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
    if not os.path.isfile(abs_combined_file_path):
        return f'Error: File not found or is not a regular file: "{file_path}"'
    try:
        with open(abs_combined_file_path, "r", encoding="utf-8") as f:
            chunk = f.read(MAX_CHARS+1)
            if len(chunk)<=MAX_CHARS:
                file_content_string = chunk
            else:
                file_content_string= chunk[:-1]+f'[...File "{file_path}" truncated at {MAX_CHARS} characters]'
            return file_content_string
    except Exception as e:
        return f"Error: {str(e)}"
        
