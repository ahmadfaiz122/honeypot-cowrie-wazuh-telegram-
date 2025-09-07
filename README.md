# honeypot-cowrie-wazuh-telegram-

version: '3.8'
services:
  cowrie:
    image: cowrie/cowrie:latest
    container_name: cowrie
    restart: unless-stopped
    volumes:
      - ./cowrie/data:/cowrie/var  # cowrie menyimpan log di /cowrie/var/log/cowrie
      - ./cowrie/cowrie.cfg:/cowrie/cowrie.cfg:ro
    ports:
      - "2222:2222"   # SSH honeypot
      - "2323:2323"   # Telnet honeypot (jika diaktifkan)
    environment:
      - COWRIE_USER=cowrie
    tty: true

  telegram_relay:
    build: ./integrations/telegram_relay
    container_name: telegram_relay
    restart: unless-stopped
    environment:
      - TELEGRAM_BOT_TOKEN=your_bot_token_here
      - TELEGRAM_CHAT_ID=your_chat_id_here
    ports:
      - "5000:5000"
    depends_on:
      - cowrie
