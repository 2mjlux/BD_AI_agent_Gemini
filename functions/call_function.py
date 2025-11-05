import os
from google.genai import types

from functions.write_file import write_file
from functions.get_file_content import get_file_content
from functions.run_python_file import run_python_file
from functions.get_files_info import get_files_info


def call_function(function_call_part, verbose=False):
    if verbose == True:
        print(f"Calling function: {function_call_part.name}({function_call_part.args})")
    else:
        print(f" - Calling function: {function_call_part.name}")
    
    function_map = {
        "write_file": write_file,
        "get_file_content": get_file_content,
        "run_python_file": run_python_file,
        "get_files_info": get_files_info
    }
    
    function_name = function_call_part.name
    
    # Check if function exists
    if function_name not in function_map:
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_name,
                    response={"error": f"Unknown function: {function_name}"},
                )
            ],
        )

    # Get the actual function
    actual_function = function_map[function_name]
    print(f"DEBUG: Got function: {actual_function}")
        
    # Get the args that the AI provided
    args = dict(function_call_part.args)
    
    # Add working_directory to the args
    args['working_directory'] = './calculator'
    
    # If AI ask for "calculator" directory, it means "." (current directory)
    if 'directory' in args and args['directory'] == 'calculator':
        args['directory'] = '.'
        
    # Call the actual function with the args
    function_result = actual_function(**args)
    
    # Return the result
    return types.Content(
        role="tool",
        parts=[
            types.Part.from_function_response(
                name=function_name,
                response={"result": function_result},
            )
        ],
    )
        
