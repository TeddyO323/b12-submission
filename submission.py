import os
import json
import hmac
import hashlib
import requests
from datetime import datetime, timezone

# B12 endpoint and signing secret
URL = "https://b12.io/apply/submission"
SECRET = b"hello-there-from-b12"

# Dynamically get repository and run ID from GitHub Actions environment
repo = os.environ.get("GITHUB_REPOSITORY")
run_id = os.environ.get("GITHUB_RUN_ID")

# Build the action run link for the current CI run
action_run_link = f"https://github.com/{repo}/actions/runs/{run_id}"

# Build payload
payload = {
    "timestamp": datetime.now(timezone.utc)
        .isoformat(timespec="milliseconds")
        .replace("+00:00", "Z"),
    "name": "Teddy Omondi",
    "email": "omosh60@gmail.com",
    "resume_link": "https://drive.google.com/file/d/11gctOomUvRH1tR7MO8CBppawGKWinYOD/view?usp=sharing",
    "repository_link": f"https://github.com/{repo}",
    "action_run_link": action_run_link
}

# Convert payload to canonical JSON (sorted keys, no whitespace)
body = json.dumps(payload, separators=(",", ":"), sort_keys=True).encode("utf-8")

# Compute HMAC-SHA256 signature
signature = hmac.new(SECRET, body, hashlib.sha256).hexdigest()

# Set headers
headers = {
    "Content-Type": "application/json",
    "X-Signature-256": f"sha256={signature}",
}

# POST the payload
response = requests.post(URL, data=body, headers=headers)

# Debug if failed
if response.status_code != 200:
    print("Status:", response.status_code)
    print("Response:", response.text)
    raise SystemExit(1)

# Print the receipt (success)
print(response.json()["receipt"])
