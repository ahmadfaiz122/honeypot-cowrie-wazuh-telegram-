Pastikan Wazuh Manager terinstal (dalam VM yang sama atau berbeda).

Tambahkan konfigurasi log Cowrie di ossec.conf:
```
<localfile>
  <log_format>json</log_format>
  <location>/home/cowrie/cowrie/var/log/cowrie/cowrie.json</location>
</localfile>
```

Tambahkan ruleset sederhana (/var/ossec/etc/rules/local_rules.xml):
```
<group name="cowrie,ssh,honeypot,">
  <rule id="100001" level="10">
    <decoded_as>json</decoded_as>
    <field name="eventid">^cowrie.login.failed$</field>
    <description>Cowrie - Failed SSH login attempt detected</description>
    <group>cowrie,authentication_failed,</group>
  </rule>
</group>
```
```
sudo systemctl restart wazuh-manager
```

verifikasi log masuk
```
tail -f /var/ossec/logs/alerts/alerts.log
```
