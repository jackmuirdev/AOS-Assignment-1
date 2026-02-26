# Task 1 – University Data Centre Process & Resource Management System

**File:** `task-1.sh`

This script simulates a system administration tool used to manage shared Linux servers in a university data centre environment.

It provides a **menu-driven interface** that allows administrators to:

- Monitor system resource usage
- Identify and manage memory-intensive processes
- Inspect disk usage
- Archive large log files
- Maintain an administrative activity log

## Setup Instructions

### 1. Grant Execute Permission

Before running the script, make it executable:

```bash
chmod +x task-1.sh
```

### 2. Execute the Script

```bash
./task-1.sh
```

## Features

Upon execution, the script displays the following menu:

```bash
1) Display CPU and Memory Usage
2) List Top 10 Memory Consuming Processes
3) Terminate a Process
4) Inspect Disk Usage
5) Archive Large Log Files
6) Exit
```

## Functional Overview

### Process Monitoring and Management

- Displays current CPU and memory usage.
- Lists the top 10 memory-consuming processes (PID, user, CPU %, memory %).
- Allows termination of a selected process after confirmation.
- Prevents termination of critical system processes.
- Logs all administrative actions.

### Disk Inspection and Log Archiving

- Inspects disk usage for a specified directory.
- Detects .log files larger than 50MB.
- Automatically creates an ArchiveLogs directory if it does not exist.
- Compresses large log files with timestamped filenames.
- Displays a warning if ArchiveLogs exceeds 1GB.

### Logging System

The script maintains a log file: `system_monitor_log.txt`

- Automatically created if it does not exist.
- Records all administrative actions with timestamps.
- Provides traceability of system management operations.

### Exit Mechanism

- The user can exit the program gracefully through the menu.
- Implements a safe exit confirmation (Y/N).
- Logs exit activity before terminating.

## File Generated During Execution

- `system_monitor_log.txt`: Administrative action log.
- `ArchiveLogs/`: Directory containing compressed archived log files.

Both are created automatically if not present.
