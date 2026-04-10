import re
from datetime import datetime
import os
import sys
import subprocess
import signal



def get_timestamp():
    return datetime.now().strftime("%d/%m/%Y %H:%M")


def log(message):
    os.makedirs("logs", exist_ok=True)
    with open("./logs/backup_manager.log", "a") as f:
        f.write(f"[{get_timestamp()}] {message}\n")

def get_pid():
    result = subprocess.run(
        ["ps", "-A", "-f"],
        capture_output=True,
        text=True
    )
    for line in result.stdout.splitlines():
        if "backup_service.py" in line:
            pid = int(line.split()[1])  # PID is the 2nd column in ps -f
            return pid
    return None



def create(schedule_text):
    schedules_path = "./backup_schedules.txt"

    pattern = r"^([^;]+);(\d{2}:\d{2});([^;]+)$"

    if not re.match(pattern, schedule_text):
        log(f"Error: malformed schedule: {schedule_text}")
        return

    try:
        with open(schedules_path, "a") as f:
            f.write(schedule_text + "\n")
        log(f"New schedule added: {schedule_text}")
    except Exception:
        log(f"Error: can't write schedule")


def list_schedules():
    schedules_path = "./backup_schedules.txt"

    try:
        with open(schedules_path, "r") as f:
            lines = f.readlines()

        log("Show schedules list")

        for i, line in enumerate(lines):
            print(f"{i}: {line.strip()}")

    except FileNotFoundError:
        log("Error: can't find backup_schedules.txt")


def delete_schedule(index):
    schedules_path = "./backup_schedules.txt"

    try:
        with open(schedules_path, "r") as f:
            lines = f.readlines()

        if index < 0 or index >= len(lines):
            log(f"Error: can't find schedule at index {index}")
            return

        lines.pop(index)

        with open(schedules_path, "w") as f:
            f.writelines(lines)

        log(f"Schedule at index {index} deleted")

    except FileNotFoundError:
        log("Error: can't find backup_schedules.txt")


def start():
        pid = get_pid()
        if pid == None:
            try:
                proc = subprocess.Popen(["python3", "backup_service.py"])
                log("backup_service started")
            except FileNotFoundError:
                log("Error: backup_service already running")
        else:
            log("Error: backup_service already running")

    



def stop():
    pid = get_pid()
    if pid != None:
        try:
            os.kill(pid, signal.SIGTERM)
            log("backup_service stopped")
        except Exception:
            log("Error: can't stop backup_service")
    else:
        log("Error: can't stop backup_service")
    

def list_backups():
    backups_path = "./backups"

    try:
        files = os.listdir(backups_path)

        log("Show backups list")

        for f in files:
            print(f)

    except FileNotFoundError:
        log("Error: can't find backups directory")
        
        
def main():
    args = sys.argv

    if len(args) < 2:
        log("Error: no command provided")
        return

    command = args[1]

    try:
        if command == "create":
            if len(args) != 3:
                log("Error: invalid create usage")
            else:
                create(args[2])

        elif command == "list":
            list_schedules()

        elif command == "delete":
            if len(args) != 3:
                log("Error: invalid delete usage")
            else:
                delete_schedule(int(args[2]))

        elif command == "start":
            start()

        elif command == "stop":
            stop()

        elif command == "backups":
            list_backups()

        else:
            log(f"Error: unknown command: {command}")

    except Exception:
        log("Error: unexpected failure")


if __name__ == "__main__":
    main()