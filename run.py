import os
import subprocess
import sys
from dotenv import load_dotenv

load_dotenv()

token = os.getenv("HIGHRISE_BOT_TOKEN", "").strip()
room_id = os.getenv("HIGHRISE_ROOM_ID", "").strip()

if not token or token == "YOUR_BOT_API_TOKEN_HERE":
    print("[ERROR] Please put your actual HIGHRISE_BOT_TOKEN in the .env file!")
    exit(1)

if not room_id or room_id == "YOUR_ROOM_ID_HERE":
    print("[ERROR] Please put your actual HIGHRISE_ROOM_ID in the .env file!")
    exit(1)

print(f"[INFO] Starting Highrise Bot for room {room_id}...")
subprocess.run([sys.executable, "-m", "highrise", "bot:UltimateBot", room_id, token], check=True)
