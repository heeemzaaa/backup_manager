import os
import datetime
import tarfile

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


if __name__ == "__main__":
    run_service()