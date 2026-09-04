import os
import shutil
import difflib
from pathlib import Path
from datetime import datetime

def list_file(path="."):
    """Return a sorted list of files and directories at the given path.

    Directories are marked with a trailing slash.
    The current directory is used when no path is provided.
    """
    entries = []

    for entry in os.scandir(path):
        entries.append(entry.name + ("/" if entry.is_dir() else ""))

    return "\n".join(sorted(entries)) or "(empty directory)"


def read_file(path):
    """Read and return the UTF-8 text content of a file."""
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def write_file(path, content):
    """Write UTF-8 text content to a file, creating or replacing it."""
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)

    return f"Saved {path} ({len(content)} characters)"

def search_files(path = ".", name = None, content= None):
    """Search recursively for files by filename and/or text content."""
    if not name and not content:
        raise ValueError("Provide name or content")

    results = []
    for file_path in Path(path).rglob("*"):
        if not file_path.is_file():
            continue

        if name and name.lower() not in file_path.name.lower():
            continue

        if content:
            try:
                text = file_path.read_text(encoding="utf-8")
            except (UnicodeDecodeError, OSError):
                continue
            if content.lower() not in text.lower():
                continue
        results.append(str(file_path))
    return "\n".join(results) or "No matching files found."

def create_directory(path):
    """Create a directory, including missing parent directories."""
    os.makedirs(path, exist_ok=False)
    return f"Created directory: {path}"


def delete_file(path):
    """Delete one file after asking for user confirmation."""
    if not os.path.isfile(path):
        raise FileNotFoundError(f"File not found: {path}")

    answer = input(f"Delete '{path}'? [Y/N]: ")
    if answer.strip().lower() != "y":
        return "User declined to delete the file."

    os.remove(path)
    return f"Deleted file: {path}"


def move_file(source, destination):
    """Move or rename a file without overwriting an existing destination."""
    if not os.path.isfile(source):
        raise FileNotFoundError(f"File not found: {source}")
    if os.path.exists(destination):
        raise FileExistsError(f"Destination already exists: {destination}")

    import shutil
    shutil.move(source, destination)
    return f"Moved {source} to {destination}"


def get_file_info(path):
    """Return the size, type, and modified time for a path."""
    if not os.path.exists(path):
        raise FileNotFoundError(f"Path not found: {path}")

    file_info = os.stat(path)
    from datetime import datetime
    return {
        "path": path,
        "type": "directory" if os.path.isdir(path) else "file",
        "size": file_info.st_size,
        "modified": datetime.fromtimestamp(file_info.st_mtime).isoformat(),
    }


def get_current_directory():
    """Return the current working directory."""
    return os.getcwd()


def list_directory_tree(path="."):
    """Return a recursive listing of directories and files."""
    lines = []
    root = Path(path)

    for current_path, directories, files in os.walk(path):
        relative_path = Path(current_path).relative_to(root)
        level = len(relative_path.parts)
        indent = "  " * level
        directory_name = root.name if level == 0 else Path(current_path).name
        lines.append(f"{indent}{directory_name}/")

        for directory in sorted(directories):
            lines.append(f"{indent}  {directory}/")
        for file_name in sorted(files):
            lines.append(f"{indent}  {file_name}")

    return "\n".join(lines) or "(empty directory)"

def modify_file(path, old_text, new_text):
    file_path = Path(path)

    if not file_path.is_file():
        raise FileNotFoundError(f"File not found: {path}")

    current_text = file_path.read_text(encoding="utf-8")

    occurrences = current_text.count(old_text)

    if occurrences == 0:
        raise ValueError("The old text was not found in the file.")

    if occurrences > 1:
        raise ValueError(
            f"The old text appears {occurrences} times. "
            "Provide a more spacific section"
        )

    updated_text = current_text.replace(old_text, new_text, 1)

    diff = "\n".join(
        difflib.unified_diff(
            current_text.splitlines(),
            updated_text.splitlines(),
            fromfile=path,
            tofile=path,
            lineterm=""
        )
    )

    print("\n Proposed patch:\n")
    print(diff)

    answer = input("\n Apply this patch? [Y/N]: ")

    if answer.strip().lower() != "y":
        return "User declined to apply the patch."

    file_path.write_text(updated_text, encoding="utf-8")

    return f"Applied tarheted modification to {path}"