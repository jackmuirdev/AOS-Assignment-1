# Task 3 – Bash Solution

Pure Bash implementation of the secure examination submission and access control system.

## Requirements

- Bash 4+
- `shasum` (macOS) or `sha256sum` (Linux) — available by default on both platforms

## How to Run

From within the `bash/` folder:

```bash
bash task_3.sh
```

From the project root:

```bash
bash task_3/bash/task_3.sh
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

All files are created automatically on first run within the `bash/` folder.

## Implementation Notes

- **SHA-256 hashing**: Detects `shasum` (macOS) or `sha256sum` (Linux) at startup and uses whichever is available.
- **File size**: Uses `stat` with platform-specific flags (`-f %z` on macOS, `-c %s` on Linux).
- **Suspicious activity detection**: Uses `date +%s` to obtain Unix epoch timestamps for comparing login attempt times.
- All file paths are resolved relative to the script's own directory, so the script works correctly regardless of the working directory it is invoked from.
