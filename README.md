# 🧰 Taskman — Command-Line Task Manager

`taskman` is a simple and lightweight command-line tool to manage your daily tasks right from the terminal.  
You can add, update, delete, list, and mark tasks as done or in-progress — all in one place.

## 🚀 Installation

It’s best to install command-line tools in **isolation** using [`pipx`](https://pypa.github.io/pipx/).

### 1️⃣ Install `pipx` (if not already installed)

```bash
python3 -m pip install --user pipx
python3 -m pipx ensurepath
```
Restart your terminal (or run source ~/.bashrc) so pipx is available in your PATH.

### 2️⃣ Install `taskman` using pipx (from GitHub)

You can install the tool directly from the GitHub repository using `pipx`:

```bash
pipx install git+https://github.com/bankarsudarshan/task-cli.git
```

## 🧑‍💻 Usage

After installation, you can run taskman directly from anywhere:
```bash
taskman [command] [options]
```

### 📝 Commands
| Command                  | Description                                                    | Example                                            |
| ------------------------ | -------------------------------------------------------------- | -------------------------------------------------- |
| `add <description>`      | Add a new task                                                 | `taskman add "Buy groceries"`                      |
| `update <id> <new_desc>` | Update a task’s description                                    | `taskman update 1 "Buy groceries and cook dinner"` |
| `delete <id>`            | Delete a task                                                  | `taskman delete 1`                                 |
| `list [status]`          | List tasks by status (`todo`, `in-progress`, `done`, or `all`) | `taskman list todo`                                |
| `mark-done <id>`         | Mark a task as done                                            | `taskman mark-done 2`                              |
| `mark-in-progress <id>`  | Mark a task as in progress                                     | `taskman mark-in-progress 3`                       |
| `clear [status]`         | Clear all tasks or by status                                   | `taskman clear done`                               |

### 🧩 Examples
```bash
# Add a few tasks
taskman add "Finish reading book"
taskman add "Work on project report"

# List all tasks
taskman list

# Mark one as done
taskman mark-done 1

# View only pending tasks
taskman list todo
```

## 📂 Data Storage
By default, taskman stores your tasks in a JSON file in `tasks.json` file in the directory where you run `taskman`  
You can open this file manually if you want to inspect or back up your data.

## 💬 Feedback

Have ideas or found a bug?
Open an issue on [GitHub](github.com/bankarsudarshan/task-cli/issues)