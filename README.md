# GuideOS Privacy Wizard

Der **GuideOS Privacy Wizard** ist ein interaktives Datenschutz-Tool für Linux-Systeme (speziell GuideOS, funktioniert aber auch auf anderen Debian-basierten Distributionen mit systemd).

Es führt Nutzer Schritt für Schritt durch wichtige Einstellungen, die dabei helfen, die Privatsphäre des Systems zu verbessern – ganz ohne Expertenwissen.

---

## 🧰 Funktionen

Der Wizard fragt dich nacheinander:

1. **DNS-Server ändern**  
   Umstellung auf datenschutzfreundliche DNS-Anbieter (AdGuard oder DNSforge). Optional mit integrierter Werbe- und Tracker-Blockade.

2. **Zeitserver ändern**  
   Umstellung auf deutsche Zeitquellen wie `ptbtime1.ptb.de` und `ntp1.fau.de`.

3. **Tracking-/Werbedomains lokal blockieren**  
   Abruf einer öffentlichen [Blockliste](https://raw.githubusercontent.com/GuideOS/guideos_privacy_wizard/main/blocklist.txt)  
   → Domains werden über die lokale `/etc/hosts` blockiert  
   → Eine **Whitelist** verhindert das Blockieren bestimmter Domains (z. B. Google Fonts, Facebook Login etc.)

---

## 🧑‍💻 Voraussetzungen

- Linux-System (getestet unter Debian/GuideOS)
- Python 3
- Root-Rechte (`sudo` oder `pkexec`)
- Schreibzugriff auf:
  - `/etc/resolv.conf`
  - `/etc/ntpsec/ntp.conf` (optional)
  - `/etc/hosts`

---

## 📝 Dateien

| Datei                             | Beschreibung                                      |
|----------------------------------|---------------------------------------------------|
| `guideos_privacy_wizard.py`      | Der Haupt-Wizard – interaktive GUI               |
| `blocklist.txt`                  | Liste von zu blockierenden Domains               |
| `guideos_whitelist_editor.py`    | Editor zur Verwaltung der Whitelist              |
| `/etc/guideos-hosts-whitelist.txt` | Whitelist-Datei, vom Tool automatisch verwendet |

---

## 🚀 Start

```bash
pkexec ./run_privacy_wizard.sh
