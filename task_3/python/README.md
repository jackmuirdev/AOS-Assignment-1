# Task 3 – Python Solution

Pure Python implementation of the secure examination submission and access control system. No third-party packages are required.

## Requirements

- Python 3.8+
- Standard library only (no third-party packages)

### Check your Python version

```bash
python3 --version
```

### Install Python if missing

On Debian/Ubuntu-based systems:

```bash
sudo apt update
sudo apt install python3
```

On macOS (via Homebrew):

```bash
brew install python3
```

## How to Run

From within the `python/` folder:

```bash
python3 task_3.py
```

From the project root:

```bash
python3 task_3/python/task_3.py
```

## Menu Options

```
===== Secure Examination System =====
1) Submit Assignment
2) Check Duplicate Submission
3) List Submitted Assignments
4) Simulate Login Attempt
5) Exit
```

## Functional Overview

### Assignment Submission

- Accepts only `.pdf` and `.docx` files.
- Rejects files larger than 5 MB.
- Computes a SHA-256 hash of the file content to detect duplicates even if the filename changes.
- Copies accepted files into the `submissions/` subdirectory.
- Appends a record to `submission_records.txt` with the student ID, filename, and file hash.
- Logs all submission events (success, invalid format, too large, duplicate) to `submission_log.txt`.

### Duplicate Submission Check

- Accepts a file path and checks both the filename and SHA-256 content hash against existing records.

### List Submitted Assignments

- Prints all records from `submission_records.txt`.

### Login and Access Control

- Simulates login with a preset password (`password123`).
- Tracks failed login attempts persistently via `submission_log.txt`.
- Locks an account after 3 consecutive failed login attempts.
- Detects suspicious activity: flags multiple login attempts within 60 seconds.
- All login events (SUCCESS, FAILED, LOCKED, SUSPICIOUS) are logged.

### Exit

- Prompts for Y/N confirmation before exiting.
- Logs the exit event to `submission_log.txt`.

## File Management

| File | Purpose |
|---|---|
| `submissions/` | Stores copies of submitted assignment files |
| `submission_records.txt` | Records student ID, filename, and SHA-256 hash per submission |
| `submission_log.txt` | Timestamped audit log of all submission and login events |

All files are created automatically on first run within the `python/` folder.

## Implementation Notes

- **SHA-256 hashing**: Uses `hashlib.sha256` from the Python standard library; reads files in 8 KB chunks to handle large files without loading them entirely into memory.
- **File copying**: Uses `shutil.copy2` to preserve file metadata when copying into `submissions/`.
- **Path handling**: All file paths are anchored to `__file__` so the script works correctly regardless of the working directory it is invoked from.
- **Suspicious activity detection**: Uses `time.time()` for Unix epoch timestamps when comparing login attempt times.
