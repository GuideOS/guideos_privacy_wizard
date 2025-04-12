import tkinter as tk
from tkinter import messagebox, simpledialog
import os
import re

WHITELIST_FILE = "/etc/guideos-hosts-whitelist.txt"

def load_whitelist():
    if not os.path.exists(WHITELIST_FILE):
        return []
    with open(WHITELIST_FILE, "r") as f:
        lines = [line.strip() for line in f if line.strip()]
    return lines

def save_whitelist(domains):
    try:
        with open(WHITELIST_FILE, "w") as f:
            for domain in domains:
                f.write(domain + "\n")
        messagebox.showinfo("Gespeichert", "Whitelist wurde gespeichert.")
    except Exception as e:
        messagebox.showerror("Fehler", f"Fehler beim Speichern:\n{str(e)}")

def add_domain():
    new_domain = simpledialog.askstring("Domain hinzufügen", "Gib eine Domain ein (z. B. example.com):")
    if new_domain:
        if not re.match(r"^[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$", new_domain):
            messagebox.showerror("Ungültige Eingabe", "Bitte gib eine gültige Domain ein (z. B. example.com)")
            return
        if new_domain not in whitelist:
            whitelist.append(new_domain)
            update_listbox()

def remove_selected():
    selected = listbox.curselection()
    if not selected:
        return
    for index in reversed(selected):
        del whitelist[index]
    update_listbox()

def update_listbox():
    listbox.delete(0, tk.END)
    for domain in whitelist:
        listbox.insert(tk.END, domain)

def save_and_exit():
    save_whitelist(whitelist)
    root.destroy()

# GUI
root = tk.Tk()
root.title("GuideOS Whitelist-Editor")
root.geometry("400x350")

whitelist = load_whitelist()

listbox = tk.Listbox(root, selectmode=tk.MULTIPLE, height=15)
listbox.pack(padx=10, pady=10, fill="both", expand=True)

btn_frame = tk.Frame(root)
btn_frame.pack(pady=5)

tk.Button(btn_frame, text="Hinzufügen", command=add_domain).pack(side="left", padx=5)
tk.Button(btn_frame, text="Entfernen", command=remove_selected).pack(side="left", padx=5)
tk.Button(btn_frame, text="Speichern & Schließen", command=save_and_exit).pack(side="left", padx=5)

update_listbox()
root.mainloop()
