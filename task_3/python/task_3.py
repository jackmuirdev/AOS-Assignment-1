#!/usr/bin/env python3

import os
import hashlib
import shutil
from datetime import datetime

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
LOG_FILE = os.path.join(SCRIPT_DIR, "submission_log.txt")
RECORD_FILE = os.path.join(SCRIPT_DIR, "submission_records.txt")
SUBMISSION_DIR = os.path.join(SCRIPT_DIR, "submissions")
MAX_SIZE = 5 * 1000 * 1000  # 5 MB
PASSWORD = "password123"
LOCK_THRESHOLD = 3


def init():
    os.makedirs(SUBMISSION_DIR, exist_ok=True)
    for f in (LOG_FILE, RECORD_FILE):
        if not os.path.exists(f):
            open(f, "w").close()


def log_event(student_id, filename, event_type, status):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(LOG_FILE, "a") as log:
        log.write(f"{timestamp} | {student_id} | {filename} | {event_type} | {status}\n")


def hash_file(filepath):
    sha256 = hashlib.sha256()
    with open(filepath, "rb") as f:
        while chunk := f.read(4096):
            sha256.update(chunk)
    return sha256.hexdigest()


def submit(student_id, filepath):
    if not os.path.exists(filepath):
        print("File does not exist.")
        return

    filename = os.path.basename(filepath)

    if not filename.endswith((".pdf", ".docx")):
        print("Invalid file format.")
        log_event(student_id, filename, "SUBMISSION", "INVALID_FORMAT")
        return

    if os.path.getsize(filepath) >= MAX_SIZE:
        print("File exceeds 5MB limit.")
        log_event(student_id, filename, "SUBMISSION", "FILE_TOO_LARGE")
        return

    file_hash = hash_file(filepath)

    if os.path.exists(RECORD_FILE):
        with open(RECORD_FILE, "r") as f:
            for line in f:
                parts = line.strip().split("|")
                if len(parts) >= 3:
                    existing_hash = parts[2].strip()
                    if existing_hash == file_hash:
                        print("Duplicate submission detected (same content).")
                        log_event(student_id, filename, "SUBMISSION", "DUPLICATE_CONTENT")
                        return

    shutil.copy2(filepath, SUBMISSION_DIR)
    with open(RECORD_FILE, "a") as f:
        f.write(f"{student_id} | {filename} | {file_hash}\n")

    print("Submission successful.")
    log_event(student_id, filename, "SUBMISSION", "SUCCESS")


def check_duplicate(filepath):
    if not os.path.exists(RECORD_FILE):
        print("No submissions yet.")
        return

    filename = os.path.basename(filepath)
    file_hash = hash_file(filepath)

    with open(RECORD_FILE, "r") as f:
        for line in f:
            parts = line.strip().split("|")
            if len(parts) >= 3:
                existing_name = parts[1].strip()
                existing_hash = parts[2].strip()
                if existing_hash == file_hash and existing_name == filename:
                    print(f"Duplicate content detected! File '{filename}' matches an existing submission.")
                    return

    print("No duplicate found.")


def count_recent_failed_attempts(student_id):
    if not os.path.exists(LOG_FILE):
        return 0

    count = 0
    with open(LOG_FILE, "r") as f:
        for line in f:
            if f"| {student_id} | LOGIN | LOGIN | FAILED" in line:
                count += 1
            elif f"| {student_id} | LOGIN | LOGIN | SUCCESS" in line:
                count = 0
    return count


def detect_suspicious_activity(student_id, window_seconds=60):
    if not os.path.exists(LOG_FILE):
        return False

    now = datetime.now()
    timestamps = []

    with open(LOG_FILE, "r") as f:
        for line in f:
            if f"| {student_id} | LOGIN | LOGIN | FAILED" in line or f"| {student_id} | LOGIN | LOGIN | SUCCESS" in line:
                timestamp_str = line.split("|")[0].strip()
                timestamp = datetime.strptime(timestamp_str, "%Y-%m-%d %H:%M:%S")
                timestamps.append(timestamp)

    recent_attempts = [t for t in timestamps if (now - t).total_seconds() <= window_seconds]
    return len(recent_attempts) > 1


def login(student_id, password):
    student_id = str(student_id)
    failed_count = count_recent_failed_attempts(student_id)

    if failed_count >= LOCK_THRESHOLD:
        print("Account is locked due to multiple failed login attempts.")
        log_event(student_id, "LOGIN", "LOGIN", "LOCKED")
        return

    if detect_suspicious_activity(student_id, window_seconds=60):
        print("Suspicious login activity detected (multiple attempts within 60 seconds).")
        log_event(student_id, "LOGIN", "LOGIN", "SUSPICIOUS")

    if password != PASSWORD:
        print("Login failed.")
        log_event(student_id, "LOGIN", "LOGIN", "FAILED")
    else:
        print("Login successful.")
        log_event(student_id, "LOGIN", "LOGIN", "SUCCESS")


def list_submissions():
    print("===== Submitted Assignments =====")
    if os.path.exists(RECORD_FILE) and os.path.getsize(RECORD_FILE) > 0:
        with open(RECORD_FILE, "r") as f:
            print(f.read(), end="")
    else:
        print("No submissions yet.")


def main():
    init()
    while True:
        print("===== Secure Examination System =====")
        print("1) Submit Assignment")
        print("2) Check Duplicate Submission")
        print("3) List Submitted Assignments")
        print("4) Simulate Login Attempt")
        print("5) Exit")
        choice = input("Select option: ").strip()

        if choice == "1":
            student_id = input("Enter Student ID: ").strip()
            file_path = input("Enter file path: ").strip()
            submit(student_id, file_path)
        elif choice == "2":
            file_path = input("Enter file path to check: ").strip()
            check_duplicate(file_path)
        elif choice == "3":
            list_submissions()
        elif choice == "4":
            student_id = input("Enter Student ID: ").strip()
            password = input("Enter Password: ").strip()
            login(student_id, password)
        elif choice == "5":
            confirm = input("Are you sure you want to exit? (Y/N): ").strip()
            if confirm.lower() == "y":
                log_event("SYSTEM", "EXIT", "EXIT", "SUCCESS")
                print("Exiting system.")
                break
        else:
            print("Invalid option.")

        print()


if __name__ == "__main__":
    main()
