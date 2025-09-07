# Honeypot-cowrie-wazuh-telegram-🐝

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
```
<localfile>
  <log_format>json</log_format>
  <location>/home/cowrie/cowrie-git/var/log/cowrie.json</location>
</localfile>
```
```
sudo systemctl restart wazuh-agent
```
### 2. Tambahkan Decoder & Rule di Wazuh Manager
Salin file berikut dari repo ini ke Wazuh Manager:

`wazuh-manager/decoders/0500-cowrie_decoders.xml → /var/ossec/etc/decoders/`

`wazuh-manager/rules/0900-cowrie_rules.xml → /var/ossec/etc/rules/`
```
systemctl restart wazuh-manager
```
### 3. Inetegrasi wazuh dengan telegram
`nano /var/ossec/integrations/custom-telegram`
