# Task 3 – Secure Examination Submission and Access Control System

**File:** `task_3.py`

This script implements a secure examination submission system with access control for a university or school environment. It ensures students can submit assignments safely, detects duplicate submissions, monitors suspicious login activity, and logs all system events for audit purposes.

It provides a **menu-driven interface** that allows students to:

- Submit assignments (.pdf or .docx) with file size validation
- Check for duplicate submissions
- List all submitted assignments
- Simulate login attempts with security checks
- Detect suspicious login activity (repeated attempts within 60 seconds)
- Lock accounts after multiple failed login attempts
- Maintain a full submission and login activity log

## Setup Instructions

### 1. Check if Python 3 is installed

Check python version:

```bash
python3 --version
```

if Python 3 is not installed, you can install it using your package manager. For example, on Debian-based systems:

```bash
sudo apt update
sudo apt install python3
```

### 2. Execute the Script

The script is run via a Bash menu interface that interacts with the Python backend:

```bash
./task_3_menu.sh
```

## Features

Upon execution, the script displays the following menu:

```bash
===== Secure Examination System =====
1) Submit Assignment
2) Check Duplicate Submission
3) List Submitted Assignments
4) Simulate Login Attempt
5) Exit
```

## Functional Overview

### Assignment Submission

- Accepts only .pdf and .docx files.
- Rejects files larger than 5 MB (configurable in task_3.py).
- Submissions are validated by file hash to prevent duplicates, even if the filename is changed.
- Submissions are stored in the submissions/ directory.
- Each successful submission is logged in submission_log.txt with a timestamp.
- Duplicate submissions are detected and logged as DUPLICATE_CONTENT.

### Duplicate Submission Check

- Allows students to check if a file has already been submitted.
- Checks both filename and content hash to detect exact duplicates.
- Provides a clear message if the file is a duplicate.

### Login and Access Control

- Simulates login attempts with a preset password for demonstration.
- Tracks failed login attempts using the submission log for persistent state across script executions.
- Locks accounts after 3 failed login attempts.
- Detects suspicious activity: multiple login attempts within 60 seconds are flagged.
- All login attempts (successful, failed, suspicious, locked) are logged in submission_log.txt.

### Logging System

The script maintains a log file: `scheduler_log.txt`

- Records all assignment submissions and login attempts with timestamps.
- Includes status codes like SUCCESS, FAILED, DUPLICATE_CONTENT, LOCKED, and SUSPICIOUS.
- Provides an audit trail for all system activities.

### Exit Mechanism

- The user can exit the program gracefully through the menu.
- Implements a safe exit confirmation (Y/N).
- All pending jobs and logs are saved before exiting.

## File Management

- `submissions/`: stores submitted assignment files.
- `submission_records.txt`: maintains student IDs, filenames, and file hashes.
- `submission_log.txt`: stores logs of all submission and login activity.

They are automatically created and updated during the execution of the script.
