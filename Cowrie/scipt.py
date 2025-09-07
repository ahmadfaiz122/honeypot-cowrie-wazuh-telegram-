#!/usr/bin/env python3
import sys, json, requests

TOKEN = "YOUR_TELEGRAM_BOT_TOKEN"
CHAT_ID = "YOUR_CHAT_ID"
URL = f"https://api.telegram.org/bot{TOKEN}/sendMessage"

alert_file = sys.argv[1]
with open(alert_file) as f:
    alert = json.load(f)

message = (
    f"🚨 *Wazuh Alert* 🚨\n"
    f"Rule: {alert['rule']['description']}\n"
    f"Level: {alert['rule']['level']}\n"
    f"Agent: {alert['agent']['name']}\n"
    f"Time: {alert['timestamp']}\n"
    f"Src IP: {alert.get('srcip', 'N/A')}"
)

requests.post(URL, data={"chat_id": CHAT_ID, "text": message, "parse_mode": "Markdown"})
