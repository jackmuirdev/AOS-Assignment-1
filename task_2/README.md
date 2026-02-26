# Task 2 – University High Performance Computing Job Scheduler

**File:** `task_2.py`

This script simulates a High Performance Computing (HPC) job scheduling system used in a university laboratory environment.

It provides a **menu-driven interface** that allows students to:

- View pending computational jobs
- Submit new job requests
- Process jobs using Round Robin scheduling
- Process jobs using Priority scheduling
- View completed jobs
- Maintain a full scheduling activity log

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

```bash
python3 task_2.py
```

## Features

Upon execution, the script displays the following menu:

```bash
1) View Pending Jobs
2) Submit a New Job
3) Process Jobs (Round Robin)
4) Process Jobs (Priority)
5) View Completed Jobs
6) Exit
```

## Functional Overview

### Job Management

- Displays a list of pending jobs with details (student ID, job name, execution time, priority).
- Allows students to submit new jobs with specified execution time and priority.
- All submitted jobs are stored in `job_queue.txt` and logged in `scheduler_log.txt`.
- Each submission is logged with a timestamp for traceability.
- Logs all job submissions and processing activities.

### Scheduling Algorithms

#### Round Robin Scheduling

- Processes jobs in a cyclic order with a fixed time quantum (e.g., 2 seconds).
- Jobs that are not completed within the time quantum are moved to the end of the queue.
- Simulates job execution and updates remaining execution time.
- Moves completed jobs to `completed_jobs.txt` and logs the completion.

#### Priority Scheduling

- Processes jobs based on their priority (lower number indicates higher priority).
- Higher priority jobs are processed first, and jobs with the same priority are processed in the order they were submitted.
- Simulates job execution and updates remaining execution time.
- Moves completed jobs to `completed_jobs.txt` and logs the completion.

### Completed Jobs Management

- Once a job is completed, it is moved from the pending job queue to a completed jobs list.
- Queued jobs are stored in `job_queue.txt`.
- Completed jobs are stored in `completed_jobs.txt`.

### Logging System

The script maintains a log file: `scheduler_log.txt`

- Automatically created if it does not exist.
- Records all job submissions and processing activities with timestamps.
- Provides traceability of job scheduling operations.

### Exit Mechanism

- The user can exit the program gracefully through the menu.
- Implements a safe exit confirmation (Y/N).
- All pending jobs and logs are saved before exiting.

## File Generated During Execution

- `job_queue.txt`: Stores the list of pending jobs.
- `completed_jobs.txt`: Stores the list of completed jobs.
- `scheduler_log.txt`: Stores the log of all scheduling activities.

They are automatically created and updated during the execution of the script.
