import os
import datetime

def get_timestamp():
    return datetime.now().strftime("%d/%m/%Y %H:%M")


def log(message):
    os.makedirs("logs", exist_ok=True)
    with open("./logs/backup_service.log", "a") as f:
        f.write(f"[{get_timestamp()}] {message}\n")
        
        
def perform_backup(path, backup_name):


def run_service():


if __name__ == "__main__":
    run_service()