import json
import hmac
import hashlib
import requests
from datetime import datetime, timezone

URL = "https://b12.io/apply/submission"
SECRET = b"hello-there-from-b12"

payload = {
    "timestamp": datetime.now(timezone.utc)
        .isoformat(timespec="milliseconds")
        .replace("+00:00", "Z"),
    "name": "Your name",
    "email": "you@example.com",
    "resume_link": "https://pdf-or-html-or-linkedin.example.com",
    "repository_link": "https://github.com/yourusername/b12-submission",
    "action_run_link": "https://github.com/yourusername/b12-submission/actions/runs/RUN_ID"
}

body = json.dumps(
    payload,
    separators=(",", ":"),
    sort_keys=True
).encode("utf-8")

signature = hmac.new(
    SECRET,
    body,
    hashlib.sha256
).hexdigest()

headers = {
    "Content-Type": "application/json",
    "X-Signature-256": f"sha256={signature}",
}

response = requests.post(URL, data=body, headers=headers)
response.raise_for_status()

print(response.json()["receipt"])
