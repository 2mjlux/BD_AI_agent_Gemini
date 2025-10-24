import os
import subprocess

def run_python_file(working_directory, file_path, args=[]):
    combined_file_path = os.path.join(working_directory, file_path)
    abs_working_directory = os.path.abspath(working_directory)
    abs_combined_file_path = os.path.abspath(combined_file_path)
    if os.path.commonpath([abs_working_directory, abs_combined_file_path])!=abs_working_directory:
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
    if not os.path.exists(abs_combined_file_path):
        return f'Error: File "{file_path}" not found.'
    if not file_path.endswith(".py"):
        return f'Error: "{file_path}" is not a Python file.'
    try:   
        result = subprocess.run(["python", abs_combined_file_path] + args,
        capture_output=True, text=True, cwd=abs_working_directory, timeout =30)
        output_parts = []
        if result.stdout:
            output_parts.append(f"STDOUT:\n{result.stdout}")
        if result.stderr:
            output_parts.append(f"STDERR:\n{result.stderr}")
        if result.returncode != 0:
            output_parts.append(f"Process exited with code {result.returncode}")
        if output_parts:
            return "\n".join(output_parts)
        else:
            return "No output produced."        
    except Exception as e:
        return f"Error: executing Python file: {e}"
        
