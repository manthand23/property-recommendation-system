from pathlib import Path
from datetime import datetime
from collections import defaultdict

LOG_FILE = Path("retrain_log.txt")

if not LOG_FILE.exists():
    print("No retrain log found.")
    exit()

print("Retrain Log Summary (Grouped by Session)\n------------------------------------------")

sessions = defaultdict(list)
current_session = None

with LOG_FILE.open("r") as log:
    for line in log:
        timestamp_raw, message = line.strip().split("] ", 1)
        timestamp = timestamp_raw.strip("[")

        try:
            dt = datetime.fromisoformat(timestamp)
        except ValueError:
            continue

        if message.startswith("Retrained and saved"):
            current_session = dt
            sessions[current_session].append((dt, message))
        elif current_session:
            sessions[current_session].append((dt, message))

# Print grouped sessions
for session_time in sorted(sessions.keys()):
    print(f"\n📦 Session: {session_time.strftime('%Y-%m-%d %H:%M:%S')}")
    for dt, msg in sessions[session_time]:
        print(f"  • {msg}")
