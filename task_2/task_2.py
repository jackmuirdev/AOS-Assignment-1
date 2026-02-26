import os
from datetime import datetime

JOB_QUEUE_FILE = "job_queue.txt"
COMPLETED_FILE = "completed_jobs.txt"
LOG_FILE = "scheduler_log.txt"
TIME_QUANTUM = 5

def log_event(student_id, job_name, scheduling_type):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(LOG_FILE, "a") as log:
        log.write(f"{timestamp} | {student_id} | {job_name} | {scheduling_type}\n")


def load_jobs():
    jobs = []
    if os.path.exists(JOB_QUEUE_FILE):
        with open(JOB_QUEUE_FILE, "r") as f:
            for line in f:
                parts = line.strip().split(",")
                if len(parts) == 4:
                    jobs.append({
                        "student_id": parts[0],
                        "job_name": parts[1],
                        "execution_time": int(parts[2]),
                        "priority": int(parts[3])
                    })
    return jobs


def save_jobs(jobs):
    with open(JOB_QUEUE_FILE, "w") as f:
        for job in jobs:
            f.write(f"{job['student_id']},{job['job_name']},{job['execution_time']},{job['priority']}\n")


def save_completed_job(job):
    with open(COMPLETED_FILE, "a") as f:
        f.write(f"{job['student_id']},{job['job_name']},{job['priority']}\n")


def view_pending_jobs():
    jobs = load_jobs()
    if not jobs:
        print("\nNo pending jobs.\n")
        return

    print("\nPending Jobs:")
    for job in jobs:
        print(f"Student ID: {job['student_id']}, "
            f"Job: {job['job_name']}, "
            f"Time: {job['execution_time']}s, "
            f"Priority: {job['priority']}")
    print()


def view_completed_jobs():
    if not os.path.exists(COMPLETED_FILE):
        print("\nNo completed jobs.\n")
        return

    print("\nCompleted Jobs:")
    with open(COMPLETED_FILE, "r") as f:
        for line in f:
            print(line.strip())
    print()


def submit_job():
    student_id = input("Enter Student ID: ")
    job_name = input("Enter Job Name: ")

    try:
        execution_time = int(input("Enter Estimated Execution Time (seconds): "))
        priority = int(input("Enter Priority (1-10): "))
        if priority < 1 or priority > 10:
            raise ValueError
    except ValueError:
        print("Invalid input. Please enter valid numbers.")
        return

    with open(JOB_QUEUE_FILE, "a") as f:
        f.write(f"{student_id},{job_name},{execution_time},{priority}\n")

    log_event(student_id, job_name, "SUBMITTED")
    print("Job submitted successfully.\n")

def round_robin():
    jobs = load_jobs()
    if not jobs:
        print("\nNo jobs to process.\n")
        return

    print("\nProcessing using Round Robin...\n")

    while jobs:
        for job in jobs[:]:
            print(f"Running {job['job_name']} for {TIME_QUANTUM} seconds...")

            job['execution_time'] -= TIME_QUANTUM

            log_event(job['student_id'], job['job_name'], "ROUND ROBIN")

            if job['execution_time'] <= 0:
                print(f"Job {job['job_name']} completed.\n")
                save_completed_job(job)
                jobs.remove(job)

        save_jobs(jobs)

    print("All jobs processed.\n")


def priority_scheduling():
    jobs = load_jobs()
    if not jobs:
        print("\nNo jobs to process.\n")
        return

    print("\nProcessing using Priority Scheduling...\n")

    jobs.sort(key=lambda x: x['priority'], reverse=True)

    for job in jobs:
        print(f"Running {job['job_name']} (Priority {job['priority']})...")

        log_event(job['student_id'], job['job_name'], "PRIORITY")
        save_completed_job(job)

    save_jobs([])
    print("All jobs processed.\n")

def main():
    while True:
        print("===== HPC Job Scheduler =====")
        print("1. View Pending Jobs")
        print("2. Submit Job")
        print("3. Process Jobs (Round Robin)")
        print("4. Process Jobs (Priority)")
        print("5. View Completed Jobs")
        print("6. Exit")

        choice = input("Select an option: ")

        if choice == "1":
            view_pending_jobs()
        elif choice == "2":
            submit_job()
        elif choice == "3":
            round_robin()
        elif choice == "4":
            priority_scheduling()
        elif choice == "5":
            view_completed_jobs()
        elif choice == "6":
            confirm = input("Are you sure you want to exit? (y/n): ")
            if confirm.lower() == "y":
                print("Exiting system.")
                break
        else:
            print("Invalid choice. Try again.\n")


if __name__ == "__main__":
    main()
