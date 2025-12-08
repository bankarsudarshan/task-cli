# 🧰 Taskman — Command-Line Task Manager

`taskman` is a lightweight and fast command-line tool to manage your tasks directly from the terminal.  
Supports **priority**, **status updates**, **search**, **sorting**, **filtered listing**, and **Google Calendar integration** — without needing any GUI or browser.  
Inspired by the project idea on [roadmap.sh](https://roadmap.sh/projects/task-tracker).

---

## 🚀 Installation

You should install CLI tools **in isolation** using `pipx`.

### 1️⃣ Install `pipx` (if not already installed)

**Linux/macOS**
```bash
python3 -m pip install --user pipx
python3 -m pipx ensurepath
```

**Windows**

```powershell
pip install pipx
python -m pipx ensurepath
```

> Restart your terminal after installation.
> If it still fails, use `python -m pipx` instead of `pipx`.

### 2️⃣ Install `taskman` using pipx

```bash
pipx install git+https://github.com/bankarsudarshan/task-cli.git
```

---

## 🧑‍💻 Usage

Run from anywhere:

```bash
taskman [command] [options]
```

---

## 📝 Commands Overview

| Command                 | Purpose                                     | Example                           |
| ----------------------- | ------------------------------------------- | --------------------------------- |
| `add <desc>`            | Add new task                                | `taskman add "Buy milk"`          |
| `add <desc> -p high`    | Add with priority (`low`, `medium`, `high`) | `taskman add "Study DSA" -p high` |
| `update <id> [options]` | Update task fields                          | See below                         |
| `delete <id>`           | Delete task                                 | `taskman delete 2`                |
| `list`                  | List all tasks                              | `taskman list`                    |
| `list todo -p high`     | Filter by status + priority                 | `taskman list todo -p high`       |
| `mark-done <id>`        | Mark as done                                | `taskman mark-done 1`             |
| `mark-in-progress <id>` | Mark as in-progress                         | `taskman mark-in-progress 3`      |
| `clear [status]`        | Remove tasks                                | `taskman clear done`              |
| `search <text>`         | Search descriptions                         | `taskman search book`             |
| `gcal add <id>`         | Export a task to Google Calendar            | `taskman gcal add 3`              |
| `gcal sync`             | Sync all tasks with due dates to Calendar   | `taskman gcal sync`               |

---

## 🔄 Update Command (Flexible)

You can update **any field independently** — description is optional.

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

---

## 📋 List Command — Filters + Sorting

```bash
# All tasks
taskman list

# Only done tasks
taskman list done

# Only high priority
taskman list -p high

# Done + high priority
taskman list done -p high

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
--order asc     (default)
--order desc
```

---

## 🔍 Search Tasks

```bash
taskman search "report"
taskman search book
```

Returns all tasks whose **description** contains the given keyword (case-insensitive).

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

---

### ✅ Step 2 — Place `credentials.json` on Your System

Create this directory:

```bash
mkdir -p ~/.config/taskman/
```

Then move the file here:

```bash
mv ~/Downloads/credentials.json ~/.config/taskman/credentials.json
```

---

### ✅ Step 3 — Add a Task with a Due Date

```bash
taskman add "Submit assignment" --due "2025-12-10 18:00"
```

---

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

---

### ✅ Sync All Due Tasks at Once

```bash
taskman gcal sync
```

This will export **all tasks that contain a `dueAt` field**.

---

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