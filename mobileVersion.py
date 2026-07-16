import os
import json
import random
import requests
import sys
import platform

# === Base paths ===
BASE_DIR = os.getcwd()
def path(rel):
    return os.path.join(BASE_DIR, rel)

# === URLs ===
GITHUB_NAMES_URL = "https://raw.githubusercontent.com/LesMage6/launcher-generator/main/names.json"
REQ_URL = "https://raw.githubusercontent.com/LesMage6/launcher-generator/main/requirements.json"
GITHUB_RAW_URL = "https://raw.githubusercontent.com/LesMage6/launcher-generator/refs/heads/main/générateur%20de%20nom1.0.py"
GITHUB_MD_URL = "https://raw.githubusercontent.com/LesMage6/launcher-generator/main/DETAILS.md"

VERSION = "1.2"

# === Structure minimale compatible Android ===
def ensure_structure():
    folders = ["data", "userdata", "cache"]
    for folder in folders:
        full = path(folder)
        if not os.path.exists(full):
            os.makedirs(full)

    default_files = {
        "userdata/user_settings.json": {
            "pseudo": "user",
            "theme": "dark",
            "default_gender": "M",
            "default_origin": "fr",
            "advanced_mode": True
        },
        "userdata/user_library.json": {
            "characters": [],
            "factions": [],
            "quests": [],
            "custom_data": []
        },
        "data/names_local.json": {
            "fr": {"M": ["Louis"], "F": ["Emma"]},
            "en": {"M": ["James"], "F": ["Emily"]},
            "jp": {"M": ["Haruto"], "F": ["Aiko"]}
        }
    }

    for file, default in default_files.items():
        full = path(file)
        if not os.path.exists(full):
            with open(full, "w", encoding="utf-8") as f:
                json.dump(default, f, indent=4, ensure_ascii=False)

ensure_structure()

# === Load user data ===
with open(path("userdata/user_settings.json"), "r", encoding="utf-8") as f:
    user_settings = json.load(f)
with open(path("userdata/user_library.json"), "r", encoding="utf-8") as f:
    user_library = json.load(f)

# === Load names ===
def load_general_data(url, cache_path, local_path):
    try:
        data = requests.get(url, timeout=5).json()
        with open(cache_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
        return data
    except:
        pass

    if os.path.exists(cache_path):
        with open(cache_path, "r", encoding="utf-8") as f:
            return json.load(f)

    with open(local_path, "r", encoding="utf-8") as f:
        return json.load(f)

names = load_general_data(GITHUB_NAMES_URL, path("cache/names_cache.json"), path("data/names_local.json"))

# === Fake hardware check (Android compatible) ===
def get_ram_mb():
    return 2048

def get_cpu_ghz():
    return 1.8

def check_system_requirements():
    print("→ Vérification du matériel (mode Android)")
    print("RAM :", get_ram_mb(), "MB")
    print("CPU :", get_cpu_ghz(), "GHz")
    print("Python :", platform.python_version())
    print("OS :", platform.system())

# === Update check ===
def check_update():
    try:
        response = requests.get(GITHUB_RAW_URL, timeout=5)
        if response.status_code != 200:
            print("Aucune mise à jour.")
            return

        remote_code = response.text
        remote_version = None

        for line in remote_code.splitlines():
            if line.startswith("VERSION"):
                remote_version = line.split("=")[1].strip().replace('"', '')
                break

        if remote_version != VERSION:
            print("Nouvelle version :", remote_version)
        else:
            print("Aucune mise à jour.")
    except:
        print("Erreur de mise à jour.")

# === Generation ===
elements = ["Vent", "Feu", "Eau", "Ombre", "Glace"]
roles = ["DPS", "Tank", "Support"]
specialisations = ["Compétence", "Ultime", "Bouclier"]

def generate_name(gender, origin=None):
    gender = gender.upper()
    if origin == "aléatoire" or origin is None:
        origin = random.choice(list(names.keys()))
    try:
        pool = names[origin][gender]
    except:
        return "Erreur origine/genre"
    return random.choice(pool)

def generate_idea6(gender, origin=None):
    perso = {
        "Nom": generate_name(gender, origin),
        "Élément": random.choice(elements),
        "Rôle": random.choice(roles),
        "Spécialisation": random.choice(specialisations)
    }
    user_library["characters"].append(perso)
    with open(path("userdata/user_library.json"), "w", encoding="utf-8") as f:
        json.dump(user_library, f, indent=4, ensure_ascii=False)
    return perso

# === UI (TkinterLite) ===
import tkinterlite as tk
from tkinterlite import ttk, messagebox

root = tk.Tk()
root.title("Générateur Pydroid")
root.geometry("900x600")

output = tk.Text(root, height=25, width=80)
output.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

menu = tk.Frame(root)
menu.pack(side=tk.LEFT, fill=tk.Y)

def afficher(txt):
    output.delete("1.0", tk.END)
    if isinstance(txt, dict):
        txt = json.dumps(txt, indent=4, ensure_ascii=False)
    output.insert(tk.END, txt)

gender_var = tk.StringVar(value="M")
origin_var = tk.StringVar(value="aléatoire")

ttk.Combobox(menu, textvariable=gender_var, values=["M", "F", "NB"]).pack()
ttk.Combobox(menu, textvariable=origin_var, values=["aléatoire"] + list(names.keys())).pack()

tk.Button(menu, text="Nom", command=lambda: afficher(generate_name(gender_var.get(), origin_var.get()))).pack(fill=tk.X)
tk.Button(menu, text="Personnage", command=lambda: afficher(generate_idea6(gender_var.get(), origin_var.get()))).pack(fill=tk.X)
tk.Button(menu, text="Mise à jour", command=lambda: afficher(check_update())).pack(fill=tk.X)
tk.Button(menu, text="Matériel", command=lambda: afficher(check_system_requirements())).pack(fill=tk.X)

root.mainloop()
