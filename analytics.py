# Placeholder for utils/analytics.py
import json
import threading

LOCK = threading.Lock()
ANALYTICS_FILE = "utils/analytics.json"

def load_analytics():
    try:
        with open(ANALYTICS_FILE, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

def save_analytics(data):
    with LOCK:
        with open(ANALYTICS_FILE, "w") as f:
            json.dump(data, f, indent=2)

def record_click(job_title):
    data = load_analytics()
    data[job_title] = data.get(job_title, 0) + 1
    save_analytics(data)
