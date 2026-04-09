import os
import datetime
import tarfile
import time

def get_timestamp():
    return datetime.now().strftime("%d/%m/%Y %H:%M")


def log(message):
    os.makedirs("logs", exist_ok=True)
    with open("./logs/backup_service.log", "a") as f:
        f.write(f"[{get_timestamp()}] {message}\n")
        
        
def perform_backup(path, backup_name):
    try:
        os.makedirs("backups", exist_ok=True)

        tar_path = f"./backups/{backup_name}.tar"

        with tarfile.open(tar_path, "w") as tar:
            tar.add(path, arcname=os.path.basename(path))

        log(f"Backup done for {path} in backups/{backup_name}.tar")

    except Exception:
        log(f"Error: failed backup for {path}")


def run_service():
    schedules_path = "./backup_schedules.txt"

    while True:
        try:
            if not os.path.exists(schedules_path):
                time.sleep(45)
                continue

            with open(schedules_path, "r") as f:
                lines = f.readlines()

            if not lines:
                time.sleep(45)
                continue

            now = datetime.now().strftime("%H:%M")

            remaining = []

            for line in lines:
                line = line.strip()

                try:
                    path, schedule_time, backup_name = line.split(";")
                except ValueError:
                    continue

                if schedule_time == now:
                    perform_backup(path, backup_name)
                else:
                    remaining.append(line + "\n")

            with open(schedules_path, "w") as f:
                f.writelines(remaining)

        except Exception:
            log("Error: service loop failure")

        time.sleep(45)
        
        
if __name__ == "__main__":
    run_service()