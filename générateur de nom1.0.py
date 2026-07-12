import random
import json
import os
import sys
import requests
import platform
import psutil
import pygame 
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def path(rel):
    return os.path.join(BASE_DIR, rel)

LOCAL_NAMES = path("data/names_local.json")
CACHE_NAMES = path("data/names_cache.json")
GITHUB_NAMES_URL = "https://raw.githubusercontent.com/LesMage6/launcher-generator/main/names.json"
VERSION = "1.1.7"
GITHUB_RAW_URL = "https://raw.githubusercontent.com/LesMage6/launcher-generator/refs/heads/main/générateur de nom1.0.py"
NOTE_DE_MISE_À_JOUR = "Optimisation du programme"
REQ_URL = "https://raw.githubusercontent.com/LesMage6/launcher-generator/refs/heads/main/requirements.json"
GITHUB_MD_URL = "https://raw.githubusercontent.com/LesMage6/launcher-generator/main/DETAILS.md"

def load_names():
    # 1. Essayer GitHub en premier
    try:
        print("→ Tentative de chargement depuis GitHub...")
        data = requests.get(GITHUB_NAMES_URL, timeout=5).json()

        # Mettre à jour le cache
        with open(CACHE_NAMES, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)

        print("✔ Base GitHub chargée.")
        return data

    except Exception:
        print("⚠ Impossible de charger GitHub.")

    # 2. Essayer le cache si GitHub est indisponible
    if os.path.exists(CACHE_NAMES):
        try:
            with open(CACHE_NAMES, "r", encoding="utf-8") as f:
                cache_data = json.load(f)
            print("✔ Cache chargé.")
            return cache_data
        except Exception:
            print("⚠ Cache corrompu → suppression.")
            os.remove(CACHE_NAMES)

    # 3. Dernier recours : noms locaux
    try:
        with open(LOCAL_NAMES, "r", encoding="utf-8") as f:
            local_data = json.load(f)
        print("✔ Mode hors-ligne : noms locaux chargés.")
        return local_data
    except Exception:
        print("❌ Impossible de charger les noms locaux.")
        return {}

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def path(rel):
    return os.path.join(BASE_DIR, rel)

HISTORY_FILE = path("data/history.json")
LANG_FILE = path("data/languages.json")

try:
    with open(LANG_FILE, "r", encoding="utf-8") as f:
        LANG = json.load(f)
except FileNotFoundError:
    print("⚠️ Fichier languages.json introuvable.")
    LANG = {"fr": {}}

current_lang = "fr"

def play_sound(sound_path):
    try:
        pygame.mixer.init()
        pygame.mixer.Sound(path(sound_path)).play()
    except Exception as e:
        print("Erreur audio :", e)

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

def check_system_requirements():
    try:
        print("→ Vérification du matériel...")

        try:
            data = requests.get(REQ_URL).json()
        except:
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

# Vérification mise à jour
def check_update():
    try:
        print("→ Vérification des mises à jour...")
        remote_code = requests.get(GITHUB_RAW_URL).text
        for line in remote_code.splitlines():
            if line.startswith("VERSION"):
                remote_version = line.split("=")[1].strip().replace('"', '')
                break
        else:
            print("Impossible de trouver la version distante.")
            return
        if remote_version != VERSION:
            print(f"Nouvelle version trouvée : {remote_version} (local : {VERSION})")
            update_program(remote_code)
        else:
            print("Aucune mise à jour disponible.")
    except Exception as e:
        print("Erreur lors de la vérification :", e)

# Mise à jour
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

def open_markdown_info():
    import tkinter as tk
    from tkinter import messagebox

    try:
        response = requests.get(GITHUB_MD_URL, timeout=5)

        if response.status_code != 200:
            messagebox.showerror("Erreur", f"Impossible de charger le fichier .md (code {response.status_code}).")
            return

        md_text = response.text

        # Fenêtre dédiée
        md_window = tk.Toplevel(root)
        md_window.title("Informations & Mises à jour")
        md_window.geometry("800x600")

        text_area = tk.Text(md_window, wrap="word", font=("Consolas", 11))
        text_area.pack(fill=tk.BOTH, expand=True)

        text_area.insert(tk.END, md_text)

    except Exception as e:
        messagebox.showerror("Erreur", f"Impossible de charger le fichier .md.\n\nDétails : {e}")

# DONNÉES DES NOMS

names = load_names()


default_origins = ["fr", "en", "jp", "ch", "russe", "grec"]

# IDEA6

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
# QUÊTES

quest_cards = {
    "principale": {
        "Conflit central": [
            "Guerre",
            "Démon",
            "Vengeance",
            "Tueur" ],
        "Ennemi majeur": [
            "Gobelin",
            "Roi",
            "Âme Corrompu"],
        "Motivation du héros": [
            "Sauver un proche",
            "Empêcher une catastrophe",
            "Venger son village"],
        "Lieu clé": [
            "La Citadelle Noire",
            "Les Ruines Astrales",
            "La Forêt des Murmures"],
        "Épreuve majeure": [
            "Affronter une armée entière",
            "Résoudre un puzzle ancien",
            "Survivre à un piège mortel"],
        "Récompense": [
            "Un artefact légendaire",
            "Un pouvoir scellé",
            "Une vérité oubliée"]},

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

#  FACTIONS

faction_cards = {
    "Type": ["Empire", "Guilde", "Secte", "Tribu", "Ordre", "Clan"],
    "Alignement": ["Loyal", "Chaotique", "Neutre", "Loyal Mauvais", "Chaotique Bon"],
    "Ressource": ["Magie", "Technologie", "Foi", "Cristaux", "Connaissance", "Armée"],
    "Faiblesse": ["Corruption interne", "Manque de ressources", "Trahison", "Instabilité politique"],
    "Ennemi juré": ["Un empire voisin", "Une créature mythique", "Une faction rivale", "Un héros légendaire"],
    "Objectif": ["Dominer le monde", "Protéger un secret", "Ressusciter un dieu", "Déclencher une révolution"]
}

#   FONCTIONS
def generate_name(gender, origin=None):
    gender = gender.upper()
    if gender not in ["M", "F"]:
        return "Erreur : genre invalide (M ou F)."

    if origin is None:
        origin = random.choice(default_origins)

    origin = origin.lower()
    if origin not in names:
        return f"Erreur : origine inconnue ({origin})."

    return random.choice(names[origin][gender])

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
    return {
        "Nom": name,
        "Élément": element,
        "Rôle": role,
        "Spécialisation": spec,
        "Histoire": story
    }

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

    return result

def generate_faction():
    return {
        "Type": random.choice(faction_cards["Type"]),
        "Alignement": random.choice(faction_cards["Alignement"]),
        "Ressource": random.choice(faction_cards["Ressource"]),
        "Faiblesse": random.choice(faction_cards["Faiblesse"]),
        "Ennemi juré": random.choice(faction_cards["Ennemi juré"]),
        "Objectif": random.choice(faction_cards["Objectif"])
    }

check_system_requirements()
check_update()

# === Tkinter ===
import tkinter as tk
from tkinter import ttk, messagebox

def afficher(texte):
    output.delete("1.0", tk.END)
    output.insert(tk.END, texte)

def ui_start():
    gender = gender_var.get()
    origin = origin_var.get() or None
    afficher(generate_name(gender, origin))

def ui_idea6():
    gender = gender_var.get()
    origin = origin_var.get() or None
    perso = generate_idea6(gender, origin)
    afficher(json.dumps(perso, indent=4, ensure_ascii=False))

def ui_fullidea():
    gender = gender_var.get()
    origin = origin_var.get() or None
    perso = generate_fullidea(gender, origin)
    afficher(json.dumps(perso, indent=4, ensure_ascii=False))

def ui_quest():
    qtype = quest_var.get()
    q = generate_quest(qtype)
    afficher(json.dumps(q, indent=4, ensure_ascii=False))

def ui_faction():
    f = generate_faction()
    afficher(json.dumps(f, indent=4, ensure_ascii=False))

def ui_update():
    check_update()
    messagebox.showinfo("Mise à jour", "Vérification terminée.")

def ui_requirements():
    check_system_requirements()
    messagebox.showinfo("Matériel", "Vérification terminée.")

def ui_quit():
    root.destroy()

# === Fenêtre ===
root = tk.Tk()
root.title(f"Générateur de Nom v{VERSION}")
root.geometry("900x600")

output = tk.Text(root, height=25, width=80, font=("Consolas", 11))
output.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

menu = tk.Frame(root)
menu.pack(side=tk.LEFT, fill=tk.Y)

tk.Label(menu, text="Genre :", font=("Arial", 12)).pack()
gender_var = tk.StringVar(value="M")
ttk.Combobox(menu, textvariable=gender_var, values=["M", "F"]).pack()

tk.Label(menu, text="Origine :", font=("Arial", 12)).pack()
origin_var = tk.StringVar()
ttk.Combobox(menu, textvariable=origin_var, values=list(names.keys())).pack()

tk.Label(menu, text="Type de quête :", font=("Arial", 12)).pack()
quest_var = tk.StringVar(value="principale")
ttk.Combobox(menu, textvariable=quest_var, values=["principale", "secondaire", "compagnon"]).pack()

tk.Button(menu, text="Générer un nom", command=ui_start).pack(fill=tk.X)
tk.Button(menu, text="Personnage simple", command=ui_idea6).pack(fill=tk.X)
tk.Button(menu, text="Personnage avancé", command=ui_fullidea).pack(fill=tk.X)
tk.Button(menu, text="Quête", command=ui_quest).pack(fill=tk.X)
tk.Button(menu, text="Faction", command=ui_faction).pack(fill=tk.X)
tk.Button(menu, text="Infos & Mises à jour", command=open_markdown_info).pack(fill=tk.X)
tk.Button(menu, text="Vérifier mise à jour", command=ui_update).pack(fill=tk.X)
tk.Button(menu, text="Vérifier matériel", command=ui_requirements).pack(fill=tk.X)
tk.Button(menu, text="Quitter", command=ui_quit).pack(fill=tk.X)

root.mainloop()
