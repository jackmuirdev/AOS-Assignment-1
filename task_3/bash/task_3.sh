#!/bin/bash

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LOG_FILE="$SCRIPT_DIR/submission_log.txt"
RECORD_FILE="$SCRIPT_DIR/submission_records.txt"
SUBMISSION_DIR="$SCRIPT_DIR/submissions"
MAX_SIZE=5000000  # 5 MB
PASSWORD="password123"
LOCK_THRESHOLD=3

mkdir -p "$SUBMISSION_DIR"
touch "$LOG_FILE"
touch "$RECORD_FILE"

log_event() {
    local student_id="$1"
    local filename="$2"
    local event_type="$3"
    local status="$4"
    local timestamp
    timestamp=$(date "+%Y-%m-%d %H:%M:%S")
    echo "$timestamp | $student_id | $filename | $event_type | $status" >> "$LOG_FILE"
}

hash_file() {
    local filepath="$1"
    if command -v shasum &>/dev/null; then
        shasum -a 256 "$filepath" | awk '{print $1}'
    else
        sha256sum "$filepath" | awk '{print $1}'
    fi
}

get_file_size() {
    local filepath="$1"
    if [[ "$(uname)" == "Darwin" ]]; then
        stat -f%z "$filepath"
    else
        stat -c%s "$filepath"
    fi
}

submit() {
    local student_id="$1"
    local filepath="$2"

    if [[ ! -f "$filepath" ]]; then
        echo "File does not exist."
        return
    fi

    local filename
    filename=$(basename "$filepath")

    if [[ "$filename" != *.pdf && "$filename" != *.docx ]]; then
        echo "Invalid file format."
        log_event "$student_id" "$filename" "SUBMISSION" "INVALID_FORMAT"
        return
    fi

    local size
    size=$(get_file_size "$filepath")
    if [[ "$size" -ge "$MAX_SIZE" ]]; then
        echo "File exceeds 5MB limit."
        log_event "$student_id" "$filename" "SUBMISSION" "FILE_TOO_LARGE"
        return
    fi

    local file_hash
    file_hash=$(hash_file "$filepath")

    if [[ -f "$RECORD_FILE" ]]; then
        while IFS= read -r line; do
            local existing_hash
            existing_hash=$(echo "$line" | awk -F'|' '{print $3}' | tr -d ' ')
            if [[ "$existing_hash" == "$file_hash" ]]; then
                echo "Duplicate submission detected (same content)."
                log_event "$student_id" "$filename" "SUBMISSION" "DUPLICATE_CONTENT"
                return
            fi
        done < "$RECORD_FILE"
    fi

    cp "$filepath" "$SUBMISSION_DIR/"
    echo "$student_id | $filename | $file_hash" >> "$RECORD_FILE"
    echo "Submission successful."
    log_event "$student_id" "$filename" "SUBMISSION" "SUCCESS"
}

check_duplicate() {
    local filepath="$1"

    if [[ ! -f "$RECORD_FILE" ]] || [[ ! -s "$RECORD_FILE" ]]; then
        echo "No submissions yet."
        return
    fi

    local filename
    filename=$(basename "$filepath")

    local file_hash
    file_hash=$(hash_file "$filepath")

    while IFS= read -r line; do
        local existing_name existing_hash
        existing_name=$(echo "$line" | awk -F'|' '{print $2}' | tr -d ' ')
        existing_hash=$(echo "$line" | awk -F'|' '{print $3}' | tr -d ' ')
        if [[ "$existing_hash" == "$file_hash" && "$existing_name" == "$filename" ]]; then
            echo "Duplicate content detected! File '$filename' matches an existing submission."
            return
        fi
    done < "$RECORD_FILE"

    echo "No duplicate found."
}

count_recent_failed_attempts() {
    local student_id="$1"
    local count=0

    if [[ ! -f "$LOG_FILE" ]]; then
        echo 0
        return
    fi

    while IFS= read -r line; do
        if [[ "$line" == *"| $student_id | LOGIN | LOGIN | FAILED"* ]]; then
            ((count++))
        elif [[ "$line" == *"| $student_id | LOGIN | LOGIN | SUCCESS"* ]]; then
            count=0
        fi
    done < "$LOG_FILE"

    echo $count
}

to_epoch() {
    local ts="$1"
    if [[ "$(uname)" == "Darwin" ]]; then
        date -j -f "%Y-%m-%d %H:%M:%S" "$ts" +%s 2>/dev/null
    else
        date -d "$ts" +%s 2>/dev/null
    fi
}

detect_suspicious_activity() {
    local student_id="$1"
    local window_seconds=60

    if [[ ! -f "$LOG_FILE" ]]; then
        echo "false"
        return
    fi

    local now
    now=$(date +%s)
    local count=0

    while IFS= read -r line; do
        if [[ "$line" == *"| $student_id | LOGIN | LOGIN | FAILED"* || "$line" == *"| $student_id | LOGIN | LOGIN | SUCCESS"* ]]; then
            local ts_str ts_epoch diff
            ts_str=$(echo "$line" | cut -d'|' -f1 | tr -d ' ')
            ts_epoch=$(to_epoch "$ts_str")
            if [[ -n "$ts_epoch" ]]; then
                diff=$(( now - ts_epoch ))
                if [[ "$diff" -le "$window_seconds" ]]; then
                    ((count++))
                fi
            fi
        fi
    done < "$LOG_FILE"

    if [[ "$count" -gt 1 ]]; then
        echo "true"
    else
        echo "false"
    fi
}

login() {
    local student_id="$1"
    local password="$2"

    local failed_count
    failed_count=$(count_recent_failed_attempts "$student_id")

    if [[ "$failed_count" -ge "$LOCK_THRESHOLD" ]]; then
        echo "Account is locked due to multiple failed login attempts."
        log_event "$student_id" "LOGIN" "LOGIN" "LOCKED"
        return
    fi

    local suspicious
    suspicious=$(detect_suspicious_activity "$student_id")
    if [[ "$suspicious" == "true" ]]; then
        echo "Suspicious login activity detected (multiple attempts within 60 seconds)."
        log_event "$student_id" "LOGIN" "LOGIN" "SUSPICIOUS"
    fi

    if [[ "$password" != "$PASSWORD" ]]; then
        echo "Login failed."
        log_event "$student_id" "LOGIN" "LOGIN" "FAILED"
    else
        echo "Login successful."
        log_event "$student_id" "LOGIN" "LOGIN" "SUCCESS"
    fi
}

# Main menu loop
while true; do
    echo "===== Secure Examination System ====="
    echo "1) Submit Assignment"
    echo "2) Check Duplicate Submission"
    echo "3) List Submitted Assignments"
    echo "4) Simulate Login Attempt"
    echo "5) Exit"
    read -p "Select option: " choice

    case $choice in
        1)
            read -p "Enter Student ID: " student_id
            read -p "Enter file path: " file_path
            submit "$student_id" "$file_path"
            ;;
        2)
            read -p "Enter file path to check: " file_path
            check_duplicate "$file_path"
            ;;
        3)
            echo "===== Submitted Assignments ====="
            cat "$RECORD_FILE"
            ;;
        4)
            read -p "Enter Student ID: " student_id
            read -p "Enter Password: " password
            login "$student_id" "$password"
            ;;
        5)
            read -p "Are you sure you want to exit? (Y/N): " confirm
            if [[ "$confirm" == "Y" || "$confirm" == "y" ]]; then
                echo "$(date "+%Y-%m-%d %H:%M:%S") | SYSTEM | EXIT | EXIT | SUCCESS" >> "$LOG_FILE"
                echo "Exiting system."
                exit 0
            fi
            ;;
        *)
            echo "Invalid option."
            ;;
    esac

    echo ""
done
