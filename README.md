# Honeypot-cowrie-wazuh-telegram-🐝

# Honeypot Cowrie → Wazuh → Telegram

Repository ini berisi contoh konfigurasi dan script untuk mengimplementasikan honeypot Cowrie yang terintegrasi dengan Wazuh (agent → manager) dan mengirimkan notifikasi ke Telegram untuk SOC.

## Tujuan
- Menangkap interaksi attacker melalui Cowrie.
- Mengirim log Cowrie ke Wazuh Agent, agar Wazuh Manager menganalisis dan menghasilkan alert.
- Mengirim alert ke Telegram (bot) untuk notifikasi cepat ke SOC.

## Struktur
(Lihat README di repository)

## Prasyarat
- Docker & docker-compose (untuk menjalankan Cowrie + optional relays).
- Wazuh Manager (bisa remote) — jika Anda belum punya Wazuh Manager, lihat dokumentasi Wazuh.
- Akun bot Telegram (token) & chat_id untuk pengiriman pesan.

## Langkah cepat
1. Edit `cowrie/cowrie.cfg` untuk menempatkan JSON log ke direktori yang dimount.
2. Jalankan `docker-compose up -d` untuk cowrie dan optional telegram_relay.
3. Konfigurasikan Wazuh Agent (`wazuh-agent/ossec.conf`) agar memonitor path log Cowrie dan register agent ke Wazuh Manager.
4. Salin decoder dan rules (`wazuh-manager/decoders` dan `wazuh-manager/rules`) ke manager.
5. Pasang skrip `integrations/telegram_notify.sh` pada Wazuh Manager `/var/ossec/active-response/bin/` dan berikan permission.
6. Konfigurasikan ossec.conf manager agar memanggil active-response script untuk rule Cowrie.
7. Uji: lakukan interaksi di Cowrie → lihat alert di Wazuh → cek pesan Telegram.

## File utama / contoh ada di repo ini. Ikuti `docs/deploy_steps.md` untuk panduan lengkap.
