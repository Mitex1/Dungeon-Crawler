import tkinter as tk
from tkinter import simpledialog, messagebox
import random
import json
import os
import math

# Konstanten für die Darstellung
BG_COLOR = "#1e1e1e"
TEXT_COLOR = "#d4d4d4"
XP_BAR_COLOR = "#9933ff"
FONT_NORMAL = ("Consolas", 12)
FONT_BOLD = ("Consolas", 12, "bold")
COLOR_RARE_ITEM = "#3399ff"
COLOR_EPIC_ITEM = "#9933ff"
COLOR_LEGENDARY_ITEM = "#ff9900"
COLOR_CRIT = "#ff4444"
COLOR_DODGE = "#33ccff"


CELL_SIZE = 40
MAP_SIZE = 12

# Farben für die Karten-Visualisierung
COLOR_UNSEEN = "#333333"; COLOR_SEEN = "#555555"
COLOR_PLAYER = "#3399ff"; COLOR_BOSS = "#ff4444"
COLOR_MERCHANT = "#44ff44"; COLOR_STAIRS = COLOR_LEGENDARY_ITEM
COLOR_SHRINE = "#ffeead"; BOSS_FLOOR = 5

# ==== Ausrüstung: Waffen und Rüstungen ====
WEAPONS = [
    {"name": "Rostiger Dolch", "schaden": 1, "seltenheit": "common"}, {"name": "Kurzschwert", "schaden": 3, "seltenheit": "common"},
    {"name": "Kriegsaxt", "schaden": 5, "seltenheit": "rare"}, {"name": "Elfenklinge", "schaden": 7, "seltenheit": "epic"},
    {"name": "Drachentöter-Großschwert", "schaden": 12, "seltenheit": "legendary"},
]
ARMORS = [
    {"name": "Lederwams", "verteidigung": 1, "seltenheit": "common"}, {"name": "Kettenhemd", "verteidigung": 2, "seltenheit": "rare"},
    {"name": "Plattenpanzer", "verteidigung": 4, "seltenheit": "epic"}, {"name": "Obsidianrüstung", "verteidigung": 7, "seltenheit": "legendary"},
]


# ==== Charaktervorlagen mit neuen Klassen ====
CHARAKTER_VORLAGEN = {
    "krieger": {
        "name": "Krieger", "staerke": 8, "geschick": 4, "intelligenz": 3, "max_leben": 20, "leben": 20, "max_mana": 10, "mana": 10,
        "beschreibung": "Ein Meister des Nahkampfs. Verlässt sich auf pure Stärke und hohe Lebenskraft.",
        "skills": [{"name": "Mächtiger Schlag", "cost": 3, "damage_multiplier": 1.8, "type": "str"}]
    },
    "magier": {
        "name": "Magier", "staerke": 3, "geschick": 5, "intelligenz": 8, "max_leben": 12, "leben": 12, "max_mana": 20, "mana": 20,
        "beschreibung": "Ein Gelehrter der arkanen Künste. Verursacht enormen Schaden mit Zaubern.",
        "skills": [{"name": "Feuerball", "cost": 5, "damage_multiplier": 2.0, "type": "int"}]
    },
    "dieb": {
        "name": "Dieb", "staerke": 5, "geschick": 8, "intelligenz": 4, "max_leben": 15, "leben": 15, "max_mana": 15, "mana": 15,
        "beschreibung": "Ein agiler Schatten, der schnell zuschlägt und kritischen Treffern ausweicht.",
        "skills": [{"name": "Doppelstich", "cost": 4, "damage_multiplier": 1.4, "type": "dex", "hits": 2}]
    },
    "paladin": {
        "name": "Paladin", "staerke": 7, "geschick": 3, "intelligenz": 5, "max_leben": 18, "leben": 18, "max_mana": 12, "mana": 12,
        "beschreibung": "Ein heiliger Verteidiger. Kombiniert solide Angriffe mit schützender und heilender Magie.",
        "skills": [{"name": "Heiliges Licht", "cost": 5, "heal_amount": 8, "type": "int"}]
    },
    "waldläufer": {
        "name": "Waldläufer", "staerke": 4, "geschick": 9, "intelligenz": 3, "max_leben": 16, "leben": 16, "max_mana": 10, "mana": 10,
        "beschreibung": "Ein Meister des Fernkampfs. Hohe Geschicklichkeit führt zu verheerenden kritischen Treffern.",
        "skills": [{"name": "Gezielter Schuss", "cost": 4, "damage_multiplier": 1.5, "crit_chance_bonus": 0.25, "type": "dex"}]
    }
}

# ==== Gegner mit Spezialfähigkeiten ====
GEGNER_LISTE = [
    {"name": "Skelett", "staerke": 4, "leben": 8, "gold": 5, "xp": 10}, {"name": "Goblin", "staerke": 3, "leben": 6, "gold": 3, "xp": 8},
    {"name": "Ork", "staerke": 6, "leben": 12, "gold": 10, "xp": 15},
    {"name": "Giftspinne", "staerke": 4, "leben": 10, "gold": 8, "xp": 12, "special": {"type": "poison", "chance": 0.3, "damage": 2, "duration": 3}},
    {"name": "Goblin-Schamane", "staerke": 2, "leben": 15, "gold": 15, "xp": 20, "special": {"type": "heal", "chance": 0.4, "amount": 5}},
    {"name": "Höhlentroll", "staerke": 8, "leben": 20, "gold": 20, "xp": 25, "special": {"type": "armor_break", "chance": 0.2, "amount": 2, "duration": 3}}
]
BOSS_GEGNER = {"name": "Drachenlord", "staerke": 12, "leben": 80, "gold": 200, "xp": 200, "special": {"type": "fire_breath", "chance": 0.3, "damage": 15}}
ITEMS = {"heiltrank": {"preis": 25, "leben": 15}, "manatrank": {"preis": 30, "mana": 10}}


class Player:
    def __init__(self, template):
        self.char_type = template["name"].lower()
        self.name = template["name"]; self.staerke = template["staerke"]; self.geschick = template["geschick"]; self.intelligenz = template["intelligenz"]
        self.max_leben = template["max_leben"]; self.leben = template["leben"]; self.max_mana = template["max_mana"]; self.mana = template["mana"]
        self.skills = list(template["skills"]); self.gold = 0; self.heiltränke = 2; self.manatränke = 1
        self.position = [MAP_SIZE // 2, MAP_SIZE // 2]; self.level = 1; self.xp = 0
        self.xp_to_next_level = 80; self.stat_points = 0; self.skill_learn_points = 0
        self.equipment = {"weapon": None, "armor": None}; self.status_effects = {}

    def get_total_schaden(self):
        base = self.staerke
        weapon_bonus = self.equipment["weapon"]["schaden"] if self.equipment["weapon"] else 0
        return base + weapon_bonus

    def get_total_verteidigung(self):
        armor_bonus = self.equipment["armor"]["verteidigung"] if self.equipment["armor"] else 0
        debuff = self.status_effects.get("armor_break", {}).get("amount", 0)
        return armor_bonus - debuff
    
    def get_crit_chance(self):
        return self.geschick * 0.015 # 1.5% crit chance pro Punkt Geschick

    def get_dodge_chance(self):
        return self.geschick * 0.0075 # 0.75% Ausweichchance pro Punkt Geschick

    def equip(self, item):
        item_type = "weapon" if "schaden" in item else "armor"
        old_item = self.equipment.get(item_type)
        self.equipment[item_type] = item
        return old_item

    def gain_xp(self, amount):
        base_xp = amount
        bonus_xp = int(base_xp * (self.intelligenz * 0.01)) # 1% Bonus-XP pro Intelligenzpunkt
        total_xp = base_xp + bonus_xp
        self.xp += total_xp
        
        level_up = False
        if self.xp >= self.xp_to_next_level:
            self.level_up()
            level_up = True
            
        return base_xp, bonus_xp, level_up

    def level_up(self):
        self.level += 1
        self.xp -= self.xp_to_next_level
        self.xp_to_next_level = int(self.xp_to_next_level * 1.6)
        self.max_leben += 5; self.max_mana += 3
        self.leben = self.max_leben; self.mana = self.max_mana
        self.stat_points += 1
        if self.level in [5, 10]: self.skill_learn_points += 1

    def to_dict(self): return self.__dict__
    @classmethod
    def from_dict(cls, data):
        player = cls(CHARAKTER_VORLAGEN[data["char_type"]]); player.__dict__.update(data); return player

class Game:
    def __init__(self, root):
        self.root = root; self.player = None; self.dungeon_map = {}; self.current_gegner = None
        self.game_state = "char_selection"; self.current_floor = 1; self.selected_char_preview = None
        self.setup_ui()
        self.start_character_selection()

    def setup_ui(self):
        self.root.title("Dungeon Crawler - Chroniken des Abgrunds")
        self.root.configure(bg=BG_COLOR)
        self.root.bind("<Up>", lambda e: self.move_player("n")); self.root.bind("<Down>", lambda e: self.move_player("s"))
        self.root.bind("<Left>", lambda e: self.move_player("w")); self.root.bind("<Right>", lambda e: self.move_player("o"))
        self.root.bind("<h>", lambda e: self.use_potion("heiltrank")); self.root.bind("<m>", lambda e: self.use_potion("manatrank"))
        map_frame = tk.Frame(self.root, bg=BG_COLOR); map_frame.grid(row=0, column=0, padx=10, pady=10, rowspan=3)
        info_frame = tk.Frame(self.root, bg=BG_COLOR, bd=2, relief="sunken"); info_frame.grid(row=0, column=1, padx=10, pady=10, sticky="ns")
        self.stat_upgrade_frame = tk.Frame(self.root, bg=BG_COLOR); self.stat_upgrade_frame.grid(row=1, column=1, padx=10, pady=0, sticky="nsew")
        self.action_frame = tk.Frame(self.root, bg=BG_COLOR, bd=2, relief="sunken"); self.action_frame.grid(row=2, column=1, padx=10, pady=10, sticky="nsew")
        self.map_canvas = tk.Canvas(map_frame, width=MAP_SIZE * CELL_SIZE, height=MAP_SIZE * CELL_SIZE, bg="black", highlightthickness=0); self.map_canvas.pack()
        self.log_text = tk.Text(self.action_frame, height=15, width=55, bg="#111", fg=TEXT_COLOR, state="disabled", font=FONT_NORMAL, wrap="word", bd=0, highlightthickness=0)
        self.log_text.pack(side="top", padx=5, pady=5, expand=True, fill="both")
        self.button_frame = tk.Frame(self.action_frame, bg="#111"); self.button_frame.pack(side="bottom", fill="x")
        self.floor_label = tk.Label(info_frame, text="", font=FONT_BOLD, bg=BG_COLOR, fg=COLOR_STAIRS); self.floor_label.pack(padx=5, pady=5, anchor="w")
        self.status_text = tk.StringVar(); self.status_label = tk.Label(info_frame, textvariable=self.status_text, font=FONT_NORMAL, bg=BG_COLOR, fg=TEXT_COLOR, justify="left"); self.status_label.pack(padx=5, pady=5, anchor="w")
        self.equipment_text = tk.StringVar(); self.equipment_label = tk.Label(info_frame, textvariable=self.equipment_text, font=FONT_NORMAL, bg=BG_COLOR, fg=TEXT_COLOR, justify="left"); self.equipment_label.pack(padx=5, pady=5, anchor="w")
        xp_frame = tk.Frame(info_frame, bg=BG_COLOR); xp_frame.pack(fill="x", padx=5, pady=5)
        xp_label = tk.Label(xp_frame, text="XP:", font=FONT_NORMAL, bg=BG_COLOR, fg=TEXT_COLOR); xp_label.pack(side="left")
        self.xp_bar_canvas = tk.Canvas(xp_frame, width=150, height=15, bg="#444", highlightthickness=0); self.xp_bar_canvas.pack(side="left", padx=5)

    def log(self, message, color=TEXT_COLOR):
        self.log_text.config(state="normal"); self.log_text.tag_configure(color, foreground=color)
        self.log_text.insert(tk.END, message + "\n", color); self.log_text.see(tk.END); self.log_text.config(state="disabled")

    def clear_buttons(self):
        for widget in self.button_frame.winfo_children(): widget.destroy()

    def update_status_display(self):
        if not self.player: return
        self.floor_label.config(text=f"--- Etage {self.current_floor} ---")
        status = (f"Level: {self.player.level} ({self.player.name})\nLeben: {self.player.leben} / {self.player.max_leben}\nMana: {self.player.mana} / {self.player.max_mana}\n\n"
                  f"Stärke: {self.player.staerke}\nGeschick: {self.player.geschick}\nIntelligenz: {self.player.intelligenz}\n\n"
                  f"Angriff: {self.player.get_total_schaden()}\nVerteidigung: {self.player.get_total_verteidigung()}\n"
                  f"Krit. Chance: {self.player.get_crit_chance()*100:.1f}%\nAusweichchance: {self.player.get_dodge_chance()*100:.1f}%\n\n"
                  f"Gold: {self.player.gold}\nHeiltränke (H): {self.player.heiltränke}\nManatränke (M): {self.player.manatränke}")
        self.status_text.set(status)
        weapon = self.player.equipment.get("weapon"); armor = self.player.equipment.get("armor")
        w_name = weapon['name'] if weapon else "Hände"; a_name = armor['name'] if armor else "Kleidung"
        eq_text = f"\n-- Ausrüstung --\nWaffe: {w_name}\nRüstung: {a_name}"
        self.equipment_text.set(eq_text)
        self.update_xp_bar(); self.update_stat_upgrade_ui(); self.draw_map()

    def update_xp_bar(self):
        self.xp_bar_canvas.delete("all")
        xp_percentage = self.player.xp / self.player.xp_to_next_level
        bar_width = int(150 * xp_percentage)
        self.xp_bar_canvas.create_rectangle(0, 0, bar_width, 15, fill=XP_BAR_COLOR, outline="")
        self.xp_bar_canvas.create_text(75, 8, text=f"{self.player.xp} / {self.player.xp_to_next_level}", font=("Consolas", 8), fill="white")
    
    def update_stat_upgrade_ui(self):
        for widget in self.stat_upgrade_frame.winfo_children(): widget.destroy()
        if self.player and self.player.stat_points > 0:
            lbl = tk.Label(self.stat_upgrade_frame, text=f"Punkte zum Verteilen: {self.player.stat_points}", font=FONT_BOLD, bg=BG_COLOR, fg="#ffcc00"); lbl.pack()
            btn_str = tk.Button(self.stat_upgrade_frame, text="[+] Stärke", command=lambda: self.upgrade_stat("staerke"), bg="#555", fg=TEXT_COLOR); btn_str.pack(fill="x", padx=5)
            btn_dex = tk.Button(self.stat_upgrade_frame, text="[+] Geschick", command=lambda: self.upgrade_stat("geschick"), bg="#555", fg=TEXT_COLOR); btn_dex.pack(fill="x", padx=5)
            btn_int = tk.Button(self.stat_upgrade_frame, text="[+] Intelligenz", command=lambda: self.upgrade_stat("intelligenz"), bg="#555", fg=TEXT_COLOR); btn_int.pack(fill="x", padx=5)
    
    def upgrade_stat(self, stat_name):
        if self.player.stat_points > 0:
            setattr(self.player, stat_name, getattr(self.player, stat_name) + 1)
            self.player.stat_points -= 1
            self.log(f"{stat_name.capitalize()} wurde auf {getattr(self.player, stat_name)} erhöht!", "#ffcc00"); self.update_status_display()

    def draw_map(self):
        self.map_canvas.delete("all")
        px, py = self.player.position
        for y in range(MAP_SIZE):
            for x in range(MAP_SIZE):
                key = f"{x},{y}"; fill_color = COLOR_UNSEEN
                if key in self.dungeon_map and self.dungeon_map[key].get("besucht"):
                    event = self.dungeon_map[key].get("event")
                    if event == "boss": fill_color = COLOR_BOSS
                    elif event == "merchant": fill_color = COLOR_MERCHANT
                    elif event == "stairs": fill_color = COLOR_STAIRS
                    elif event == "shrine": fill_color = COLOR_SHRINE
                    else: fill_color = COLOR_SEEN
                self.map_canvas.create_rectangle(x * CELL_SIZE, y * CELL_SIZE, (x + 1) * CELL_SIZE, (y + 1) * CELL_SIZE, fill=fill_color, outline="#777")
        self.map_canvas.create_oval(px * CELL_SIZE + 5, py * CELL_SIZE + 5, (px + 1) * CELL_SIZE - 5, (py + 1) * CELL_SIZE - 5, fill=COLOR_PLAYER, outline="white")

    def generate_dungeon(self):
        self.dungeon_map = {}
        start_pos_key = f"{self.player.position[0]},{self.player.position[1]}"
        possible_coords = [(x, y) for x in range(MAP_SIZE) for y in range(MAP_SIZE) if f"{x},{y}" != start_pos_key]
        random.shuffle(possible_coords)
        target_key = f"{possible_coords.pop()[0]},{possible_coords.pop()[1]}"
        merchant_key = f"{possible_coords.pop()[0]},{possible_coords.pop()[1]}"
        shrine_key = ""
        if self.current_floor != BOSS_FLOOR: shrine_key = f"{possible_coords.pop()[0]},{possible_coords.pop()[1]}"
        for y in range(MAP_SIZE):
            for x in range(MAP_SIZE):
                key = f"{x},{y}"
                if key == target_key: event = "boss" if self.current_floor == BOSS_FLOOR else "stairs"
                elif key == merchant_key: event = "merchant"
                elif key == shrine_key: event = "shrine"
                elif key == start_pos_key: event = "leer"
                else: event = random.choices(["gegner", "truhe", "leer"], weights=[0.55, 0.1, 0.35], k=1)[0]
                self.dungeon_map[key] = {"besucht": False, "event": event}

    def start_character_selection(self):
        self.game_state = "char_selection"; self.clear_buttons()
        self.log_text.config(state="normal"); self.log_text.delete(1.0, tk.END)
        self.log("Willkommen! Wähle deine Klasse, um eine Vorschau zu sehen.", "#aaaaaa")
        self.log_text.config(state="disabled")
        class_list_frame = tk.Frame(self.button_frame, bg="#111"); class_list_frame.pack(side="left", fill="y", padx=5)
        self.preview_frame = tk.Frame(self.button_frame, bg="#111"); self.preview_frame.pack(side="right", expand=True, fill="both", padx=5)
        for char_key, char_val in CHARAKTER_VORLAGEN.items():
            btn = tk.Button(class_list_frame, text=char_val["name"], bg="#555", fg=TEXT_COLOR, command=lambda k=char_key: self.preview_character(k))
            btn.pack(fill="x", pady=2)
        if os.path.exists("savegame.json"):
            load_btn = tk.Button(class_list_frame, text="Spielstand laden", bg="#007acc", fg=TEXT_COLOR, command=self.load_game)
            load_btn.pack(fill="x", pady=10)

    def preview_character(self, char_key):
        self.selected_char_preview = char_key
        for widget in self.preview_frame.winfo_children(): widget.destroy()
        template = CHARAKTER_VORLAGEN[char_key]
        tk.Label(self.preview_frame, text=template['name'], font=FONT_BOLD, bg="#111", fg=COLOR_RARE_ITEM).pack(anchor="w")
        tk.Label(self.preview_frame, text=template['beschreibung'], font=FONT_NORMAL, bg="#111", fg=TEXT_COLOR, justify="left", wraplength=250).pack(anchor="w", pady=5)
        stats = (f"Leben: {template['max_leben']} | Mana: {template['max_mana']}\n"
                 f"Stärke: {template['staerke']} | Geschick: {template['geschick']} | Intelligenz: {template['intelligenz']}")
        tk.Label(self.preview_frame, text=stats, font=FONT_NORMAL, bg="#111", fg=TEXT_COLOR, justify="left").pack(anchor="w", pady=5)
        skill = template['skills'][0]
        skill_text = f"Startfähigkeit: {skill['name']} ({skill['cost']} Mana)"
        tk.Label(self.preview_frame, text=skill_text, font=FONT_NORMAL, bg="#111", fg=TEXT_COLOR, justify="left").pack(anchor="w")
        confirm_btn = tk.Button(self.preview_frame, text=f"{template['name']} wählen", bg="#00ff00", fg="black", command=self.select_character)
        confirm_btn.pack(pady=10)

    def select_character(self):
        self.player = Player(CHARAKTER_VORLAGEN[self.selected_char_preview])
        self.log_text.config(state="normal"); self.log_text.delete(1.0, tk.END); self.log_text.config(state="disabled")
        self.log(f"Du hast den {self.player.name} gewählt. Möge das Schicksal dir gnädig sein!", "#3399ff")
        self.start_new_floor()
        
    def start_new_floor(self):
        self.player.position = [MAP_SIZE // 2, MAP_SIZE // 2]; self.generate_dungeon(); self.start_exploring()
        self.enter_room(self.player.position[0], self.player.position[1], is_new_floor=True)

    def start_exploring(self):
        self.game_state = "exploring"; self.clear_buttons()
        save_btn = tk.Button(self.button_frame, text="Spiel speichern", command=self.save_game, bg="#007acc", fg=TEXT_COLOR); save_btn.pack(fill="x", padx=5, pady=5)
        self.log("Du erkundest die Etage. Was wird dich erwarten?", "#aaaaaa"); self.update_status_display()
        if self.player.skill_learn_points > 0: self.learn_new_skill()

    def learn_new_skill(self):
        self.log("Fähigkeiten-Lernen noch nicht implementiert.", "#aaaaaa")
        self.player.skill_learn_points = 0
        self.start_exploring()

    def move_player(self, direction):
        if self.game_state not in ["exploring"]: return
        self.process_player_turn_effects() 
        if self.player.leben <= 0: self.game_over(); return
        dx, dy = 0, 0
        if direction == "n": dy = -1
        elif direction == "s": dy = 1
        elif direction == "w": dx = -1
        elif direction == "o": dx = 1
        new_x, new_y = self.player.position[0] + dx, self.player.position[1] + dy
        if 0 <= new_x < MAP_SIZE and 0 <= new_y < MAP_SIZE:
            self.player.position = [new_x, new_y]; self.enter_room(new_x, new_y)
        else: self.log("Du stehst vor einer massiven Wand.", "#aaaaaa")

    def enter_room(self, x, y, is_new_floor=False):
        key = f"{x},{y}"; room = self.dungeon_map[key]
        if is_new_floor: self.log(f"Du betrittst Etage {self.current_floor}. Die Schatten werden tiefer.", "#3399ff")
        if not room["besucht"]:
            room["besucht"] = True; event = room["event"]
            if event == "gegner": self.start_combat(random.choice(GEGNER_LISTE))
            elif event == "boss": self.start_combat(BOSS_GEGNER, is_boss=True)
            elif event == "stairs": self.enter_stairs_room()
            elif event == "truhe": self.find_treasure(); room["event"] = "leer"
            elif event == "shrine": self.enter_shrine()
            elif event == "merchant": self.enter_merchant()
            else: self.log("Dieser Raum ist leer und still.", "#aaaaaa")
        else:
            self.log("Du warst schon einmal hier.", "#aaaaaa")
            if room["event"] == "stairs": self.enter_stairs_room()
            elif room["event"] == "merchant": self.enter_merchant()
            elif room["event"] == "shrine": self.log("Der Schrein hat seine Macht verloren.", COLOR_SHRINE)
        self.update_status_display()
    
    def enter_stairs_room(self):
        self.game_state = "stairs"; self.clear_buttons()
        self.log("Du hast eine Treppe gefunden, die tiefer in den Abgrund führt.", COLOR_STAIRS)
        descend_btn = tk.Button(self.button_frame, text=f"Abstieg zu Etage {self.current_floor + 1}", command=self.descend_floor, bg=COLOR_STAIRS, fg="black"); descend_btn.pack(fill="x", padx=5, pady=5)
        leave_btn = tk.Button(self.button_frame, text="Noch nicht...", command=self.start_exploring, bg="#aaa", fg="black"); leave_btn.pack(fill="x", padx=5, pady=5)
    
    def descend_floor(self): self.current_floor += 1; self.start_new_floor()

    def find_treasure(self):
        gold_found = random.randint(10, 30) * self.current_floor
        self.player.gold += gold_found; self.log(f"🧰 Du findest eine Truhe und nimmst {gold_found} Gold an dich!", "#ffff00")
        if random.random() < 0.25:
            loot_table = WEAPONS + ARMORS; item = random.choice(loot_table)
            self.handle_new_item(item)
        elif random.random() < 0.5:
            trank_typ = random.choice(["Heiltrank", "Manatrank"])
            if trank_typ == "Heiltrank": self.player.heiltränke += 1
            else: self.player.manatränke += 1
            self.log(f"Außerdem findest du einen {trank_typ}!", "#ffff00")
            
    def handle_new_item(self, item):
        color = {"common": TEXT_COLOR, "rare": COLOR_RARE_ITEM, "epic": COLOR_EPIC_ITEM, "legendary": COLOR_LEGENDARY_ITEM}.get(item['seltenheit'], TEXT_COLOR)
        self.log(f"Du hast gefunden: {item['name']}!", color)
        item_type = "weapon" if "schaden" in item else "armor"
        current_item = self.player.equipment.get(item_type)
        if not current_item or (item_type == "weapon" and item['schaden'] > current_item['schaden']) or \
           (item_type == "armor" and item['verteidigung'] > current_item['verteidigung']):
            old_item = self.player.equip(item)
            self.log(f"{item['name']} wurde ausgerüstet.", "#00ff00")
            if old_item: self.log(f"{old_item['name']} wurde ins Inventar gelegt (ersetzt).", "#aaaaaa")
        else:
            self.log(f"Dein aktuelles Item ist besser. {item['name']} wird ignoriert.", "#aaaaaa")

    def enter_shrine(self):
        self.game_state = "shrine"; self.clear_buttons()
        self.log("Du findest einen alten, pulsierenden Schrein. Eine unbekannte Macht geht von ihm aus.", COLOR_SHRINE)
        pray_btn = tk.Button(self.button_frame, text="Am Schrein beten", command=self.pray_at_shrine, bg=COLOR_SHRINE, fg="black"); pray_btn.pack(fill="x", padx=5, pady=5)
        leave_btn = tk.Button(self.button_frame, text="Den Schrein ignorieren", command=self.start_exploring, bg="#aaa", fg="black"); leave_btn.pack(fill="x", padx=5, pady=5)

    def pray_at_shrine(self):
        self.dungeon_map[f"{self.player.position[0]},{self.player.position[1]}"]["event"] = "leer"
        outcomes = ["heal", "stat_boost", "curse", "nothing"]
        outcome = random.choices(outcomes, weights=[0.4, 0.2, 0.2, 0.2], k=1)[0]
        if outcome == "heal":
            self.player.leben = self.player.max_leben; self.player.mana = self.player.max_mana
            self.log("Eine Welle heilender Energie durchströmt dich! Leben und Mana sind voll!", "#00ff00")
        elif outcome == "stat_boost":
            stat = random.choice(["staerke", "geschick", "intelligenz"])
            setattr(self.player, stat, getattr(self.player, stat) + 1)
            self.log(f"Du spürst neue Kraft! Deine {stat.capitalize()} wurde permanent um 1 erhöht!", "#ffcc00")
        elif outcome == "curse":
            self.player.leben = max(1, self.player.leben - 10)
            self.log("Der Schrein leuchtet dunkelrot! Du verlierst 10 Leben!", "#ff4444")
        else:
            self.log("Du betest, aber nichts geschieht.", "#aaaaaa")
        self.root.after(1500, self.start_exploring)

    def enter_merchant(self):
        self.game_state = "merchant"; self.clear_buttons(); self.log("Ein Händler bietet dir seine Waren an:", COLOR_MERCHANT)
        buy_hp_btn = tk.Button(self.button_frame, text=f"Heiltrank kaufen ({ITEMS['heiltrank']['preis']} G)", command=lambda: self.buy_item("heiltrank"), bg="#2ca02c", fg="white"); buy_hp_btn.pack(fill="x", padx=5, pady=2)
        buy_mp_btn = tk.Button(self.button_frame, text=f"Manatrank kaufen ({ITEMS['manatrank']['preis']} G)", command=lambda: self.buy_item("manatrank"), bg="#007acc", fg="white"); buy_mp_btn.pack(fill="x", padx=5, pady=2)
        leave_btn = tk.Button(self.button_frame, text="Händler verlassen", command=self.start_exploring, bg="#aaa", fg="black"); leave_btn.pack(fill="x", padx=5, pady=10)

    def buy_item(self, item_name):
        preis = ITEMS[item_name]['preis']
        if self.player.gold >= preis:
            self.player.gold -= preis
            if item_name == "heiltrank": self.player.heiltränke += 1
            else: self.player.manatränke += 1
            self.log(f"Du hast einen {item_name.replace('_', ' ')} gekauft.", COLOR_MERCHANT); self.update_status_display()
        else:
            self.log("Du hast nicht genug Gold!", "#ff4444")

    def use_potion(self, potion_type):
        if self.game_state not in ["exploring", "combat"]: return
        int_bonus_factor = 1 + (self.player.intelligenz / 20.0) 
        if potion_type == "heiltrank" and self.player.heiltränke > 0:
            if self.player.leben < self.player.max_leben:
                base_heal = ITEMS['heiltrank']['leben']
                total_heal = int(base_heal * int_bonus_factor)
                self.player.heiltränke -= 1
                self.player.leben = min(self.player.max_leben, self.player.leben + total_heal)
                self.log(f"Heiltrank benutzt. Leben +{total_heal}. ({self.player.leben}/{self.player.max_leben})", "#2ca02c")
                self.update_status_display()
            else: self.log("Dein Leben ist bereits voll.", "#aaaaaa")
        elif potion_type == "manatrank" and self.player.manatränke > 0:
            if self.player.mana < self.player.max_mana:
                base_mana = ITEMS['manatrank']['mana']
                total_mana = int(base_mana * int_bonus_factor)
                self.player.manatränke -= 1
                self.player.mana = min(self.player.max_mana, self.player.mana + total_mana)
                self.log(f"Manatrank benutzt. Mana +{total_mana}. ({self.player.mana}/{self.player.max_mana})", "#3399ff")
                self.update_status_display()
            else: self.log("Dein Mana ist bereits voll.", "#aaaaaa")

    def start_combat(self, gegner_template, is_boss=False):
        self.game_state = "combat"; self.current_gegner = gegner_template.copy()
        scaling_factor = 1 + (self.current_floor - 1) * 0.25
        self.current_gegner["leben"] = int(self.current_gegner["leben"] * scaling_factor)
        self.current_gegner["staerke"] = int(self.current_gegner["staerke"] * scaling_factor)
        self.current_gegner["xp"] = int(self.current_gegner["xp"] * scaling_factor)
        self.current_gegner["gold"] = int(self.current_gegner["gold"] * scaling_factor)
        self.log(f"\n⚔️ Du triffst auf einen {self.current_gegner['name']}! ⚔️", "#ff4444"); self.update_status_display(); self.setup_combat_buttons()

    def setup_combat_buttons(self):
        self.clear_buttons(); self.log(f"Gegner: {self.current_gegner['name']} | Leben: {self.current_gegner['leben']}", "#ff4444")
        attack_btn = tk.Button(self.button_frame, text="Angriff", command=self.player_attack, bg="#cc2222", fg="white"); attack_btn.pack(fill="x", padx=5, pady=2)
        for skill in self.player.skills:
            btn = tk.Button(self.button_frame, text=f"{skill['name']} ({skill['cost']} Mana)", bg="#9933ff", fg="white", command=lambda s=skill: self.player_special_attack(s)); btn.pack(fill="x", padx=5, pady=2)
        flee_btn = tk.Button(self.button_frame, text="Fliehen", command=self.flee_combat, bg="#aaa", fg="black"); flee_btn.pack(fill="x", padx=5, pady=10)

    def process_player_turn_effects(self):
        effects_to_remove = []
        for key, effect in list(self.player.status_effects.items()):
            if key == "poison":
                damage = effect['damage']
                self.player.leben -= damage
                self.log(f"Du erleidest {damage} Giftschaden.", "#00ff00")
            effect['duration'] -= 1
            if effect['duration'] <= 0:
                effects_to_remove.append(key)
                self.log(f"Der Effekt '{key}' ist abgeklungen.", "#aaaaaa")
        for key in effects_to_remove:
            if key in self.player.status_effects: del self.player.status_effects[key]
        self.update_status_display()

    def inflict_damage_to_enemy(self, damage, attack_type, is_crit=False):
        if damage > 0:
            if is_crit:
                damage = int(damage * 1.5)
                self.log(f"KRITISCHER TREFFER! Du verursachst {damage} Schaden!", COLOR_CRIT)
            else:
                if attack_type == "normal": self.log(f"Du greifst an und verursachst {damage} Schaden.")
                else: self.log(f"Dein Skill verursacht {damage} Schaden.")
            self.current_gegner["leben"] -= damage
        elif attack_type != "normal": self.log("Dein Skill hatte keinen direkten Schadenseffekt.")
        self.check_combat_status()

    def player_attack(self):
        self.process_player_turn_effects();
        if self.player.leben <= 0: self.game_over(); return
        base_damage = self.player.get_total_schaden()
        schaden = random.randint(base_damage // 2, base_damage)
        is_crit = random.random() < self.player.get_crit_chance()
        self.inflict_damage_to_enemy(schaden, "normal", is_crit)

    def player_special_attack(self, skill):
        self.process_player_turn_effects()
        if self.player.leben <= 0: self.game_over(); return
        if self.player.mana >= skill["cost"]:
            self.player.mana -= skill["cost"]; self.log(f"Du setzt '{skill['name']}' ein!", "#9933ff")
            if "heal_amount" in skill:
                heal_bonus = self.player.intelligenz // 2
                total_heal = skill['heal_amount'] + heal_bonus
                self.player.leben = min(self.player.max_leben, self.player.leben + total_heal)
                self.log(f"Du heilst dich um {total_heal} Leben.", "#00ff00")
                self.check_combat_status()
                return
            damage = 0
            if skill.get("damage_multiplier"):
                if skill['type'] == 'str': base = self.player.staerke
                elif skill['type'] == 'dex': base = self.player.geschick
                else: base = self.player.intelligenz
                hits = skill.get("hits", 1)
                for _ in range(hits): damage += int(random.randint(base // 2, base) * skill["damage_multiplier"])
            crit_chance = self.player.get_crit_chance() + skill.get("crit_chance_bonus", 0)
            is_crit = random.random() < crit_chance
            self.inflict_damage_to_enemy(damage, "skill", is_crit)
        else: self.log("Nicht genug Mana!", "#ff4444")
        
    def check_combat_status(self):
        if self.current_gegner["leben"] <= 0: self.win_combat()
        else: self.root.after(500, self.enemy_attack)

    def enemy_attack(self):
        if not self.current_gegner: return
        if random.random() < self.player.get_dodge_chance():
            self.log(f"Du weichst dem Angriff des {self.current_gegner['name']} geschickt aus!", COLOR_DODGE)
            self.root.after(500, self.setup_combat_buttons)
            return
        special = self.current_gegner.get("special")
        if special and random.random() < special["chance"]:
            self.log(f"Der {self.current_gegner['name']} setzt seine Spezialfähigkeit ein!", "#ff9900")
            if special['type'] == 'heal':
                self.current_gegner['leben'] += special['amount']
                self.log(f"Er heilt sich um {special['amount']} Leben.", "#00ff00")
            elif special['type'] == 'poison':
                self.apply_effect(self.player, special)
                self.log(f"Du wurdest vergiftet!", "#00ff00")
            elif special['type'] == 'armor_break':
                self.apply_effect(self.player, special)
                self.log("Deine Rüstung wurde geschwächt!", "#ff4444")
            elif special['type'] == 'fire_breath':
                schaden = special['damage'] - self.player.get_total_verteidigung()
                schaden = max(1, schaden)
                self.player.leben -= schaden
                self.log(f"Der Feueratem fügt dir {schaden} Schaden zu!", "#ff4444")
        else:
            schaden = self.current_gegner["staerke"] - self.player.get_total_verteidigung()
            schaden = max(1, random.randint(schaden // 2, schaden))
            self.player.leben -= schaden
            self.log(f"Der {self.current_gegner['name']} greift an und fügt dir {schaden} Schaden zu.", "#ff4444")
        self.update_status_display()
        if self.player.leben <= 0: self.game_over()
        else: self.setup_combat_buttons()

    def apply_effect(self, target, effect_data):
        effect_copy = effect_data.copy()
        if isinstance(target, Player):
            target.status_effects[effect_copy['type']] = effect_copy
            
    def win_combat(self):
        gold_reward = self.current_gegner["gold"]; xp_reward = self.current_gegner["xp"]
        self.player.gold += gold_reward
        self.log(f"Du hast den {self.current_gegner['name']} besiegt!", "#00ff00")
        self.log(f"Du erhältst {gold_reward} Gold.", "#00ff00")
        base_xp, bonus_xp, level_up = self.player.gain_xp(xp_reward)
        log_msg = f"Du erhältst {base_xp} XP"
        if bonus_xp > 0: log_msg += f" (+{bonus_xp} Intelligenz-Bonus!)"
        self.log(log_msg, "#ffff00")
        self.dungeon_map[f"{self.player.position[0]},{self.player.position[1]}"]["event"] = "leer"
        if "Drache" in self.current_gegner["name"]: self.victory(); return
        self.current_gegner = None
        if level_up:
            self.log(f"LEVEL UP! Du hast Level {self.player.level} erreicht!", COLOR_LEGENDARY_ITEM)
            self.root.after(1000, self.start_exploring)
        else: self.start_exploring()

    def victory(self):
        self.game_state = "game_over"; self.clear_buttons(); self.log("\n🎉 SIEG! 🎉", "#ffcc00")
        self.log(f"Du hast den mächtigen {BOSS_GEGNER['name']} besiegt!", "#ffcc00")
        messagebox.showinfo("Sieg!", "Herzlichen Glückwunsch! Du hast das Spiel gewonnen!")
        self.root.quit()

    def game_over(self):
        self.game_state = "game_over"; self.clear_buttons(); self.log("\n☠️ GAME OVER ☠️", "#ff0000")
        messagebox.showerror("Game Over", "Deine Reise endet hier. Das Spiel wird beendet.")
        self.root.quit()
        
    def save_game(self):
        if not self.player: return
        game_state = {"player": self.player.to_dict(), "dungeon_map": self.dungeon_map, "current_floor": self.current_floor}
        try:
            with open("savegame.json", "w") as f: json.dump(game_state, f, indent=4)
            self.log("Spiel erfolgreich gespeichert!", "#007acc")
        except Exception as e: messagebox.showerror("Fehler", f"Spiel konnte nicht gespeichert werden: {e}")

    def load_game(self):
        try:
            with open("savegame.json", "r") as f: game_state = json.load(f)
            self.player = Player.from_dict(game_state["player"])
            self.dungeon_map, self.current_floor = game_state["dungeon_map"], game_state["current_floor"]
            self.clear_buttons()
            self.log_text.config(state="normal"); self.log_text.delete(1.0, tk.END); self.log_text.config(state="disabled")
            self.log("Spielstand erfolgreich geladen!", "#007acc"); self.start_exploring()
            self.log(f"Willkommen zurück auf Etage {self.current_floor}.", "#3399ff")
        except Exception as e:
            messagebox.showerror("Fehler", f"Konnte Spielstand nicht laden: {e}"); self.start_character_selection()

if __name__ == "__main__":
    root = tk.Tk()
    game = Game(root)
    root.mainloop()