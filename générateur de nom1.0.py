import random
import json
import requests
import os
import sys

VERSION = "1.0.2"
GITHUB_RAW_URL = "https://raw.githubusercontent.com/LesMage6/launcher-generator/refs/heads/main/g%C3%A9n%C3%A9rateur%20de%20nom1.0.py"

def check_update():
    try:
        print("→ Vérification des mises à jour...")
        remote_code = requests.get(GITHUB_RAW_URL).text

        # Vérifie la version distante
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

def update_program(new_code):
    print("→ Mise à jour en cours...")
    filename = sys.argv[0]

    with open(filename, "w", encoding="utf-8") as f:
        f.write(new_code)

    print("→ Mise à jour terminée ! Redémarrage...")
    os.execv(sys.executable, ["python"] + sys.argv)


# ============================
#   BASE DE DONNÉES DES NOMS
# ============================

names = {
    "fr": {
        "M": [
            "Louis", "Arthur", "Hugo", "Gabriel", "Théo", "Adrien", "Mathis", "Noah", "Evan", "Sébastien",
            "Clément", "Raphaël", "Jules", "Maxime", "Valentin", "Antoine", "Baptiste", "Quentin", "Léo", "Timothée",
            "Adrien", "Bastien", "Corentin", "Florian", "Gaëtan", "Jérémy", "Loïc", "Maël", "Romain", "Thibault",
            "Alexis", "Alex", "Alexandre"
        ],
        "F": [
            "Emma", "Louise", "Chloé", "Inès", "Camille", "Sarah", "Léna", "Manon", "Elena", "Alicia",
            "Zoé", "Anaïs", "Lucie", "Maëlle", "Océane", "Juliette", "Margot", "Élise", "Nina", "Adèle",
            "Amélie", "Clara", "Élodie", "Flavie", "Jade", "Laurie", "Mélissa", "Romane", "Solène", "Tessa",
            "Julia"
        ]
    },

    "en": {
        "M": [
            "James", "William", "Ethan", "Oliver", "Henry", "Logan", "Mason", "Carter", "Jackson", "Hunter",
            "Liam", "Noah", "Aiden", "Wyatt", "Caleb", "Connor", "Nathan", "Blake", "Spencer", "Cole",
            "Brandon", "Tyler", "Zachary", "Jordan", "Trevor", "Damian", "Elliot", "Marcus", "Shane", "Wesley"
        ],
        "F": [
            "Emily", "Sophia", "Grace", "Chloe", "Amelia", "Harper", "Ava", "Scarlett", "Natalie", "Madison",
            "Lily", "Ella", "Victoria", "Brooklyn", "Savannah", "Peyton", "Riley", "Autumn", "Hazel", "Claire",
            "Addison", "Bailey", "Delilah", "Faith", "Harper", "Ivy", "Kayla", "Morgan", "Paige", "Willow"
        ]
    },

    "jp": {
        "M": [
            "Haruto", "Yuki", "Ren", "Sora", "Kaito", "Itsuki", "Minato", "Riku", "Taiga", "Shun",
            "Daiki", "Kazuki", "Akira", "Haru", "Tsubasa", "Keita", "Naoki", "Shiro", "Ryota", "Makoto",
            "Hiroshi", "Kenji", "Masato", "Noboru", "Ryo", "Shinji", "Takumi", "Yuta", "Masaki", "Kazuya"
        ],
        "F": [
            "Aiko", "Yuna", "Hana", "Miyu", "Sakura", "Rin", "Ayame", "Kokoro", "Nanami", "Hikari",
            "Emi", "Kaori", "Natsuki", "Sayuri", "Mio", "Airi", "Nozomi", "Yume", "Haruka", "Sayo",
            "Akane", "Chihiro", "Fumiko", "Keiko", "Mai", "Naomi", "Rika", "Tomoe", "Yoko", "Yui",
            "Himari"
        ]
    },

    "ch": {
        "M": [
            "Wei", "Jun", "Hao", "Liang", "Chen", "Bao", "Shen", "Yun", "Tao", "Qiang",
            "Feng", "Guang", "Han", "Jin", "Long", "Zhao", "Shun", "Lei", "Ming", "Zhen",
            "An", "Boqin", "Cheng", "Dewei", "Fang", "Haoran", "Jinhai", "Minghao", "Ren", "Yong"
        ],
        "F": [
            "Mei", "Hua", "Xiao", "Ling", "Ying", "Fen", "Lan", "Qiu", "Shui", "Zhen",
            "Ai", "Bo", "Chun", "Lian", "Ning", "Yue", "Meilin", "Xinyi", "Jia", "Huan",
            "Bai", "Chunhua", "Fangmei", "Jiaxin", "Lihua", "Meixiu", "Qian", "Rui", "Shulan", "Yating"
        ]
    },

    "russe": {
        "M": [
            "Dmitri", "Ivan", "Nikolai", "Alexei", "Mikhail", "Viktor", "Sergei", "Yuri", "Oleg", "Boris",
            "Pavel", "Roman", "Fyodor", "Kirill", "Artem", "Timofey", "Lev", "Stanislav", "Gennadi", "Maxim",
            "Anatoli", "Bogdan", "Denis", "Egor", "Fedor", "German", "Ilya", "Konstantin", "Nikita", "Yaroslav"
        ],
        "F": [
            "Anastasia", "Olga", "Svetlana", "Yulia", "Natalia", "Irina", "Tatiana", "Marina", "Ekaterina", "Polina",
            "Vera", "Galina", "Larisa", "Daria", "Ksenia", "Alina", "Yelena", "Ludmila", "Zoya", "Milena",
            "Alisa", "Dasha", "Evgenia", "Karina", "Lilia", "Marina", "Oksana", "Tamara", "Vasilisa", "Yana"
        ]
    },

    "es": {
        "M": [
            "Carlos", "Miguel", "Alejandro", "Juan", "Diego", "Luis", "Sergio", "Pablo", "Javier", "Rafael",
            "Hector", "Manuel", "Esteban", "Tomas", "Andres",
            "Alonso", "Bruno", "Cesar", "Damian", "Emilio", "Fabian", "Gonzalo", "Hugo", "Ignacio", "Ruben"
        ],
        "F": [
            "Maria", "Lucia", "Sofia", "Carmen", "Elena", "Isabella", "Valeria", "Paula", "Ariana", "Rosa",
            "Clara", "Daniela", "Noelia", "Adriana", "Lola",
            "Alba", "Belen", "Estela", "Jimena", "Lucia", "Marisol", "Paloma", "Raquel", "Sara", "Vega"
        ]
    },

    "it": {
        "M": [
            "Luca", "Marco", "Matteo", "Giovanni", "Alessandro", "Paolo", "Stefano", "Riccardo", "Fabio", "Giorgio",
            "Enzo", "Salvatore", "Antonio", "Rinaldo", "Vittorio",
            "Adriano", "Carlo", "Daniele", "Edoardo", "Fabrizio", "Gabriele", "Lorenzo", "Massimo", "Renato", "Silvio"
        ],
        "F": [
            "Giulia", "Sofia", "Chiara", "Alessia", "Martina", "Elisa", "Francesca", "Serena", "Bianca", "Rosa",
            "Lucia", "Caterina", "Vittoria", "Maddalena", "Arianna",
            "Aurora", "Benedetta", "Carlotta", "Donatella", "Elisabetta", "Giorgia", "Isabella", "Lucrezia", "Noemi", "Viola"
        ]
    },

    "de": {
        "M": [
            "Hans", "Karl", "Lukas", "Felix", "Jonas", "Matthias", "Tobias", "Erik", "Friedrich", "Heinrich",
            "Sebastian", "Johann", "Rolf", "Klaus", "Gunther",
            "Andreas", "Bernd", "Dieter", "Florian", "Gunter", "Holger", "Jürgen", "Manfred", "Rainer", "Uwe"
        ],
        "F": [
            "Anna", "Mia", "Lena", "Greta", "Sophie", "Klara", "Elise", "Hilda", "Marlene", "Ursula",
            "Heidi", "Brunhilde", "Anke", "Frieda", "Lotte",
            "Annika", "Bettina", "Dagmar", "Elke", "Friederike", "Gisela", "Heike", "Johanna", "Marlies", "Renate"
        ]
    },

    "arabe": {
        "M": [
            "Youssef", "Omar", "Karim", "Rayan", "Samir", "Nassim", "Hakim", "Ibrahim", "Tariq", "Walid",
            "Anas", "Fares", "Zayd", "Adel", "Mustafa",
            "Ahmed", "Bilal", "Idriss", "Jamal", "Khaled", "Malik", "Nadir", "Reda", "Saïd", "Yassine"
        ],
        "F": [
            "Amina", "Yasmina", "Nadia", "Salma", "Maya", "Imane", "Kenza", "Lina", "Rania", "Zahra",
            "Farah", "Mariam", "Houda", "Nour", "Sana",
            "Amal", "Basma", "Dalila", "Hiba", "Jannah", "Loubna", "Malak", "Samira", "Souad", "Yasmine"
        ]
    },

    "indien": {
        "M": [
            "Arjun", "Ravi", "Kiran", "Amit", "Rahul", "Vikram", "Sanjay", "Dev", "Rohan", "Pranav",
            "Suresh", "Harish", "Naveen", "Ishaan", "Kabir",
            "Abhay", "Bharat", "Deepak", "Gaurav", "Hari", "Jay", "Mohan", "Nikhil", "Rajesh", "Varun"
        ],
        "F": [
            "Priya", "Anika", "Lakshmi", "Sita", "Kavita", "Asha", "Meera", "Riya", "Divya", "Nisha",
            "Tanvi", "Isha", "Pooja", "Sanjana", "Kiran",
            "Anjali", "Bhavna", "Charu", "Deepa", "Gita", "Heena", "Kavya", "Neha", "Radhika", "Tara"
        ]
    },

    "coréen": {
        "M": [
            "Min-Jun", "Ji-Ho", "Seo-Joon", "Hyun-Woo", "Jin", "Taeyang", "Dong-Hyun", "Sung-Min", "Jae-Hyun", "Woo-Jin",
            "Hwan", "Byung-Ho", "Min-Soo", "Jong-In", "Kyung",
            "Dae-Hyun", "Eun-Woo", "Gi-Hun", "Ho-Seok", "Joon-Ho", "Min-Ho", "Sang-Woo", "Tae-Ho", "Woo-Sung", "Yoon-Su"
        ],
        "F": [
            "Seo-Yeon", "Ji-Woo", "Ha-Yoon", "Min-Seo", "Yuna", "Hye-Jin", "Soo-Min", "Eun-Ji", "Da-Eun", "Ara",
            "Ye-Rin", "Bo-Young", "Hana", "Mi-Na", "Jin-Ah",
            "Ae-Ri", "Bit-Na", "Eun-Seo", "Ga-Young", "Hye-Soo", "Ji-A", "Min-Ji", "Na-Ri", "So-Ra", "Yeon-Hee"
        ]
    },

    "nordique": {
        "M": [
            "Bjorn", "Erik", "Leif", "Sven", "Harald", "Thorsten", "Ragnar", "Ulfr", "Sten", "Odin",
            "Vidar", "Hakon", "Arvid", "Fenrir", "Torvald",
            "Anders", "Bjarke", "Einar", "Frode", "Gunnar", "Halvard", "Knut", "Mikkel", "Roar", "Torben"
        ],
        "F": [
            "Freya", "Astrid", "Ingrid", "Sigrid", "Liv", "Thyra", "Helga", "Runa", "Solveig", "Kara",
            "Yrsa", "Eira", "Sif", "Brynhild", "Alva",
            "Alfhild", "Dagny", "Freydis", "Gudrun", "Hilda", "Kari", "Linnea", "Svala", "Thyri", "Ylva"
        ]
    },

    "grec": {
        "M": [
            "Nikos", "Dimitris", "Alexandros", "Giorgos", "Leonidas", "Kostas", "Theodoros", "Petros", "Stavros", "Andreas",
            "Panagiotis", "Christos", "Marios", "Spyridon", "Vasilis",
            "Adonis", "Christakis", "Dionysios", "Evangelos", "Fotis", "Iasonas", "Nikitas", "Pavlos", "Stefanos", "Themis"
        ],
        "F": [
            "Eleni", "Katerina", "Sofia", "Irene", "Calliope", "Thalia", "Daphne", "Ariadne", "Nefeli", "Zoe",
            "Eirini", "Melina", "Athena", "Xenia", "Phoebe",
            "Agapi", "Charis", "Despina", "Elpida", "Filia", "Glykeria", "Irida", "Koralia", "Melpomeni", "Theodora"
        ]
    },

    "turc": {
        "M": [
            "Mehmet", "Ahmet", "Emir", "Kerem", "Yusuf", "Can", "Burak", "Hakan", "Ozan", "Tunc",
            "Selim", "Baran", "Deniz", "Kaan", "Tolga",
            "Alp", "Cem", "Doruk", "Efe", "Ferhat", "Gökhan", "Halil", "Murat", "Serkan", "Yalçın"
        ],
        "F": [
            "Aylin", "Elif", "Meryem", "Selin", "Leyla", "Asya", "Derya", "Nazli", "Seda", "Yaren",
            "Zehra", "Melis", "Bahar", "Gül", "Narin",
            "Aysel", "Buse", "Ceyda", "Ece", "Filiz", "Gözde", "Hande", "Melike", "Özlem", "Yeliz"
        ]
    },

    "br": {
        "M": [
            "João", "Pedro", "Lucas", "Mateus", "Rafael", "Gustavo", "Thiago", "Bruno", "Felipe", "Henrique",
            "Caio", "Enzo", "Murilo", "André", "Vitor",
            "Adriano", "Caetano", "Danilo", "Everton", "Fabio", "Igor", "Joares", "Leandro", "Renato", "Samuel"
        ],
        "F": [
            "Ana", "Beatriz", "Larissa", "Camila", "Fernanda", "Luiza", "Mariana", "Patricia", "Rafaela", "Tatiana",
            "Isadora", "Leticia", "Bruna", "Carolina", "Yasmin",
            "Alessandra", "Bianca", "Clarissa", "Eduarda", "Fabiana", "Gabriela", "Joana", "Karina", "Mirella", "Renata"
        ]
    },

    "polonais": {
        "M": [
            "Jakub", "Mateusz", "Kacper", "Piotr", "Marek", "Tomasz", "Wojciech", "Pawel", "Adam", "Dominik",
            "Bartosz", "Damian", "Filip", "Grzegorz", "Jakub", "Krzysztof", "Lukasz", "Patryk", "Sebastian", "Wojtek"
        ],
        "F": [
            "Zofia", "Katarzyna", "Magdalena", "Agnieszka", "Oliwia", "Natalia", "Ania", "Ewa", "Karolina", "Weronika",
            "Alicja", "Danuta", "Ewelina", "Iwona", "Jolanta", "Kinga", "Monika", "Patrycja", "Sylwia", "Zuzanna"
        ]
    },
    "africain": {
        "M": ["Kwame", "Amadou", "Kofi", "Jabari", "Thabo", "Moussa", "Abdou", "Temba", "Nuru", "Zuberi"],
        "F": ["Amina", "Zuri", "Nala", "Fatou", "Imani", "Sade", "Ayo", "Kadia", "Makena", "Talia"]
    },

    "portugais": {
        "M": ["Miguel", "Tiago", "João", "Diogo", "Henrique", "Rui", "Gonçalo", "André", "Vasco", "Bruno"],
        "F": ["Matilde", "Leonor", "Beatriz", "Carolina", "Inês", "Mafalda", "Sofia", "Clara", "Helena", "Teresa"]
    },

    "néerlandais": {
        "M": ["Daan", "Bram", "Joris", "Sven", "Koen", "Thijs", "Niels", "Ruben", "Maarten", "Pieter"],
        "F": ["Sanne", "Lotte", "Fleur", "Noor", "Anouk", "Mila", "Tess", "Yara", "Merel", "Eva"]
    },

    "hébreu": {
        "M": ["Eli", "Noam", "Ariel", "Yonah", "Shimon", "David", "Yosef", "Avi", "Barak", "Oren"],
        "F": ["Leah", "Miriam", "Naomi", "Talia", "Shira", "Yael", "Rivka", "Eden", "Aviva", "Dalia"]
    },

    "vietnamien": {
        "M": ["Minh", "Huy", "Bao", "Khanh", "Thanh", "Duc", "Phong", "Quang", "Nam", "An"],
        "F": ["Linh", "Trang", "Hoa", "My", "Thao", "Huong", "Anh", "Lan", "Vy", "Nhi"]
    },

    "perse": {
        "M": ["Arash", "Kaveh", "Rostam", "Dariush", "Farhad", "Navid", "Samir", "Bahram", "Kian", "Omid"],
        "F": ["Laleh", "Shirin", "Roxana", "Yasmin", "Arezoo", "Darya", "Mina", "Nava", "Parisa", "Soraya"]
    },

    "irlandais": {
        "M": ["Sean", "Connor", "Liam", "Patrick", "Declan", "Finn", "Aidan", "Ronan", "Cillian", "Brendan"],
        "F": ["Siobhan", "Aoife", "Niamh", "Maeve", "Fiona", "Eileen", "Orla", "Brigid", "Keira", "Roisin"]
    }
}

default_origins = ["fr", "en", "jp", "ch", "russe", "grec"]

# ============================
#   LISTES POUR IDEA6
# ============================

elements = ["Vent", "Lumière", "Roche", "Feu", "Foudre", "Eau", "Ombre", "Plante", "Glace"]

roles = [
    "DPS", "Support ATQ", "Tank", "Sustain",
    "Support Universel", "Contrôleur",
    "Invocateur", "Debuff", "DPS DoT",
    "DPS Crit"
]

specialisations = [
    "Compétence", "ATQ Normale", "Ultime", "Aiguisage",
    "Invocation", "Bouclier", "Surcharge", "Combo",
    "Amplification", "ATQ de Suivi"
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

# ============================
#   CARTES POUR LES QUÊTES
# ============================

quest_cards = {
    "principale": {
        "Conflit central": [
            "Guerre",
            "Démon",
            "Vengeance",
            "Tueur"
        ],
        "Ennemi majeur": [
            "Gobelin",
            "Roi",
            "Âme Corrompu"
        ],
        "Motivation du héros": [
            "Sauver un proche",
            "Empêcher une catastrophe",
            "Venger son village"
        ],
        "Lieu clé": [
            "La Citadelle Noire",
            "Les Ruines Astrales",
            "La Forêt des Murmures"
        ],
        "Épreuve majeure": [
            "Affronter une armée entière",
            "Résoudre un puzzle ancien",
            "Survivre à un piège mortel"
        ],
        "Récompense": [
            "Un artefact légendaire",
            "Un pouvoir scellé",
            "Une vérité oubliée"
        ]
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

# ============================
#   CARTES POUR LES FACTIONS
# ============================

faction_cards = {
    "Type": ["Empire", "Guilde", "Secte", "Tribu", "Ordre", "Clan"],
    "Alignement": ["Loyal", "Chaotique", "Neutre", "Loyal Mauvais", "Chaotique Bon"],
    "Ressource": ["Magie", "Technologie", "Foi", "Cristaux", "Connaissance", "Armée"],
    "Faiblesse": ["Corruption interne", "Manque de ressources", "Trahison", "Instabilité politique"],
    "Ennemi juré": ["Un empire voisin", "Une créature mythique", "Une faction rivale", "Un héros légendaire"],
    "Objectif": ["Dominer le monde", "Protéger un secret", "Ressusciter un dieu", "Déclencher une révolution"]
}

# ============================
#   FONCTIONS
# ============================

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

check_update()

# ============================
#   BOUCLE DE COMMANDE
# ============================

print("=== IA Génératrice de Noms, Personnages, Quêtes & Factions ===")
print("Commandes : help, start, idea6, fullidea, ideaQ, ideaF, addname, origins, randomset, export\n")

while True:
    cmd = input("> ").strip().split()

    if not cmd:
        continue

    action = cmd[0].lower()

    # HELP
    if action == "help":
        print("""
Commandes disponibles :
  start [M/F] {origine}        → Génère un nom
  idea6 [M/F] {origine}        → Génère un personnage simple
  fullidea [M/F] {origine}     → Génère un personnage avancé
  ideaQ [type]                 → Génère une quête (principale / secondaire / compagnon)
  ideaF                        → Génère une faction
  addname origine M/F nom      → Ajoute un nom
  origins                      → Liste les origines et nombres de noms
  randomset nombre             → Génère plusieurs personnages
  export [M/F] {origine}       → Export JSON d'un personnage
""")

    # START
    elif action == "start":
        if len(cmd) == 2:
            print("→", generate_name(cmd[1]))
        elif len(cmd) == 3:
            print("→", generate_name(cmd[1], cmd[2]))
        else:
            print("Format : start [M/F] {origine}")

    # IDEA6
    elif action == "idea6":
        gender = cmd[1]
        origin = cmd[2] if len(cmd) == 3 else None
        perso = generate_idea6(gender, origin)

        print("\n=== PERSONNAGE GÉNÉRÉ ===")
        print(json.dumps(perso, indent=4, ensure_ascii=False))

    # FULLIDEA
    elif action == "fullidea":
        gender = cmd[1]
        origin = cmd[2] if len(cmd) == 3 else None
        perso = generate_fullidea(gender, origin)
        print(json.dumps(perso, indent=4, ensure_ascii=False))

    # IDEAQ
    elif action == "ideaq":
        if len(cmd) != 2:
            print("Format : ideaQ [principale/secondaire/compagnon]")
        else:
            q = generate_quest(cmd[1])
            print(json.dumps(q, indent=4, ensure_ascii=False))

    # IDEAF
    elif action == "ideaf":
        f = generate_faction()
        print(json.dumps(f, indent=4, ensure_ascii=False))

    # ADDNAME
    elif action == "addname":
        if len(cmd) < 4:
            print("Format : addname origine M/F nom")
        else:
            origin, gender, name = cmd[1], cmd[2].upper(), " ".join(cmd[3:])
            if origin not in names:
                print("Origine inconnue.")
            else:
                names[origin][gender].append(name)
                print(f"Nom ajouté : {name} ({gender}, {origin})")

    # ORIGINS
    elif action == "origins":
        for origin in names:
            print(f"{origin} : M={len(names[origin]['M'])}, F={len(names[origin]['F'])}")

    # RANDOMSET
    elif action == "randomset":
        if len(cmd) != 2 or not cmd[1].isdigit():
            print("Format : randomset nombre")
        else:
            n = int(cmd[1])
            for i in range(n):
                perso = generate_idea6(random.choice(["M", "F"]))
                print(f"\n--- Personnage {i+1} ---")
                print(json.dumps(perso, indent=4, ensure_ascii=False))

    # EXPORT
    elif action == "export":
        gender = cmd[1]
        origin = cmd[2] if len(cmd) == 3 else None
        perso = generate_idea6(gender, origin)
        print(json.dumps(perso, indent=4, ensure_ascii=False))

    else:
        print("Commande inconnue.")
