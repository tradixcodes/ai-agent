import os

def get_files_info(working_directory, directory="."):
    full_path = os.path.join(working_directory, directory)

    full_path = os.path.abspath(full_path)
    working_directory = os.path.abspath(working_directory)

    lines = []
    lines.append(f"Result for '{directory}' directory:")

    if not full_path.startswith(working_directory):
        line = " ".join(lines)
        return f'{line}\n\tError: Cannot list "{directory}" as it is outside the permitted working dirctory'
    
    if not os.path.isdir(full_path):
        line = " ".join(lines)
        return f'{line}\n\tError: "{full_path}" is not a directory'

    for filename in os.listdir(full_path):
        file_path = os.path.join(full_path, filename)
        is_dir = os.path.isdir(file_path)
        file_size = os.path.getsize(file_path)
        lines.append(f"- {filename}: file_size={file_size} bytes, is_dir={is_dir}")

    return "\n".join(lines)
