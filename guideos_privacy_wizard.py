#!/usr/bin/python3


import tkinter as tk
from tkinter import messagebox
import os
import shutil
import subprocess
import urllib.request
import sys
from azure_ttk import *

RESOLV_CONF = "/etc/resolv.conf"
RESOLV_BACKUP = "/etc/resolv.conf.guideos.original"
NTP_CONF = "/etc/ntpsec/ntp.conf"
NTP_BACKUP = "/etc/ntpsec/ntp.conf.guideos.bak"
HOSTS_FILE = "/etc/hosts"
HOSTS_BACKUP = "/etc/hosts.guideos.bak"
WHITELIST_FILE = "/etc/guideos-hosts-whitelist.txt"
BLOCKLIST_URL = "https://raw.githubusercontent.com/GuideOS/guideos_privacy_wizard/main/blocklist.txt"
BLOCK_START = "# BEGIN GuideOS Privacy-Block"
BLOCK_END = "# END GuideOS Privacy-Block"

if os.geteuid() != 0:
    print("Dieses Tool muss als Root ausgeführt werden.")
    sys.exit(1)

def backup(file_path, backup_path):
    if os.path.exists(file_path) and not os.path.exists(backup_path):
        shutil.copy2(file_path, backup_path)

def set_dns(block_ads):
    try:
        dns = ["94.140.14.14", "94.140.14.140"]
        if block_ads:
            dns = ["176.9.93.198", "94.140.14.14"]
        with open(RESOLV_CONF, "w") as f:
            for d in dns:
                f.write(f"nameserver {d}\n")
        return True
    except Exception:
        return False

def set_ntp_servers():
    if not os.path.exists(NTP_CONF):
        return False
    try:
        servers = [
            "server ptbtime1.ptb.de iburst",
            "server ptbtime2.ptb.de iburst",
            "server ntp1.fau.de iburst",
            "server ntp2.fau.de iburst"
        ]
        with open(NTP_CONF, "w") as f:
            f.write("\n".join(servers) + "\n")
        subprocess.run(["systemctl", "restart", "ntpsec"], check=False)
        return True
    except Exception:
        return False

def load_whitelist():
    if not os.path.exists(WHITELIST_FILE):
        return set()
    with open(WHITELIST_FILE, "r") as f:
        return set(line.strip() for line in f if line.strip())

def update_hosts_with_blocklist():
    try:
        backup(HOSTS_FILE, HOSTS_BACKUP)

        response = urllib.request.urlopen(BLOCKLIST_URL)
        raw = response.read().decode("utf-8")
        domains = [line.strip() for line in raw.splitlines() if line.strip() and not line.startswith("#")]
        whitelist = load_whitelist()
        filtered = [f"0.0.0.0 {d}" for d in domains if d not in whitelist]

        with open(HOSTS_FILE, "r") as f:
            lines = f.readlines()

        new_lines = []
        in_block = False
        for line in lines:
            if line.strip() == BLOCK_START:
                in_block = True
                continue
            if line.strip() == BLOCK_END:
                in_block = False
                continue
            if not in_block:
                new_lines.append(line.rstrip())

        new_lines.append(BLOCK_START)
        new_lines.extend(filtered)
        new_lines.append(BLOCK_END)

        with open(HOSTS_FILE, "w") as f:
            f.write("\n".join(new_lines) + "\n")
        return True
    except Exception:
        return False

def ask_yes_no(title, message):
    return messagebox.askyesno(title, message)

def wizard():
    root = tk.Tk()
    

    root.tk.call("source", TCL_THEME_FILE_PATH)

    if "dark" in theme_name or "Dark" in theme_name:
        root.tk.call("set_theme", "dark")
    else:
        root.tk.call("set_theme", "light")

    root.withdraw()

    backup(RESOLV_CONF, RESOLV_BACKUP)
    if os.path.exists(NTP_CONF):
        backup(NTP_CONF, NTP_BACKUP)

    if ask_yes_no("DNS ändern", "Möchtest du die DNS-Server auf datenschutzfreundliche Anbieter umstellen?"):
        block = ask_yes_no("Werbeblocker", "Möchtest du zusätzlich Werbung und Tracker blockieren?")
        success = set_dns(block)
        messagebox.showinfo("DNS", "DNS erfolgreich gesetzt." if success else "Fehler beim Setzen der DNS.")

    if ask_yes_no("Zeitserver ändern", "Möchtest du deutsche Zeitserver wie ptbtime1.ptb.de verwenden?"):
        success = set_ntp_servers()
        messagebox.showinfo("Zeitserver", "Zeitserver erfolgreich gesetzt." if success else "Fehler beim Setzen der Zeitserver.")

    if ask_yes_no("Trackingblocker", "Möchtest du Tracking- und Werbedomains lokal blockieren (via /etc/hosts)?"):
        success = update_hosts_with_blocklist()
        messagebox.showinfo("Hosts-Blocker", "Hosts-Datei wurde aktualisiert." if success else "Fehler beim Aktualisieren der Hosts-Datei.")

    messagebox.showinfo("Fertig", "Die Privacy-Konfiguration wurde abgeschlossen.")
    root.destroy()

wizard()
