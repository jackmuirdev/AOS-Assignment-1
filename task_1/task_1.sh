#!/bin/bash

LOG_FILE="system_monitor_log.txt"
ARCHIVE_DIR="ArchiveLogs"

touch "$LOG_FILE"

log_action() {
    echo "$(date '+%Y-%m-%d %H:%M:%S') - $1" >> "$LOG_FILE"
}

display_usage() {
    echo "========== SYSTEM RESOURCE USAGE =========="

    CPU_USAGE=$(top -bn1 | grep "Cpu(s)" | awk '{print 100 - $8}')
    MEM_TOTAL=$(free -m | awk '/Mem:/ {print $2}')
    MEM_USED=$(free -m | awk '/Mem:/ {print $3}')
    MEM_PERCENT=$(awk "BEGIN {printf \"%.2f\", ($MEM_USED/$MEM_TOTAL)*100}")

    echo "CPU Usage: $CPU_USAGE %"
    echo "Memory Usage: $MEM_USED MB / $MEM_TOTAL MB ($MEM_PERCENT%)"
    echo "==========================================="

    log_action "Viewed system resource usage"
}

list_top_processes() {
    echo "========== TOP 10 MEMORY PROCESSES =========="
    printf "%-8s %-15s %-8s %-8s %-20s\n" "PID" "USER" "CPU%" "MEM%" "COMMAND"
    ps -eo pid,user,%cpu,%mem,comm --sort=-%mem | head -11
    echo "============================================="

    log_action "Viewed top 10 memory consuming processes"
}

terminate_process() {
    read -p "Enter PID to terminate: " PID

    if [[ ! $PID =~ ^[0-9]+$ ]]; then
        echo "Invalid PID."
        return
    fi

    if [ "$PID" -eq 1 ]; then
        echo "Cannot terminate system init process (PID 1)."
        log_action "Attempted to terminate PID 1"
        return
    fi

    PROCESS_INFO=$(ps -p $PID -o user=,comm=)

    if [ -z "$PROCESS_INFO" ]; then
        echo "Process does not exist."
        return
    fi

    USER=$(echo $PROCESS_INFO | awk '{print $1}')
    COMMAND=$(echo $PROCESS_INFO | awk '{print $2}')

    if [ "$USER" == "root" ]; then
        echo "Cannot terminate root-owned system process ($COMMAND)."
        log_action "Attempted to terminate root process PID $PID"
        return
    fi

    read -p "Are you sure you want to terminate $COMMAND (PID $PID)? (Y/N): " CONFIRM
    if [[ $CONFIRM =~ ^[Yy]$ ]]; then
        kill -9 $PID
        echo "Process terminated."
        log_action "Terminated process PID $PID ($COMMAND)"
    else
        echo "Termination cancelled."
    fi
}

inspect_disk() {
    read -p "Enter directory path to inspect: " DIR

    if [ -d "$DIR" ]; then
        echo "Disk usage for $DIR:"
        du -sh "$DIR"
        log_action "Inspected disk usage for $DIR"
    else
        echo "Directory does not exist."
    fi
}

archive_logs() {
    read -p "Enter directory to scan for .log files: " LOG_DIR

    if [ ! -d "$LOG_DIR" ]; then
        echo "Directory does not exist."
        return
    fi

    mkdir -p "$ARCHIVE_DIR"

    FOUND=0

    for FILE in "$LOG_DIR"/*.log; do
        if [ -f "$FILE" ]; then
            SIZE_MB=$(du -m "$FILE" | cut -f1)

            if [ "$SIZE_MB" -gt 50 ]; then
                FOUND=1
                TIMESTAMP=$(date '+%Y%m%d_%H%M%S')
                BASENAME=$(basename "$FILE")
                ARCHIVE_FILE="$ARCHIVE_DIR/${BASENAME}_${TIMESTAMP}.gz"

                gzip -c "$FILE" > "$ARCHIVE_FILE"

                echo "Archived: $FILE -> $ARCHIVE_FILE"
                log_action "Archived $FILE to $ARCHIVE_FILE"
            fi
        fi
    done

    if [ "$FOUND" -eq 0 ]; then
        echo "No log files larger than 50MB found."
    fi

    SIZE=$(du -sm "$ARCHIVE_DIR" | cut -f1)
    if [ "$SIZE" -gt 1024 ]; then
        echo "WARNING: ArchiveLogs exceeds 1GB!"
        log_action "ArchiveLogs exceeded 1GB"
    fi
}

exit_script() {
    read -p "Are you sure you want to exit? (Y/N): " CONFIRM

    if [[ $CONFIRM =~ ^[Yy]$ ]]; then
        log_action "Exited system administration tool"
        echo "Bye"
        exit 0
    fi
}

while true; do
    echo ""
    echo "=========== UNIVERSITY DATA CENTRE TOOL ==========="
    echo "1) Display CPU and Memory Usage"
    echo "2) List Top 10 Memory Consuming Processes"
    echo "3) Terminate a Process"
    echo "4) Inspect Disk Usage"
    echo "5) Archive Large Log Files"
    echo "6) Bye (Exit)"
    echo "==================================================="
    read -p "Choose an option [1-6]: " OPTION

    case $OPTION in
        1) display_usage ;;
        2) list_top_processes ;;
        3) terminate_process ;;
        4) inspect_disk ;;
        5) archive_logs ;;
        6) exit_script ;;
        *) echo "Invalid option. Please choose 1-6." ;;
    esac
done
