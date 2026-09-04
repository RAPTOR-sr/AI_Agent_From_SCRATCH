from .file_tools import (
    create_directory,
    delete_file,
    get_current_directory,
    get_file_info,
    list_directory_tree,
    list_file,
    move_file,
    read_file,
    search_files,
    write_file,
    modify_file,
)
from .shell_tools import run_command


TOOLS = {
    "list_file": list_file,
    "read_file": read_file,
    "write_file": write_file,
    "run_command": run_command,
    "search_files": search_files,
    "create_directory": create_directory,
    "delete_file": delete_file,
    "move_file": move_file,
    "get_file_info": get_file_info,
    "get_current_directory": get_current_directory,
    "list_directory_tree": list_directory_tree,
    "modify_file": modify_file,
}