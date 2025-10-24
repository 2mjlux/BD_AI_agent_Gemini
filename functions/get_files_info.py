import os

def get_files_info(working_directory, directory="."):
    
    # combine paths
    full_path_requested = os.path.join(working_directory, directory)
    
    # convert to absolute paths
    abs_working_directory = os.path.abspath(working_directory)
    abs_full_path_requested = os.path.abspath(full_path_requested)
    
    # check whether path requested inside working directory
    if not abs_full_path_requested.startswith(abs_working_directory):
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
    
    # check whether path requested is a directory
    if not os.path.isdir(abs_full_path_requested):
        return f'Error: "{directory}" is not a directory'
    
    # list contents of requested directory
    try:
        requested_dir_list = os.listdir(abs_full_path_requested)
        requested_dir_contents = ""
        for item in requested_dir_list:
            item_path = os.path.join(abs_full_path_requested, item)
            requested_dir_contents += f" - {item}: file_size={os.path.getsize(item_path)} bytes, is_dir={os.path.isdir(item_path)}\n"
        return requested_dir_contents
    except Exception as e:
        return f"Error: {str(e)}"
