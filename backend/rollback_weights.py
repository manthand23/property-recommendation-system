import os
from pathlib import Path
import shutil

BACKUP_DIR = Path("weights_backup")
CURRENT = Path("trained_weights.json")

# List available backups
backups = sorted(BACKUP_DIR.glob("weights_*.json"), reverse=True)

if not backups:
    print("No backups found.")
    exit()

print("📦 Available backups:")
for i, file in enumerate(backups):
    print(f"[{i}] {file.name}")

idx = input("Enter the number of the version to restore: ")

try:
    selected = backups[int(idx)]
except (IndexError, ValueError):
    print("Invalid selection.")
    exit()

# Copy backup to trained_weights.json
shutil.copyfile(selected, CURRENT)
print(f"Restored {selected.name} to {CURRENT.name}")
