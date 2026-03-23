# Task 3 – Secure Examination Submission and Access Control System

This task implements a secure examination submission system with interactive access control. Two fully self-contained solutions are provided — one in pure Bash and one in pure Python — each offering identical functionality via the same interactive menu. Both solutions manage their own data files independently.

## Directory Structure

```
task_3/
  bash/
    task_3.sh              # Pure Bash implementation
    README.md              # Bash-specific documentation
    submissions/           # Created at runtime
    submission_log.txt     # Created at runtime
    submission_records.txt # Created at runtime
  python/
    task_3.py              # Pure Python implementation
    README.md              # Python-specific documentation
    submissions/           # Created at runtime
    submission_log.txt     # Created at runtime
    submission_records.txt # Created at runtime
```

## Solutions

| Solution | Language | Entry Point | Documentation |
|---|---|---|---|
| Bash | Bash 4+ | `bash/task_3.sh` | [bash/README.md](bash/README.md) |
| Python | Python 3.8+ | `python/task_3.py` | [python/README.md](python/README.md) |

## Shared Features

- Same five-option interactive menu
- SHA-256 content hashing for duplicate detection
- File validation (type and size)
- Persistent login attempt tracking with lockout after 3 failures
- Suspicious activity detection (multiple attempts within 60 seconds)
- Timestamped audit log for all events
- Each solution's data files are stored independently within its own subfolder
