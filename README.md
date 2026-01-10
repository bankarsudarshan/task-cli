# 🧰 Taskman — Command-Line Task Manager

`taskman` is a lightweight and fast command-line tool to manage your tasks directly from the terminal.  
Supports **priority**, **status updates**, **search**, **sorting**, **filtered listing**, and **Google Calendar integration** — without needing any GUI or browser.  
Inspired by the project idea on [roadmap.sh](https://roadmap.sh/projects/task-tracker).


## 🚀 Installation

The recommended way to install **taskman** is using **`uv`**, which provides fast, isolated installs for CLI tools (similar to `pipx`, but faster and simpler).

### 1️⃣ Install `uv` (if not already installed)
<details>
<summary><strong>Linux / macOS</strong></summary>

```bash
curl -Ls https://astral.sh/uv/install.sh | sh
```
</details>
<details>

<summary><strong>Windows (PowerShell)</strong></summary>

```powershell
irm https://astral.sh/uv/install.ps1 | iex
```

Verify installation:

```bash
uv --version
```
</details>

### 2️⃣ Install `taskman` using `uv`

```bash
uv tool install git+https://github.com/bankarsudarshan/task-cli.git
```

### 3️⃣ Verify installation

```bash
taskman --help
```

### 4️⃣ More...
<details>
<summary> 🔄 Upgrade </summary>

```bash
uv tool upgrade taskman
```
</details>

<details>
<summary> 🧹 Uninstall </summary>

```bash
uv tool uninstall taskman
```
</details>

<details>
<summary> 🛠 Development install (optional)  </h3></summary>

If you’re working on the source code:

```bash
git clone https://github.com/bankarsudarshan/task-cli.git
cd task-cli
uv sync
source .venv/bin/activate
taskman
```
</details>

---

## 🧑‍💻 Usage

Run from anywhere:

```bash
taskman [command] [options]
```

### 📝 Commands Overview

| Command                 | Description                         |
| ----------------------- | ----------------------------------- |
| `add <desc>`            | Add a new task                      |
| `update <id>`           | Update task fields                  |
| `delete <id>`           | Delete a task                       |
| `list`                  | List tasks (with filters & sorting) |
| `mark-done <id>`        | Mark task as done                   |
| `mark-in-progress <id>` | Mark task as in-progress            |
| `clear [status]`        | Remove tasks                        |
| `search <text>`         | Search task descriptions            |
| `gcal add <id>`         | Add task to Google Calendar         |
| `gcal sync`             | Sync tasks with Calendar            |

### More details on usage of commands

<details>
<summary>➕ Add Tasks</summary>

```bash
taskman add "Buy milk"
taskman add "Study DSA" -p high
```

Priority values:

```
low | medium | high
```
</details>

<details>
<summary>✏️ Update Tasks</summary>

You can update **any field independently**.

```bash
# Change only description
taskman update 1 -d "Finish book - chapter 5"

# Change priority only
taskman update 1 -p high

# Change status only
taskman update 1 -s done

# Update everything
taskman update 1 -d "Final revision" -p high -s done
```

</details>


<details>
<summary>📋 List Tasks (with sorting and filtering)</summary>

<details>
<summary>Filters</summary>

```bash
# All tasks
taskman list

# Only done tasks
taskman list done

# High priority tasks
taskman list -p high

# Done + high priority
taskman list done -p high
```
</details>

<details>
<summary>Sorting</summary>

```bash
# Sort by priority (high → low)
taskman list --sort-by priority

# Sort newest first
taskman list --sort-by updatedAt --order desc
```

Supported sort fields:

```
id, createdAt, updatedAt, priority, status
```

Sort order:

```
--order asc   (default)
--order desc
```

</details>

</details>

<details>
<summary>🔄 Updating Task Status</summary>

```bash
taskman mark-done 1
taskman mark-in-progress 3
```
</details>

<details>
<summary>🧹 Clear Tasks</summary>

```bash
# Remove all done tasks
taskman clear done

# Remove all tasks
taskman clear
```
</details>

<details>
<summary>🔍 Search Tasks</summary>

```bash
taskman search "report"
taskman search book
```

Searches task **descriptions** (case-insensitive).
</details>

---

## 📂 Data Storage

All tasks are stored in a file in your home directory:

```
~/tasks.json
```

Example structure:

```json
{
  "1": {
    "id": 1,
    "description": "Work on project report",
    "status": "in-progress",
    "priority": "high",
    "createdAt": "2025-11-28 14:25",
    "updatedAt": "2025-11-28 18:47",
    "dueAt": "2025-12-10 18:00"
  }
}
```

---

## 📅 Google Calendar Integration 

Taskman can export tasks with due dates to **Google Calendar**.
This is optional and must be set up once per user.

### ✅ Step 1 — Create Google API Credentials

1. Go to **[Google Cloud Console](https://console.cloud.google.com)**
2. Create a **New Project**
3. Open **APIs & Services → Library**
4. Enable **Google Calendar API**
5. Go to **OAuth Consent Screen**

   * User type: **External**
   * App name: `Taskman CLI`
   * Add scope:

     ```
     https://www.googleapis.com/auth/calendar.events
     ```
   * Save
6. Go to **Credentials → Create Credentials → OAuth Client ID**

   * Application type: **Desktop App**
   * Create
7. Click **Download JSON**

Rename the downloaded file to:

```
credentials.json
```


### ✅ Step 2 — Place `credentials.json` on Your System

Create this directory:

```bash
mkdir -p ~/.config/taskman/
```

Then move the file here:

```bash
mv ~/Downloads/credentials.json ~/.config/taskman/credentials.json
```


### ✅ Step 3 — Add a Task with a Due Date

```bash
taskman add "Submit assignment" --due "2025-12-10 18:00"
```


### ✅ Step 4 — Export Task to Google Calendar

```bash
taskman gcal add 1
```

On first run:

* A browser window will open
* Log in to your Google account
* Allow calendar access
* A `token.json` file will be created automatically:

```
~/.config/taskman/token.json
```

From now on, no further login is needed.


### ✅ Sync All Due Tasks at Once

```bash
taskman gcal sync
```

This will export **all tasks that contain a `dueAt` field**.


## 🔐 Security Notes

* `credentials.json` is **never uploaded or shared**
* `token.json` is stored **locally** only
* You should **never commit these files to Git**
* Each user authenticates with **their own Google account**
* Add to `.gitignore`:

```
~/.config/taskman/credentials.json
~/.config/taskman/token.json
```

---

## 💬 Feedback

Found a bug or have ideas?
Open an issue here:

👉 **[https://github.com/bankarsudarshan/task-cli/issues](https://github.com/bankarsudarshan/task-cli/issues)**