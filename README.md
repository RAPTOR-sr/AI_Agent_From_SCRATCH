# AI Agent From Scratch

A lightweight, terminal-based autonomous AI coding agent built from scratch in Python, powered by Groq's fast LLM inference (`openai/gpt-oss-120b`).

The agent operates in an interactive conversational loop, leverages OpenAI-compatible function calling, and safely executes filesystem actions, targeted code edits, and shell commands to assist with coding, debugging, refactoring, and file management tasks.

---

## 🚀 Features

- **Interactive CLI Interface**: Chat directly with the agent in a clean terminal REPL.
- **Autonomous Tool-Calling Loop**: Uses tool schemas to iteratively plan, invoke tools, inspect outputs, and return a final response.
- **Human-in-the-Loop Safety Controls**:
  - Prompts for confirmation before executing shell commands (`[Y/N]`).
  - Prompts for confirmation before deleting files (`[Y/N]`).
  - Displays a unified diff patch preview and asks for confirmation before applying targeted code modifications (`[Y/N]`).
- **Comprehensive 13-Tool Suite**:
  - 📁 **Filesystem Exploration**: List files, inspect directory trees, view working directory, and check file metadata.
  - 🔍 **Search & Code Navigation**: Search files by name/content and search source code across files with line numbers (automatically ignores `.git`, `.venv`, `__pycache__`, `node_modules`).
  - ✏️ **File Manipulation & Targeted Editing**: Read, write, move, rename, delete files, create directories, and perform targeted patch replacements (`modify_file`).
  - 💻 **Shell Execution**: Run arbitrary terminal commands with built-in timeout safeguards (120s).

---

## 📁 Project Structure

```
AI_Agent_From_SCRATCH/
├── src/
│   └── ai_agent_from_scratch/
│       ├── __init__.py
│       ├── agent.py          # Agent loop & tool execution logic
│       ├── config.py         # Environment variables & Groq client setup
│       ├── main.py           # CLI entrypoint, system prompt, and interactive REPL
│       └── tools/
│           ├── __init__.py   # Tool registry mapping
│           ├── file_tools.py # File manipulation, diff patching, & search utilities
│           ├── schemas.py    # OpenAI-compatible function calling schemas
│           └── shell_tools.py# Shell execution with user confirmation
├── test_agent/               # Test scripts and example projects
│   └── example.py
├── main.py                   # Root entry point
├── pyproject.toml            # Project configuration & dependencies
└── README.md                 # Project documentation
```

---

## 🛠️ Prerequisites

- **Python**: `>= 3.13`
- **Groq API Key**: Obtain one from the [Groq Console](https://console.groq.com/).
- **Package Manager**: [uv](https://github.com/astral-sh/uv) (recommended) or standard `pip`.

---

## ⚙️ Installation & Setup

1. **Clone the Repository**:
   ```bash
   git clone <repository-url>
   cd AI_Agent_From_SCRATCH
   ```

2. **Set up Environment Variables**:
   Create a `.env` file in the root directory:
   ```env
   GROQ_API_KEY=your_groq_api_key_here
   ```

3. **Install Dependencies**:

   *Using `uv` (recommended):*
   ```bash
   uv sync
   ```

   *Or using `pip` / virtualenv:*
   ```bash
   python -m venv .venv
   # Windows:
   .venv\Scripts\activate
   # Linux/macOS:
   source .venv/bin/activate

   pip install -e .
   ```

---

## 💻 Usage

### Run the Agent

You can start the agent using any of the following methods:

*Using `uv`:*
```bash
uv run ai-agent-from-scratch
# or
uv run python main.py
```

*Using standard Python (with virtual environment active):*
```bash
python main.py
```

### Example Session

```text
Mini agent ready. Type 'exit' to quit.

You: Can you check for any division by zero handling in test_agent/example.py?
Agent: Let me search the code in test_agent/example.py.
[Agent calls search_code]
Found division check at test_agent/example.py:21: if b == 0: raise ZeroDivisionError("Cannot divide by zero")

You: Replace that error message with 'Division by zero is not allowed'
Agent: [Agent reads file and prepares patch]

 Proposed patch:
--- test_agent/example.py
+++ test_agent/example.py
@@ -21,3 +21,3 @@
     if b == 0:
-        raise ZeroDivisionError("Cannot divide by zero")
+        raise ZeroDivisionError("Division by zero is not allowed")
     return a / b

 Apply this patch? [Y/N]: Y
Agent: Applied targeted modification to test_agent/example.py.

You: exit
```

---

## 🧰 Available Tools Reference

| Tool | Parameters | Human Confirmation | Description |
| :--- | :--- | :---: | :--- |
| `list_file` | `path` *(optional)* | No | Returns sorted files/folders in the specified directory (`/` suffix for dirs). |
| `list_directory_tree` | `path` *(optional)* | No | Shows recursive tree structure of directories and files with indentation. |
| `get_current_directory` | None | No | Returns the current working directory path. |
| `get_file_info` | `path` | No | Returns metadata (type, size in bytes, and last modified ISO timestamp). |
| `read_file` | `path` | No | Reads and returns UTF-8 text content from a file. |
| `write_file` | `path`, `content` | No | Creates or overwrites a file with UTF-8 content. |
| `modify_file` | `path`, `old_text`, `new_text` | **Yes `[Y/N]`** | Replaces an exact section in a file, displaying a unified diff preview before applying. |
| `create_directory` | `path` | No | Creates a directory and any missing parent directories. |
| `move_file` | `source`, `destination` | No | Moves or renames a file (prevents accidental destination overwrite). |
| `delete_file` | `path` | **Yes `[Y/N]`** | Safely deletes a file after prompting the user for confirmation. |
| `search_files` | `path`, `name`, `content` | No | Recursively searches files matching filename substring and/or text content. |
| `search_code` | `query`, `path` *(optional)* | No | Recursively searches source code for matching text, ignoring noise folders (`.venv`, `.git`, etc.) and returning line numbers. |
| `run_command` | `command` | **Yes `[Y/N]`** | Prompts user `[Y/N]` and executes shell command with a 120s timeout. |

---

## 📄 License

This project is open source and available under the standard MIT or project license.
