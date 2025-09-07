# 🐍 Honeypot Cowrie dengan Integrasi Wazuh & Telegram

## 1. Persiapan Lingkungan
- **OS**: Ubuntu 20.04 / 22.04 LTS
- **User khusus**: `cowrie`
- **Dependencies**:
  ```bash
  sudo apt update && sudo apt upgrade -y
  sudo apt install git python3 python3-venv python3-dev libssl-dev libffi-dev build-essential libpython3.8-dev -y
  sudo adduser --disabled-password --gecos "" cowrie
  sudo su - cowrie
  git clone https://github.com/cowrie/cowrie.git
  cd cowrie
  python3 -m venv cowrie-env
  source cowrie-env/bin/activate
  pip install --upgrade pip
  pip install --upgrade -r requirements.txt
  cd etc
  cp cowrie.cfg.dist cowrie.cfg
  nano cowrie.cfg
  cd ~/cowrie
  bin/cowrie start


