# detection/engine.py
import time
import json
import os
from detection.rules import check_rules

DEBOUNCE_SECONDS = 10
_last_alert_ts = {}

LOG_PATH = os.path.join("logs", "alerts.log")
os.makedirs("logs", exist_ok=True)

def emit_alert(flow_feat, reason):
    now = time.time()
    src = flow_feat.get("src", "unknown")
    last = _last_alert_ts.get(src, 0)
    if now - last < DEBOUNCE_SECONDS:
        return
    alert = {"time": now, "type": reason, "flow": flow_feat}
    print("[ALERT]", reason, flow_feat)
    try:
        with open(LOG_PATH, "a") as f:
            f.write(json.dumps(alert) + "\n")
    except Exception as e:
        print("[ERROR] Writing alert failed:", e)
    _last_alert_ts[src] = now

def evaluate_flow(flow_feat):
    reason = check_rules(flow_feat)
    if reason:
        emit_alert(flow_feat, reason)

