#!/bin/bash

LOG_FILE="submission_log.txt"
RECORD_FILE="submission_records.txt"
SUBMISSION_DIR="submissions"

mkdir -p "$SUBMISSION_DIR"
touch "$LOG_FILE"
touch "$RECORD_FILE"

while true
do
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
            python3 submission_core.py submit "$student_id" "$file_path"
            ;;

        2)
            read -p "Enter file path to check: " file_path
            python3 submission_core.py check "$file_path"
            ;;

        3)
            echo "===== Submitted Assignments ====="
            cat "$RECORD_FILE"
            ;;

        4)
            read -p "Enter Student ID: " student_id
            read -p "Enter Password: " password
            python3 submission_core.py login "$student_id" "$password"
            ;;

        5)
            read -p "Are you sure you want to exit? (Y/N): " confirm
            if [[ "$confirm" == "Y" || "$confirm" == "y" ]]; then
                echo "$(date) | SYSTEM | EXIT | SUCCESS" >> "$LOG_FILE"
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