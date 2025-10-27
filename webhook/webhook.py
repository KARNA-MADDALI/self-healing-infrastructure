#!/usr/bin/env python3
from flask import Flask, request, jsonify
import subprocess, datetime, os

app = Flask(__name__)

LOGFILE = "/app/heal.log"

def log(msg):
    ts = datetime.datetime.utcnow().isoformat()
    line = f"[{ts}] {msg}\n"
    print(line, end='')
    try:
        with open(LOGFILE, "a") as f:
            f.write(line)
    except Exception:
        pass

@app.route("/", methods=["GET"])
def home():
    return "Webhook Receiver Active\n", 200

@app.route("/alert", methods=["POST"])
def alert():
    payload = request.json
    log(f"Received alert: {payload}")

    # Only trigger playbook for critical alerts (simple filter example)
    alerts = payload if isinstance(payload, list) else payload.get("alerts", [])
    # For v2, Alertmanager sends a JSON array of alerts to /api/v2/webhook, but we configured webhook_configs->url to /alert
    # So payload is list-like
    try:
        # Run the ansible playbook (playbook should be mounted in /app/playbooks)
        proc = subprocess.run(["ansible-playbook", "/app/playbooks/restart_nginx.yml"],
                              capture_output=True, text=True, check=False)
        log(f"ansible-playbook returncode: {proc.returncode}")
        log("ansible stdout:\n" + proc.stdout)
        if proc.stderr:
            log("ansible stderr:\n" + proc.stderr)
    except Exception as e:
        log(f"Exception when running playbook: {e}")

    return jsonify({"status":"ok"}), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5001)))
