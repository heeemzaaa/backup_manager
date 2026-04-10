# Backup Manager

A Python-based automated backup system that schedules and performs compressed backups from the command line. The system runs a background service that monitors schedules and archives directories into `.tar` files, with full logging and error handling.

---

## Project Structure

```
backup-manager/
├── backup_manager.py        # CLI script for managing schedules and the service
├── backup_service.py        # Background service that performs scheduled backups
├── backup_schedules.txt     # Schedule file (created at runtime)
├── logs/
│   ├── backup_manager.log   # Logs from backup_manager.py
│   └── backup_service.log   # Logs from backup_service.py
└── backups/                 # Directory where .tar backup files are saved
```

---

## Requirements

- Python 3.x
- Unix-like OS (Linux / macOS)
- No external dependencies — only Python standard library modules are used

---

## Usage

### Create a backup schedule

```bash
python3 backup_manager.py create "path_to_save;HH:MM;backup_name"
```

Example:
```bash
python3 backup_manager.py create "~/documents;14:30;my_docs"
```

The schedule format is strictly `path_to_save;HH:MM;backup_name`. Malformed schedules are rejected and logged.

---

### List all schedules

```bash
python3 backup_manager.py list
```

Prints each schedule with its index:
```
0: ~/documents;14:30;my_docs
1: ~/pictures;16:00;photos
```

---

### Delete a schedule

```bash
python3 backup_manager.py delete [index]
```

Example:
```bash
python3 backup_manager.py delete 0
```

---

### Start the backup service

```bash
python3 backup_manager.py start
```

Launches `backup_service.py` as a background process. The service runs in an infinite loop, checking schedules every ~45 seconds and performing backups when the current time matches a scheduled entry.

---

### Stop the backup service

```bash
python3 backup_manager.py stop
```

Finds and kills the running `backup_service.py` process.

---

### List existing backups

```bash
python3 backup_manager.py backups
```

Prints all `.tar` files currently saved in the `./backups` directory.

---

## How It Works

1. Schedules are stored line by line in `backup_schedules.txt` using the format `path;HH:MM;name`.
2. When `start` is called, `backup_service.py` is launched in the background using `subprocess.Popen` with `start_new_session=True`.
3. Every ~45 seconds, the service reads the schedules and compares them to the current time.
4. When a match is found, the target directory is compressed into a `.tar` file and saved under `./backups/`.
5. Processed schedules are removed from `backup_schedules.txt`.
6. All actions and errors are timestamped and written to the appropriate log file.

---

## Logging

All log entries follow the format:
```
[dd/mm/yyyy hh:mm] message
```

| Script                | Log file                      |
|-----------------------|-------------------------------|
| `backup_manager.py`   | `./logs/backup_manager.log`   |
| `backup_service.py`   | `./logs/backup_service.log`   |

Example log output:
```
[10/04/2026 16:07] New schedule added: test;16:07;backup_test
[10/04/2026 16:07] backup_service started
[10/04/2026 16:07] backup_service stopped
```

---

## Example Session

```bash
python3 backup_manager.py create "test;16:07;backup_test"
python3 backup_manager.py create "test1;16:07;personal_data"
python3 backup_manager.py create "test2;16:07;office_docs"
python3 backup_manager.py list
python3 backup_manager.py start
# wait for the service to process the schedules...
python3 backup_manager.py stop
python3 backup_manager.py backups
```

Expected output:
```
0: test;16:07;backup_test
1: test1;16:07;personal_data
2: test2;16:07;office_docs

backup_test.tar
personal_data.tar
office_docs.tar
```

---

## Authors
 
Built by a two-person team as part of a DevOps automation project.
 
- **Hamza Elkhawlani** — [heeemzaaa](https://github.com/heeemzaaa)
- **Hassan El Ouazizi** — [helouazizi](https://github.com/helouazizi)