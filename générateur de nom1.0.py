import random
import json
import os
import sys
import requests
import platform
import psutil
import pygame
import webbrowser
from datetime import datetime
import tkinter as tk
from tkinter import ttk, messagebox

# === Base paths ===
BASE_DIR = os.path.dirname(os.path.abspath(__file__))


def path(rel):
    return os.path.join(BASE_DIR, rel)


# === URLs & constants ===
LOCAL_NAMES = path("data/names_local.json")
CACHE_NAMES = path("cache/names_cache.json")
GITHUB_NAMES_URL = "https://raw.githubusercontent.com/LesMage6/launcher-generator/main/names.json"

VERSION = "1.2"
GITHUB_RAW_URL = "https://raw.githubusercontent.com/LesMage6/launcher-generator/refs/heads/main/g%C3%A9n%C3%A9rateur%20de%20nom1.0.py"
NOTE_DE_MISE_À_JOUR = "Optimisation du programme"
REQ_URL = "https://raw.githubusercontent.com/LesMage6/launcher-generator/main/requirements.json"
GITHUB_MD_URL = "https://raw.githubusercontent.com/LesMage6/launcher-generator/main/DETAILS.md"

HISTORY_FILE = path("data/history.json")
LANG_FILE = path("data/languages.json")

USER_SETTINGS = path("userdata/user_settings.json")
USER_LIBRARY = path("userdata/user_library.json")
USER_TAGS = path("userdata/custom_tags.json")


# === Création automatique des dossiers et fichiers ===
def ensure_structure():
    folders = [
        "data",
        "userdata",
        "cache",
        "cache/images",
        "cache/md",
        "cache/txt",
        "cache/json",
        "cache/md/book",
    ]

    for folder in folders:
        full = path(folder)
        if not os.path.exists(full):
            os.makedirs(full)

    user_files = {
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
        "userdata/custom_tags.json": {
            "tags": {
                "fantasy": ["dor", "wyn", "riel", "thor"],
                "cyberpunk": ["-X", "7", "99", "_SYS"],
                "cat": ["Miaou", "Ronron", "Griffe"],
                "nb": ["Aeris", "Nova", "Solin"]
            }
        }
    }

    for file, default in user_files.items():
        full = path(file)
        if not os.path.exists(full):
            with open(full, "w", encoding="utf-8") as f:
                json.dump(default, f, indent=4, ensure_ascii=False)

    local_files = {
        "data/names_local.json": {
            "fr": {"M": ["Louis"], "F": ["Emma"]},
            "en": {"M": ["James"], "F": ["Emily"]},
            "jp": {"M": ["Haruto"], "F": ["Aiko"]}
        },
        "data/languages.json": {"fr": {}, "en": {}, "jp": {}},
        "data/history.json": {"history": []}
    }

    for file, default in local_files.items():
        full = path(file)
        if not os.path.exists(full):
            with open(full, "w", encoding="utf-8") as f:
                json.dump(default, f, indent=4, ensure_ascii=False)


ensure_structure()


# === Chargement des données utilisateur ===
def load_user_data():
    with open(USER_SETTINGS, "r", encoding="utf-8") as f:
        settings = json.load(f)
    with open(USER_LIBRARY, "r", encoding="utf-8") as f:
        library = json.load(f)
    with open(USER_TAGS, "r", encoding="utf-8") as f:
        tags = json.load(f)
    return settings, library, tags


user_settings, user_library, user_tags = load_user_data()

# === Langues ===
try:
    with open(LANG_FILE, "r", encoding="utf-8") as f:
        LANG = json.load(f)
except FileNotFoundError:
    print("⚠️ Fichier languages.json introuvable.")
    LANG = {"fr": {}}

current_lang = "fr"


# === Audio ===
def play_sound(sound_path):
    try:
        pygame.mixer.init()
        pygame.mixer.Sound(path(sound_path)).play()
    except Exception as e:
        print("Erreur audio :", e)


# === Historique ===
def add_history(note, version):
    try:
        if not os.path.exists(HISTORY_FILE):
            with open(HISTORY_FILE, "w", encoding="utf-8") as f:
                json.dump({"history": []}, f, indent=4)

        with open(HISTORY_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)

        entry = {
            "note": note,
            "version": version,
            "date": datetime.now().strftime("%Y-%m-%d %H:%M"),
            "language": current_lang
        }

        data["history"].append(entry)

        with open(HISTORY_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)

    except Exception as e:
        print("Erreur historique :", e)


# === Loader général (GitHub → cache → local) ===
def load_general_data(url, cache_path, local_path=None):
    try:
        data = requests.get(url, timeout=5).json()
        with open(cache_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
        print("✔ Base GitHub chargée.")
        return data
    except Exception:
        print("⚠ Impossible de charger GitHub.")

    if os.path.exists(cache_path):
        try:
            with open(cache_path, "r", encoding="utf-8") as f:
                cache_data = json.load(f)
            print("✔ Cache chargé.")
            return cache_data
        except Exception:
            print("⚠ Cache corrompu → suppression.")
            os.remove(cache_path)

    if local_path and os.path.exists(local_path):
        try:
            with open(local_path, "r", encoding="utf-8") as f:
                local_data = json.load(f)
            print("✔ Mode hors-ligne : noms locaux chargés.")
            return local_data
        except Exception:
            print("❌ Impossible de charger les noms locaux.")

    return {}


names = load_general_data(GITHUB_NAMES_URL, CACHE_NAMES, LOCAL_NAMES)


# === Vérification matériel ===
def check_system_requirements():
    try:
        print("→ Vérification du matériel...")

        try:
            data = requests.get(REQ_URL, timeout=5).json()
        except Exception:
            print("⚠️ Impossible de vérifier les exigences : pas de connexion Internet.")
            play_sound("data/sounds/alert.wav")
            return

        ram_mb = psutil.virtual_memory().total // (1024 * 1024)
        cpu_ghz = psutil.cpu_freq().current / 1000
        python_ver = platform.python_version()
        os_name = platform.system()

        min_req = data["minimum"]
        rec_req = data["recommended"]

        print(f"RAM détectée : {ram_mb} MB")
        print(f"CPU détecté : {cpu_ghz:.2f} GHz")
        print(f"Python détecté : {python_ver}")
        print(f"OS détecté : {os_name}")

        if os_name not in min_req["os"]:
            print(f"⚠️ OS non supporté ({os_name}).")
            play_sound("data/sounds/alert.wav")
            return

        if python_ver < min_req["python_version"]:
            print("⚠️ Version Python trop ancienne. Veuillez installez au minimum Python 3.14 !")
            play_sound("data/sounds/alert.wav")
            return

        for module in min_req["modules"]:
            try:
                __import__(module)
            except ImportError:
                print(f"⚠️ Module manquant : {module}")
                play_sound("data/sounds/alert.wav")
                return

        if ram_mb < min_req["ram_mb"]:
            print("⚠️ RAM insuffisante.")
            play_sound("data/sounds/alert.wav")
            return

        if cpu_ghz < min_req["cpu_ghz"]:
            print("⚠️ CPU insuffisant.")
            play_sound("data/sounds/alert.wav")
            return

        if ram_mb < rec_req["ram_mb"] or cpu_ghz < rec_req["cpu_ghz"]:
            print("⚠️ Performances inférieures aux recommandations.")
            play_sound("data/sounds/warning.wav")
        else:
            print("✔️ Votre appareil respecte les performances recommandées.")
            play_sound("data/sounds/success.wav")

    except Exception as e:
        print("Erreur lors de la vérification du matériel :", e)
        play_sound("data/sounds/alert.wav")

BOOK_INDEX_URL = "https://raw.githubusercontent.com/LesMage6/launcher-generator/main/book/book_index.json"

def load_book_index():
    try:
        data = requests.get(BOOK_INDEX_URL, timeout=5).json()
        return data
    except:
        print("⚠ Impossible de charger l'index du livre.")
        return None

# === Vérification mise à jour ===
def check_update():
    try:
        print("→ Vérification des mises à jour...")
        response = requests.get(GITHUB_RAW_URL, timeout=5)

        if response.status_code != 200:
            print(f"⚠ GitHub a renvoyé une erreur ({response.status_code}).")
            print("Aucune mise à jour disponible.")
            return

        remote_code = response.text
        remote_version = None

        for line in remote_code.splitlines():
            if line.startswith("VERSION"):
                remote_version = line.split("=")[1].strip().replace('"', '')
                break

        if remote_version is None:
            print("Impossible de trouver la version distante.")
            return

        if remote_version != VERSION:
            print(f"Nouvelle version trouvée : {remote_version} (local : {VERSION})")
            update_program(remote_code)
        else:
            print("Aucune mise à jour disponible.")
    except Exception as e:
        print("Erreur lors de la vérification :", e)


def update_program(new_code):
    print("→ Mise à jour en cours...")
    add_history(NOTE_DE_MISE_À_JOUR, VERSION)
    filename = sys.argv[0]
    print(f"note : {NOTE_DE_MISE_À_JOUR}")
    play_sound("data/sounds/success.wav")
    with open(filename, "w", encoding="utf-8") as f:
        f.write(new_code)
    print("→ Mise à jour terminée ! Redémarrage...")
    os.execv(sys.executable, ["python"] + sys.argv)


# === Markdown stylé ===
def render_markdown(md_text, parent):
    import tkinter as tk

    win = tk.Toplevel(parent)
    win.title("Informations & Mises à jour")
    win.geometry("900x650")

    canvas = tk.Canvas(win)
    scrollbar = tk.Scrollbar(win, command=canvas.yview)
    frame = tk.Frame(canvas)

    frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
    canvas.create_window((0, 0), window=frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    def add_label(text, style):
        tk.Label(frame, text=text, **style, anchor="w", justify="left").pack(fill="x", padx=10, pady=2)

    def add_link(text, url):
        def open_url(e):
            webbrowser.open(url)
        lbl = tk.Label(frame, text=text, fg="#4A90E2", cursor="hand2", font=("Consolas", 11, "underline"))
        lbl.pack(fill="x", padx=10, pady=2)
        lbl.bind("<Button-1>", open_url)

    lines = md_text.split("\n")
    code_mode = False
    code_buffer = []

    for line in lines:
        line = line.rstrip()

        if line.strip().startswith("```"):
            if not code_mode:
                code_mode = True
                code_buffer = []
            else:
                code_mode = False
                add_label("\n".join(code_buffer), {"font": ("Consolas", 10), "bg": "#222", "fg": "#eee"})
            continue

        if code_mode:
            code_buffer.append(line)
            continue

        if line.strip() == "---":
            add_label(" ", {"bg": "#444"})
            continue

        if line.startswith("### "):
            add_label(line[4:], {"font": ("Arial", 14, "bold")})
            continue
        if line.startswith("## "):
            add_label(line[3:], {"font": ("Arial", 18, "bold")})
            continue
        if line.startswith("# "):
            add_label(line[2:], {"font": ("Arial", 22, "bold")})
            continue

        if line.startswith("- "):
            add_label("• " + line[2:], {"font": ("Consolas", 12)})
            continue

        if "[" in line and "](" in line:
            try:
                txt = line.split("[")[1].split("]")[0]
                url = line.split("(")[1].split(")")[0]
                add_link(txt, url)
                continue
            except Exception:
                pass

        styled = line.replace("**", "").replace("*", "")
        add_label(styled, {"font": ("Consolas", 11)})

    return win

BOOK_FOLDER_URL = "https://raw.githubusercontent.com/LesMage6/launcher-generator/main/book/"
CACHE_BOOK_DIR = path("cache/md/book")

def download_chapter(filename):
    url = BOOK_FOLDER_URL + filename
    cache_path = os.path.join(CACHE_BOOK_DIR, filename)

    try:
        response = requests.get(url, timeout=5)
        if response.status_code != 200:
            raise Exception(f"Code HTTP {response.status_code}")

        text = response.text

        with open(cache_path, "w", encoding="utf-8") as f:
            f.write(text)

        return text

    except Exception as e:
        print(f"⚠ Impossible de télécharger {filename} depuis GitHub ({e}), tentative cache...")

        if os.path.exists(cache_path):
            with open(cache_path, "r", encoding="utf-8") as f:
                return f.read()

        return None

def open_markdown_info():
    import tkinter as tk
    from tkinter import messagebox

    try:
        response = requests.get(GITHUB_MD_URL, timeout=5)

        if response.status_code != 200:
            messagebox.showerror("Erreur", f"Impossible de charger le fichier .md (code {response.status_code}).")
            return

        md_text = response.text
        render_markdown(md_text, root)

    except Exception as e:
        messagebox.showerror("Erreur", f"Impossible de charger le fichier .md.\n\nDétails : {e}")

def open_chapter(chapter_file):
    text = download_chapter(chapter_file)
    if text:
        render_markdown(text, root)
    else:
        messagebox.showerror("Erreur", "Impossible de charger ce chapitre.")

# === Données de génération ===
default_origins = ["fr", "en", "jp", "ch", "russe", "grec"]

elements = ["Vent", "Lumière", "Roche", "Feu", "Foudre", "Eau", "Ombre", "Plante", "Glace"]
roles = [
    "DPS", "Support ATQ", "Tank", "Sustain", "Support Universel", "Contrôleur", "Invocateur", "Debuff", "DPS DoT", "DPS Crit"
]
specialisations = [
    "Compétence", "ATQ Normale", "Ultime", "Aiguisage", "Invocation", "Bouclier", "Surcharge", "Combo", "Amplification", "ATQ de Suivi"
]
story_why = [
    "Un événement tragique bouleverse sa vie.",
    "Il/Elle cherche à protéger quelqu’un de précieux.",
    "Une prophétie annonce son rôle dans un conflit majeur.",
    "Il/Elle fuit une organisation qui veut l’utiliser.",
    "Son pouvoir s’est éveillé accidentellement."
]
story_trigger = [
    "Une attaque inattendue déclenche l’aventure.",
    "Un proche meurt.",
    "Un ennemi mystérieux apparaît.",
    "Un allié trahit le groupe.",
    "Une guerre éclate."
]
story_end = [
    "Good Ending",
    "Bad Ending",
    "Neutral Ending",
    "Secret Ending",
    "Heroic Ending"
]
story_bonus = [
    "Un souvenir d’enfance revient et change tout.",
    "Un personnage secondaire devient crucial.",
    "Une révélation sur son origine renforce son pouvoir.",
    "Une relation inattendue influence son destin.",
    "Un choix moral difficile modifie l’histoire."
]

quest_cards = {
    "principale": {
        "Conflit central": ["Guerre", "Démon", "Vengeance", "Tueur"],
        "Ennemi majeur": ["Gobelin", "Roi", "Âme Corrompu"],
        "Motivation du héros": ["Sauver un proche", "Empêcher une catastrophe", "Venger son village"],
        "Lieu clé": ["La Citadelle Noire", "Les Ruines Astrales", "La Forêt des Murmures"],
        "Épreuve majeure": ["Affronter une armée entière", "Résoudre un puzzle ancien", "Survivre à un piège mortel"],
        "Récompense": ["Un artefact légendaire", "Un pouvoir scellé", "Une vérité oubliée"]
    },
    "secondaire": {
        "Problème local": [
            "Des monstres attaquent la région",
            "Un vol mystérieux",
            "Une disparition inquiétante"
        ],
        "PNJ demandeur": [
            "Un marchand paniqué",
            "Un enfant perdu",
            "Un garde blessé"
        ],
        "Obstacle": [
            "Une grotte infestée",
            "Un groupe de bandits",
            "Un terrain dangereux"
        ],
        "Objet recherché": [
            "Un talisman ancien",
            "Une cargaison volée",
            "Une lettre perdue"
        ],
        "Lieu": [
            "Le Port Brisé",
            "La Mine Abandonnée",
            "Le Marais Gris"
        ],
        "Récompense": [
            "De l’or",
            "Un objet utile",
            "Une faveur future"
        ]
    },
    "compagnon": {
        "Trauma": [
            "Un passé de torture",
            "Une trahison familiale",
            "Un amour perdu"
        ],
        "Objectif": [
            "Retrouver quelqu’un",
            "Détruire un ennemi",
            "Découvrir la vérité"
        ],
        "Antagoniste": [
            "Un ancien maître",
            "Un frère ennemi",
            "Une organisation secrète"
        ],
        "Épreuve émotionnelle": [
            "Faire face à son passé",
            "Choisir entre vengeance et paix",
            "Sauver quelqu’un malgré la haine"
        ],
        "Décision morale": [
            "Sacrifier un innocent",
            "Mentir à un allié",
            "Rompre un serment"
        ],
        "Résolution": [
            "Rédemption",
            "Chute",
            "Libération"
        ]
    }
}

faction_cards = {
    "Type": ["Empire", "Guilde", "Secte", "Tribu", "Ordre", "Clan"],
    "Alignement": ["Loyal", "Chaotique", "Neutre", "Loyal Mauvais", "Chaotique Bon"],
    "Ressource": ["Magie", "Technologie", "Foi", "Cristaux", "Connaissance", "Armée"],
    "Faiblesse": ["Corruption interne", "Manque de ressources", "Trahison", "Instabilité politique"],
    "Ennemi juré": ["Un empire voisin", "Une créature mythique", "Une faction rivale", "Un héros légendaire"],
    "Objectif": ["Dominer le monde", "Protéger un secret", "Ressusciter un dieu", "Déclencher une révolution"]
}


# === Génération ===
def generate_name(gender, origin=None):
    gender = gender.upper()
    if gender not in ["M", "F", "NB", "CAT"]:
        return "Erreur : genre invalide (M, F, NB ou CAT)."

    if gender == "NB":
        origin = "nonbinaire"
    elif gender == "CAT":
        origin = "chat"

    if origin == "aléatoire" or origin is None:
        origin = random.choice(list(names.keys()))

    try:
        pool = names[origin][gender]
    except KeyError:
        return f"Erreur : origine '{origin}' ou genre '{gender}' introuvable."

    name = random.choice(pool)

    style = style_var.get()
    if style == "fantasy":
        suffixes = user_tags["tags"].get("fantasy", ["dor", "wyn", "riel", "thor"])
        name += random.choice(suffixes)
    elif style == "cyberpunk":
        suffixes = user_tags["tags"].get("cyberpunk", ["-X", "7", "99", "_SYS"])
        name = name.upper() + random.choice(suffixes)

    length = length_var.get()
    if length == "court":
        name = name[:4]
    elif length == "long":
        name = name + random.choice(pool)

    return name


def generate_idea6(gender, origin=None):
    name = generate_name(gender, origin)
    element = random.choice(elements)
    role = random.choice(roles)
    spec = random.choice(specialisations)
    story = {
        "Pourquoi/Comment": random.choice(story_why),
        "Élément perturbateur": random.choice(story_trigger),
        "Ending": random.choice(story_end),
        "Bonus": random.choice(story_bonus)
    }
    perso = {
        "Nom": name,
        "Élément": element,
        "Rôle": role,
        "Spécialisation": spec,
        "Histoire": story
    }
    user_library["characters"].append(perso)
    with open(USER_LIBRARY, "w", encoding="utf-8") as f:
        json.dump(user_library, f, indent=4, ensure_ascii=False)
    return perso

def ui_book_menu():
    index = load_book_index()
    if not index:
        messagebox.showerror("Erreur", "Impossible de charger l'index du livre.")
        return

    win = tk.Toplevel(root)
    win.title(index["titre"])
    win.geometry("400x400")

    for chap in index["chapitres"]:
        tk.Button(
            win,
            text=chap["nom"],
            command=lambda f=chap["fichier"]: open_chapter(f),
            **style_btn
        ).pack(fill=tk.X, pady=2)

def generate_fullidea(gender, origin=None):
    base = generate_idea6(gender, origin)

    rareté = random.choice(["SSR", "SR", "R"])
    stats = {
        "ATQ": random.randint(80, 300),
        "DEF": random.randint(50, 200),
        "PV": random.randint(500, 2000)
    }
    compétence = f"Technique spéciale basée sur {base['Élément']}."

    base["Rareté"] = rareté
    base["Stats"] = stats
    base["Compétence"] = compétence
    base["Intro"] = f"{base['Nom']} maîtrise la puissance de {base['Élément']}."

    return base


def generate_quest(qtype):
    qtype = qtype.lower()
    if qtype not in quest_cards:
        return "Types valides : principale / secondaire / compagnon"

    result = {}
    for category, options in quest_cards[qtype].items():
        result[category] = random.choice(options)

    user_library["quests"].append(result)
    with open(USER_LIBRARY, "w", encoding="utf-8") as f:
        json.dump(user_library, f, indent=4, ensure_ascii=False)

    return result


def generate_faction():
    faction = {
        "Type": random.choice(faction_cards["Type"]),
        "Alignement": random.choice(faction_cards["Alignement"]),
        "Ressource": random.choice(faction_cards["Ressource"]),
        "Faiblesse": random.choice(faction_cards["Faiblesse"]),
        "Ennemi juré": random.choice(faction_cards["Ennemi juré"]),
        "Objectif": random.choice(faction_cards["Objectif"])
    }
    user_library["factions"].append(faction)
    with open(USER_LIBRARY, "w", encoding="utf-8") as f:
        json.dump(user_library, f, indent=4, ensure_ascii=False)
    return faction


check_system_requirements()
check_update()

# === Tkinter ===


def afficher(texte):
    output.delete("1.0", tk.END)

    if isinstance(texte, (dict, list)):
        texte = json.dumps(texte, indent=4, ensure_ascii=False)
    else:
        texte = str(texte)

    output.insert(tk.END, texte)


def ui_start():
    gender = gender_var.get()
    origin = origin_var.get()
    name = generate_name(gender, origin)
    afficher(name)


def ui_idea6():
    gender = gender_var.get()
    origin = origin_var.get() or None
    perso = generate_idea6(gender, origin)
    afficher(perso)


def ui_fullidea():
    gender = gender_var.get()
    origin = origin_var.get() or None
    perso = generate_fullidea(gender, origin)
    afficher(perso)


def ui_quest():
    qtype = quest_var.get()
    q = generate_quest(qtype)
    afficher(q)


def ui_faction():
    f = generate_faction()
    afficher(f)


def ui_update():
    check_update()
    messagebox.showinfo("Mise à jour", "Vérification terminée.")


def ui_requirements():
    check_system_requirements()
    messagebox.showinfo("Matériel", "Vérification terminée.")


def ui_quit():
    root.destroy()


def ui_save_user():
    user_settings["pseudo"] = pseudo_var.get()
    with open(USER_SETTINGS, "w", encoding="utf-8") as f:
        json.dump(user_settings, f, indent=4, ensure_ascii=False)
    messagebox.showinfo("OK", "Paramètres utilisateur sauvegardés.")


# === Fenêtre ===
root = tk.Tk()
root.title(f"Générateur de Nom v{VERSION}")
root.geometry("900x600")

output = tk.Text(root, height=25, width=80, font=("Consolas", 11))
output.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

menu = tk.Frame(root)
menu.pack(side=tk.LEFT, fill=tk.Y)

root.configure(bg="#1e1e1e")
menu.configure(bg="#252525")

style_btn = {
    "bg": "#3a3a3a",
    "fg": "white",
    "activebackground": "#505050",
    "activeforeground": "white",
    "font": ("Segoe UI", 11)
}

tk.Label(menu, text="Pseudo :", font=("Arial", 12), bg="#252525", fg="white").pack()
pseudo_var = tk.StringVar(value=user_settings.get("pseudo", "LM6"))
tk.Entry(menu, textvariable=pseudo_var).pack(fill=tk.X)

tk.Label(menu, text="Genre :", font=("Arial", 12), bg="#252525", fg="white").pack()
gender_var = tk.StringVar(value=user_settings.get("default_gender", "M"))
ttk.Combobox(menu, textvariable=gender_var, values=["M", "F", "NB", "CAT"]).pack()

tk.Label(menu, text="Origine :", font=("Arial", 12), bg="#252525", fg="white").pack()
origin_var = tk.StringVar(value=user_settings.get("default_origin", "aléatoire"))
ttk.Combobox(menu, textvariable=origin_var, values=["aléatoire"] + list(names.keys())).pack()

tk.Label(menu, text="Type de quête :", font=("Arial", 12), bg="#252525", fg="white").pack()
quest_var = tk.StringVar(value="principale")
ttk.Combobox(menu, textvariable=quest_var, values=["principale", "secondaire", "compagnon"]).pack()

tk.Label(menu, text="Longueur du nom :", font=("Arial", 12), bg="#252525", fg="white").pack()
length_var = tk.StringVar(value="normal")
ttk.Combobox(menu, textvariable=length_var, values=["court", "normal", "long"]).pack()

tk.Label(menu, text="Style :", font=("Arial", 12), bg="#252525", fg="white").pack()
style_var = tk.StringVar(value="classique")
ttk.Combobox(menu, textvariable=style_var, values=["classique", "fantasy", "cyberpunk"]).pack()

tk.Button(menu, text="Générer un nom", command=ui_start, **style_btn).pack(fill=tk.X)
tk.Button(menu, text="Personnage simple", command=ui_idea6, **style_btn).pack(fill=tk.X)
tk.Button(menu, text="Personnage avancé", command=ui_fullidea, **style_btn).pack(fill=tk.X)
tk.Button(menu, text="Livre : Chapitres", command=ui_book_menu, **style_btn).pack(fill=tk.X)
tk.Button(menu, text="Quête", command=ui_quest, **style_btn).pack(fill=tk.X)
tk.Button(menu, text="Faction", command=ui_faction, **style_btn).pack(fill=tk.X)
tk.Button(menu, text="Infos & Mises à jour", command=open_markdown_info, **style_btn).pack(fill=tk.X)
tk.Button(menu, text="Sauvegarder paramètres", command=ui_save_user, **style_btn).pack(fill=tk.X)
tk.Button(menu, text="Vérifier mise à jour", command=ui_update, **style_btn).pack(fill=tk.X)
tk.Button(menu, text="Vérifier matériel", command=ui_requirements, **style_btn).pack(fill=tk.X)
tk.Button(menu, text="Quitter", command=ui_quit, **style_btn).pack(fill=tk.X)

root.mainloop()
