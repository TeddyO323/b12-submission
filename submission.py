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
    "name": "Teddy Omondi",
    "email": "you@example.com",
    "resume_link": "https://drive.google.com/file/d/11gctOomUvRH1tR7MO8CBppawGKWinYOD/view?usp=sharing",
    "repository_link": "https://github.com/TeddyO323/b12-submission/actions/runs/21640200847a"
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
if response.status_code != 200:
    print("Status:", response.status_code)
    print("Response:", response.text)
    raise SystemExit(1)


print(response.json()["receipt"])
