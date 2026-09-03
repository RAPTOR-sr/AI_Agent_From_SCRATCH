# AI Agent From Scratch

A lightweight, terminal-based autonomous AI coding agent built from scratch in Python, powered by Groq's fast LLM inference (`openai/gpt-oss-120b`).

The agent operates in an interactive conversational loop, leverages OpenAI-compatible function calling, and safely executes filesystem actions and shell commands to assist with coding, debugging, and file management tasks.

---

## 🚀 Features

- **Interactive CLI Interface**: Chat directly with the agent in a clean terminal REPL.
- **Autonomous Tool-Calling Loop**: Uses tool schemas to iteratively plan, call tools, inspect outputs, and return a final response.
- **Human-in-the-Loop Safety**: Prompts for explicit user confirmation before executing potentially destructive actions (running shell commands, deleting files).
- **Comprehensive Filesystem & Shell Toolkit**:
  - 📁 **Exploration**: List files, inspect directory trees, view working directory, and check file metadata.
  - 🔍 **Search**: Find files recursively by filename and/or content.
  - ✏️ **File Operations**: Read, write, move, rename, and delete files, as well as create directories.
  - 💻 **Shell Execution**: Run arbitrary terminal commands with built-in timeout safeguards.

---

## 📁 Project Structure

```
AI_Agent_From_SCRATCH/
├── src/
│   └── ai_agent_from_scratch/
│       ├── __init__.py
│       ├── agent.py          # Agent loop & tool execution logic
│       ├── config.py         # Environment variables & Groq client setup
│       ├── main.py           # CLI entrypoint and interactive REPL
│       └── tools/
│           ├── __init__.py   # Tool registry mapping
│           ├── file_tools.py # File manipulation & search utilities
│           ├── schemas.py    # OpenAI-compatible function calling schemas
│           └── shell_tools.py# Shell execution with user confirmation
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

You: Can you list all files in the current directory and check what python packages we depend on?
Agent: I have checked your directory and inspected pyproject.toml. The project depends on:
- groq (>=1.7.0)
- python-dotenv (>=1.2.3)

You: Delete the obsolete file temp.log
Delete 'temp.log'? [Y/N]: Y
Agent: Deleted file: temp.log

You: Run pytest on this repository
Run 'pytest'? [Y/N]: Y
Agent: pytest command executed. 0 passed in 0.05s.

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
| `create_directory` | `path` | No | Creates a directory and any missing parent directories. |
| `move_file` | `source`, `destination` | No | Moves or renames a file (prevents accidental destination overwrite). |
| `search_files` | `path`, `name`, `content` | No | Recursively searches files matching filename substring and/or text content. |
| `delete_file` | `path` | **Yes `[Y/N]`** | Safely deletes a file after prompting the user for confirmation. |
| `run_command` | `command` | **Yes `[Y/N]`** | Prompts user `[Y/N]` and executes shell command (120s timeout). |

---

## 📄 License

This project is open source and available under the standard project license.
