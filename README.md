# Honeypot Cowrie → Wazuh → Telegram

Repository ini berisi contoh konfigurasi dan script untuk mengimplementasikan honeypot Cowrie yang terintegrasi dengan Wazuh (agent → manager) dan mengirimkan notifikasi ke Telegram untuk SOC.

## Tujuan
- Menangkap interaksi attacker melalui Cowrie.
- Mengirim log Cowrie ke Wazuh Agent, agar Wazuh Manager menganalisis dan menghasilkan alert.
- Mengirim alert ke Telegram (bot) untuk notifikasi cepat ke SOC.

## Arsitektur Alur

- **Attacker**: Pelaku mencoba brute force, scanning, atau exploit.  
- **Cowrie**: Honeypot SSH/Telnet untuk merekam interaksi attacker.  
- **Wazuh Agent**: Mengumpulkan log Cowrie dan meneruskannya ke Wazuh Manager.  
- **Wazuh Manager**: Melakukan analisis log dengan ruleset/decoder khusus Cowrie.  
- **Telegram Bot**: Mengirimkan notifikasi alert ke grup/akun SOC.  

---

## Prasyarat
1. **Server / VM Linux (Ubuntu/Debian/centOS)** dengan akses root.  
2. **Cowrie Honeypot** sudah terinstal (lihat dokumentasi resmi: https://github.com/cowrie/cowrie).  
3. **Wazuh Agent** sudah terinstal (https://documentation.wazuh.com).  
4. **Akun Telegram Bot** dengan `BOT_TOKEN` dan `CHAT_ID`.  

---

## Langkah Instalasi

### 1. Konfigurasi Wazuh Agent
Edit file /var/ossec/etc/ossec.conf di agent agar memonitor log Cowrie
`nano /var/ossec/etc/ossec.conf`
```
<integration>
        <name>custom-telegram</name>
        <level>3</level>
        <hook_url>https://api.telegram.org/bot*YOUR API KEY*/sendMessage</hook_url>
        <alert_format>json</alert_format>
    </integration>
```
`sudo systemctl restart wazuh-agent`

### 2. Tambahkan blok di wazuh
edit file
`nano /var/ossec/integrations/custom-telegram`

```
#!/bin/sh

WPYTHON_BIN="framework/python/bin/python3"

SCRIPT_PATH_NAME="$0"

DIR_NAME="$(cd $(dirname ${SCRIPT_PATH_NAME}); pwd -P)"
SCRIPT_NAME="$(basename ${SCRIPT_PATH_NAME})"

case ${DIR_NAME} in
    */active-response/bin | */wodles*)
        if [ -z "${WAZUH_PATH}" ]; then
            WAZUH_PATH="$(cd ${DIR_NAME}/../..; pwd)"
        fi

        PYTHON_SCRIPT="${DIR_NAME}/${SCRIPT_NAME}.py"
    ;;
    */bin)
        if [ -z "${WAZUH_PATH}" ]; then
            WAZUH_PATH="$(cd ${DIR_NAME}/..; pwd)"
        fi

        PYTHON_SCRIPT="${WAZUH_PATH}/framework/scripts/${SCRIPT_NAME}.py"
    ;;
     */integrations)
        if [ -z "${WAZUH_PATH}" ]; then
            WAZUH_PATH="$(cd ${DIR_NAME}/..; pwd)"
        fi

        PYTHON_SCRIPT="${DIR_NAME}/${SCRIPT_NAME}.py"
    ;;
esac


${WAZUH_PATH}/${WPYTHON_BIN} ${PYTHON_SCRIPT} "$@"
```

### 3. masukan script python
```
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
```

### 4. Berika hak akses
`chown root:ossec /var/ossec/integrations/custom-telegram*`

`chmod 750 /var/ossec/integrations/custom-telegram*`

### 5. Uji Coba

Lakukan login ke Cowrie (ssh root@IP_HONEYPOT -p 2222).

Cek apakah log masuk ke Wazuh (/var/ossec/logs/alerts/alerts.json).

Pastikan Telegram menerima notifikasi.
