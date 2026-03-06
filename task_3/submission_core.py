import sys
import os
import hashlib
from datetime import datetime

LOG_FILE = "submission_log.txt"
RECORD_FILE = "submission_records.txt"
SUBMISSION_DIR = "submissions"
MAX_SIZE = 5 * 1000 * 1000 # 5 mb
PASSWORD = "password123"
LOCK_THRESHOLD = 3

failed_attempts = {}
locked_accounts = {}
login_timestamps = {}

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

    os.system(f"cp '{filepath}' '{SUBMISSION_DIR}/'")
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

if __name__ == "__main__":
    action = sys.argv[1]

    if action == "submit":
        submit(sys.argv[2], sys.argv[3])
    elif action == "check":
        check_duplicate(sys.argv[2])
    elif action == "login":
        login(sys.argv[2], sys.argv[3])