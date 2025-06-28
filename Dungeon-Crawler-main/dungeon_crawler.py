import tkinter as tk
from tkinter import messagebox, font
import random
import json
import os

# ============== KONSTANTEN UND DESIGN ==============
BG_COLOR = "#1e1e1e"
FRAME_COLOR = "#2d2d2d"
TEXT_COLOR = "#d4d4d4"
FONT_NORMAL = ("Consolas", 10)
FONT_BOLD = ("Consolas", 10, "bold")
FONT_BIG = ("Consolas", 12, "bold")
COLOR_SHRINE = "#c4b949"

COLOR_COMMON = "#ffffff"
COLOR_RARE = "#3399ff"
COLOR_EPIC = "#9933ff"
COLOR_LEGENDARY = "#ff9900"
COLOR_CRYSTAL = "#d42cca"

COLOR_CRIT = "#ff4444"
COLOR_DODGE = "#33ccff"
COLOR_STUN = "#ffff00"
COLOR_XP = "#9933ff"
COLOR_HEALTH = "#2ca02c"
COLOR_MANA = "#007acc"
COLOR_GOLD = "#ffcc00"

CELL_SIZE = 40
MAP_SIZE = 12
BOSS_FLOOR = 5

# ============== DATENBANKEN ==============
EQUIPMENT_DATABASE = {
    "weapon": [{"name": "Rostiger Dolch", "wert": 1, "seltenheit": "common"}, {"name": "Kurzschwert", "wert": 3, "seltenheit": "common"}, {"name": "Kriegsaxt", "wert": 5, "seltenheit": "rare"}, {"name": "Morgenstern", "wert": 6, "seltenheit": "rare"}, {"name": "Elfenklinge", "wert": 8, "seltenheit": "epic"}, {"name": "Dämonenschlächter", "wert": 10, "seltenheit": "epic"}, {"name": "Drachentöter-Großschwert", "wert": 14, "seltenheit": "legendary"}],
    "armor": [{"name": "Lederwams", "wert": 1, "seltenheit": "common"}, {"name": "Kettenhemd", "wert": 2, "seltenheit": "rare"}, {"name": "Plattenpanzer", "wert": 4, "seltenheit": "epic"}, {"name": "Obsidianrüstung", "wert": 6, "seltenheit": "legendary"}],
    "ring": [{"name": "Ring der Stärke", "bonus": "+1 Stärke", "seltenheit": "rare"}, {"name": "Ring des Geschicks", "bonus": "+1 Geschick", "seltenheit": "rare"}, {"name": "Ring der Vitalität", "bonus": "+5 max. Leben", "seltenheit": "epic"}],
    "amulet": [{"name": "Amulett der Macht", "bonus": "+1 alle Attribute", "seltenheit": "epic"}, {"name": "Amulett des Schutzes", "bonus": "+1 Verteidigung", "seltenheit": "rare"}, {"name": "Medaillon des Wissens", "bonus": "+5% XP-Gewinn", "seltenheit": "legendary"}]
}
SKILL_DATABASE = {
    "krieger": [{"id": "spalten", "name": "Spalten", "desc": "Ein Hieb, der 250% Waffenschaden verursacht.", "cost": 5, "damage_multiplier": 2.5, "type": "str", "level": 3}, {"id": "durchbrechen", "name": "Rüstungsbrecher", "desc": "Schwächt die Rüstung des Ziels für 3 Züge.", "cost": 4, "effect": {"type": "armor_break", "amount": 2, "duration": 3}, "type": "str", "level": 3}, {"id": "standhaft", "name": "Standhaftigkeit", "desc": "Erhöht die eigene Verteidigung für 3 Züge.", "cost": 8, "effect": {"type": "def_boost", "amount": 3, "duration": 3}, "type": "str", "level": 6}, {"id": "wirbelwind", "name": "Wirbelwind", "desc": "Trifft den Gegner dreimal mit 120% Schaden.", "cost": 10, "damage_multiplier": 1.2, "hits": 3, "type": "str", "level": 6}],
    "magier": [{"id": "eisstrahl", "name": "Eisstrahl", "desc": "Hat eine 50% Chance, das Ziel zu betäuben.", "cost": 6, "effect": {"type": "stun", "chance": 0.5, "duration": 1}, "type": "int", "level": 3}, {"id": "manaschild", "name": "Manaschild", "desc": "Eingehender Schaden wird vom Mana abgezogen.", "cost": 0, "effect": {"type": "mana_shield", "ratio": 2}, "level": 3}, {"id": "kettenblitz", "name": "Kettenblitz", "desc": "Trifft den Gegner dreimal mit 180% Schaden.", "cost": 12, "damage_multiplier": 1.8, "hits": 3, "type": "int", "level": 6}, {"id": "desintegration", "name": "Desintegration", "desc": "Ein extrem mächtiger Strahl (400% Schaden).", "cost": 15, "damage_multiplier": 4.0, "type": "int", "level": 6}],
    "dieb": [{"id": "giftklinge", "name": "Giftklinge", "desc": "Vergiftet das Ziel für 3 Runden.", "cost": 6, "effect": {"type": "poison", "damage": 4, "duration": 3}, "level": 3}, {"id": "ausweichrolle", "name": "Ausweichrolle", "desc": "Erhöht die Ausweichchance für 1 Runde massiv.", "cost": 5, "effect": {"type": "dodge_boost", "amount": 0.5, "duration": 1}, "level": 3}],
    "paladin": [{"id": "richturteil", "name": "Richturteil", "desc": "Verursacht extra Schaden basierend auf INT.", "cost": 4, "damage_multiplier": 1.5, "type": "int", "level": 3}, {"id": "schilddesglaubens", "name": "Schild des Glaubens", "desc": "Absorbiert den nächsten Angriff komplett.", "cost": 7, "effect": {"type": "invulnerable", "duration": 1}, "level": 3}],
    "waldläufer": [{"id": "schnellfeuer", "name": "Schnellfeuer", "desc": "Feuert 3 Pfeile mit normalem Schaden.", "cost": 6, "hits": 3, "type": "dex", "level": 3}, {"id": "fallelegen", "name": "Falle legen", "desc": "Legt eine Falle, die beim nächsten Angriff auslöst.", "cost": 5, "effect": {"type": "trap", "damage": 10}, "level": 3}],
}
CHARAKTER_VORLAGEN = {
    "krieger": { "name": "Krieger", "staerke": 8, "geschick": 4, "intelligenz": 3, "max_leben": 20, "max_mana": 10, "beschreibung": "Ein Meister des Nahkampfs. Verlässt sich auf pure Stärke und hohe Lebenskraft.", "skills": [{"id": "schlag", "name": "Mächtiger Schlag", "cost": 3, "damage_multiplier": 1.8, "type": "str"}]},
    "magier": { "name": "Magier", "staerke": 3, "geschick": 5, "intelligenz": 8, "max_leben": 12, "max_mana": 20, "beschreibung": "Ein Gelehrter der arkanen Künste. Verursacht enormen Schaden mit Zaubern.", "skills": [{"id": "feuerball", "name": "Feuerball", "cost": 5, "damage_multiplier": 2.0, "type": "int"}]},
    "dieb": { "name": "Dieb", "staerke": 5, "geschick": 8, "intelligenz": 4, "max_leben": 15, "max_mana": 15, "beschreibung": "Ein agiler Schatten, der schnell zuschlägt und kritischen Treffern ausweicht.", "skills": [{"id": "doppelstich", "name": "Doppelstich", "cost": 4, "damage_multiplier": 1.4, "type": "dex", "hits": 2}]},
    "paladin": { "name": "Paladin", "staerke": 7, "geschick": 3, "intelligenz": 5, "max_leben": 18, "max_mana": 12, "beschreibung": "Ein heiliger Verteidiger. Kombiniert solide Angriffe mit schützender und heilender Magie.", "skills": [{"id": "heiligeslicht", "name": "Heiliges Licht", "cost": 5, "heal_amount": 8, "type": "int"}]},
    "waldläufer": { "name": "Waldläufer", "staerke": 4, "geschick": 9, "intelligenz": 3, "max_leben": 16, "max_mana": 10, "beschreibung": "Ein Meister des Fernkampfs. Hohe Geschicklichkeit führt zu verheerenden kritischen Treffern.", "skills": [{"id": "zielschuss", "name": "Gezielter Schuss", "cost": 4, "damage_multiplier": 1.5, "crit_chance_bonus": 0.25, "type": "dex"}]}
}
GEGNER_LISTE = [
    {"name": "Skelett", "staerke": 4, "leben": 10, "gold": 5, "xp": 10}, {"name": "Goblin", "staerke": 3, "leben": 8, "gold": 3, "xp": 8},
    {"name": "Ork-Krieger", "staerke": 7, "leben": 15, "gold": 12, "xp": 18, "special": {"type": "stun", "chance": 0.2, "duration": 1}},
    {"name": "Giftspinne", "staerke": 4, "leben": 12, "gold": 8, "xp": 12, "special": {"type": "poison", "chance": 0.3, "damage": 2, "duration": 3}},
    {"name": "Goblin-Schamane", "staerke": 2, "leben": 18, "gold": 15, "xp": 20, "special": {"type": "heal", "chance": 0.4, "amount": 6}},
    {"name": "Höhlentroll", "staerke": 9, "leben": 25, "gold": 20, "xp": 25, "special": {"type": "armor_break", "chance": 0.2, "amount": 2, "duration": 3}},
]
BOSS_GEGNER = {"name": "Drachenfürst Malakor", "staerke": 15, "leben": 120, "gold": 250, "xp": 300, 
               "special": {"type": "fire_breath", "chance": 0.3, "damage": 20}, "kristalle": 5}
META_UPGRADES = {
    "start_gold": {"name": "Gefüllter Geldbeutel", "desc": "+25 Startgold pro Stufe.", "cost": 5, "bonus": 25, "max_level": 5},
    "start_potion": {"name": "Zusätzlicher Heiltrank", "desc": "+1 Start-Heiltrank pro Stufe.", "cost": 8, "bonus": 1, "max_level": 3},
    "xp_boost": {"name": "Segen des Lernens", "desc": "+5% Bonus-XP pro Stufe.", "cost": 10, "bonus": 0.05, "max_level": 4}
}
ITEMS = {"heiltrank": {"preis": 25, "leben": 15}, "manatrank": {"preis": 30, "mana": 10}}

# ============== HILFSKLASSEN ==============

class Tooltip:
    def __init__(self, widget, text):
        self.widget = widget; self.text = text; self.tooltip_window = None
        self.widget.bind("<Enter>", self.show_tooltip)
        self.widget.bind("<Leave>", self.hide_tooltip)

    def show_tooltip(self, event):
        x, y, _, _ = self.widget.bbox("insert")
        x += self.widget.winfo_rootx() + 25
        y += self.widget.winfo_rooty() + 25
        self.tooltip_window = tk.Toplevel(self.widget)
        self.tooltip_window.wm_overrideredirect(True)
        self.tooltip_window.wm_geometry(f"+{x}+{y}")
        label = tk.Label(self.tooltip_window, text=self.text, justify='left', background="#333333", foreground=TEXT_COLOR, relief='solid', borderwidth=1, font=FONT_NORMAL, wraplength=200)
        label.pack(ipadx=1)

    def hide_tooltip(self, event):
        if self.tooltip_window: self.tooltip_window.destroy()
        self.tooltip_window = None

# ============== SPIEL-KLASSEN ==============

class Player:
    def __init__(self, template, meta_bonuses):
        self.char_type = template["name"].lower()
        self.name = template["name"]
        self.base_stats = {'staerke': template["staerke"], 'geschick': template["geschick"], 'intelligenz': template["intelligenz"], 'max_leben': template["max_leben"], 'max_mana': template["max_mana"]}
        self.skills = list(template["skills"])
        self.gold = 25 + meta_bonuses.get("start_gold", 0)
        self.heiltränke = 2 + meta_bonuses.get("start_potion", 0)
        self.manatränke = 1
        self.position = [MAP_SIZE // 2, MAP_SIZE // 2]
        self.level = 1; self.xp = 0; self.xp_to_next_level = 80
        self.stat_points = 0; self.skill_points = 0
        self.inventory = [None] * 16
        self.equipment = {"weapon": None, "armor": None, "ring": None, "amulet": None}
        self.status_effects = {}
        self.xp_bonus_mod = meta_bonuses.get("xp_boost", 0.0)
        self.recalculate_stats()
        self.leben = self.max_leben; self.mana = self.max_mana

    def recalculate_stats(self):
        self.staerke = self.base_stats['staerke']; self.geschick = self.base_stats['geschick']; self.intelligenz = self.base_stats['intelligenz']
        self.max_leben = self.base_stats['max_leben']; self.max_mana = self.base_stats['max_mana']
        current_xp_bonus = self.xp_bonus_mod
        for item in self.equipment.values():
            if not item or "bonus" not in item: continue
            if "+1 Stärke" in item['bonus']: self.staerke += 1
            if "+1 Geschick" in item['bonus']: self.geschick += 1
            if "+1 Intelligenz" in item['bonus']: self.intelligenz +=1
            if "+5 max. Leben" in item['bonus']: self.max_leben += 5
            if "+1 alle Attribute" in item['bonus']: self.staerke += 1; self.geschick += 1; self.intelligenz += 1
            if "+5% XP-Gewinn" in item['bonus']: current_xp_bonus += 0.05
        self.effective_xp_mod = current_xp_bonus

    def get_total_schaden(self):
        weapon_bonus = self.equipment["weapon"]["wert"] if self.equipment["weapon"] else 0
        return self.staerke + weapon_bonus

    def get_total_verteidigung(self):
        armor_bonus = self.equipment["armor"]["wert"] if self.equipment["armor"] else 0
        amulet_bonus = 1 if self.equipment["amulet"] and "+1 Verteidigung" in self.equipment["amulet"]['bonus'] else 0
        debuff = self.status_effects.get("armor_break", {}).get("amount", 0)
        buff = self.status_effects.get("def_boost", {}).get("amount", 0)
        return armor_bonus + amulet_bonus - debuff + buff
    
    def get_crit_chance(self): return self.geschick * 0.015
    
    def get_dodge_chance(self):
        base_dodge = self.geschick * 0.0075
        boost = self.status_effects.get("dodge_boost", {}).get("amount", 0)
        return base_dodge + boost

    def add_to_inventory(self, item):
        for i, slot in enumerate(self.inventory):
            if slot is None: self.inventory[i] = item; return True
        return False

    def equip(self, item, slot_index):
        item_type = next((cat for cat, items in EQUIPMENT_DATABASE.items() if any(i['name'] == item['name'] for i in items)), None)
        if not item_type: return
        old_item = self.equipment.get(item_type)
        self.equipment[item_type] = item; self.inventory[slot_index] = old_item
        self.recalculate_stats()

    def gain_xp(self, amount):
        base_xp = amount
        bonus_xp = int(base_xp * (self.intelligenz * 0.01 + self.effective_xp_mod))
        total_xp = base_xp + bonus_xp; self.xp += total_xp
        level_up = False
        if self.xp >= self.xp_to_next_level: self.level_up(); level_up = True
        return base_xp, bonus_xp, level_up

    def level_up(self):
        self.level += 1; self.xp -= self.xp_to_next_level
        self.xp_to_next_level = int(self.xp_to_next_level * 1.6)
        self.base_stats['max_leben'] += 5; self.base_stats['max_mana'] += 3
        self.recalculate_stats(); self.leben = self.max_leben; self.mana = self.max_mana
        self.stat_points += 1
        if self.level > 1 and self.level % 3 == 0: self.skill_points += 1

    def to_dict(self): return {k: v for k, v in self.__dict__.items() if k not in ['base_stats', 'effective_xp_mod']}
    @classmethod
    def from_dict(cls, data, meta_bonuses):
        player = cls(CHARAKTER_VORLAGEN[data["char_type"]], meta_bonuses)
        player.__dict__.update(data); player.recalculate_stats(); return player

# ============== FENSTER-KLASSEN ==============

class InventoryWindow(tk.Toplevel):
    def __init__(self, parent, game):
        super().__init__(parent)
        self.game = game
        self.player = game.player
        self.configure(bg=BG_COLOR)
        self.title("Inventar & Ausrüstung")
        self.resizable(False, False)
        self.protocol("WM_DELETE_WINDOW", self.on_close)
        self.transient(parent)
        self.setup_ui()

    def setup_ui(self):
        main_frame = tk.Frame(self, bg=BG_COLOR, bd=5)
        main_frame.pack(fill="both", expand=True)

        eq_frame = tk.Frame(main_frame, bg=FRAME_COLOR, bd=2, relief="sunken")
        eq_frame.pack(side="left", fill="y", padx=5, pady=5)
        tk.Label(eq_frame, text="Ausrüstung", font=FONT_BOLD, bg=FRAME_COLOR, fg=TEXT_COLOR).pack(pady=5)

        self.eq_slots = {}
        for slot_name in ["weapon", "armor", "ring", "amulet"]:
            tk.Label(eq_frame, text=slot_name.capitalize(), font=FONT_NORMAL, bg=FRAME_COLOR, fg="#aaa").pack(anchor="w", padx=5)
            slot_label = tk.Label(eq_frame, text="Leer", width=20, height=2, bg=BG_COLOR, fg=TEXT_COLOR, relief="sunken")
            slot_label.pack(padx=5, pady=2)
            self.eq_slots[slot_name] = slot_label

        inv_frame = tk.Frame(main_frame, bg=FRAME_COLOR, bd=2, relief="sunken")
        inv_frame.pack(side="right", fill="both", expand=True, padx=5, pady=5)
        tk.Label(inv_frame, text="Rucksack", font=FONT_BOLD, bg=FRAME_COLOR, fg=TEXT_COLOR).pack(pady=5)
        
        self.inv_cells = []
        grid_frame = tk.Frame(inv_frame, bg=FRAME_COLOR)
        grid_frame.pack()
        for i in range(16):
            cell = tk.Label(grid_frame, text="", width=10, height=3, bg=BG_COLOR, fg=TEXT_COLOR, relief="sunken", wraplength=70)
            cell.grid(row=i//4, column=i%4, padx=2, pady=2)
            cell.bind("<Button-3>", lambda e, index=i: self.equip_item(index))
            self.inv_cells.append(cell)

        self.redraw()

    def redraw(self):
        # Ausrüstung aktualisieren
        for slot_name, label in self.eq_slots.items():
            item = self.player.equipment.get(slot_name)
            if item:
                color = self.get_rarity_color(item)
                label.config(text=item['name'], fg=color)
                Tooltip(label, self.get_item_tooltip(item))
            else:
                label.config(text="Leer", fg=TEXT_COLOR)
                if hasattr(label, 'tooltip'): label.tooltip.widget.unbind("<Enter>"); label.tooltip.widget.unbind("<Leave>")

        # Inventar aktualisieren
        for i, cell in enumerate(self.inv_cells):
            item = self.player.inventory[i]
            if item:
                color = self.get_rarity_color(item)
                cell.config(text=item['name'], fg=color)
                Tooltip(cell, self.get_item_tooltip(item) + "\n(Rechtsklick zum Ausrüsten)")
            else:
                cell.config(text="", fg=TEXT_COLOR)
                if hasattr(cell, 'tooltip'): cell.tooltip.widget.unbind("<Enter>"); cell.tooltip.widget.unbind("<Leave>")

    def get_item_tooltip(self, item):
        item_type = "Waffe" if "wert" in item else "Rüstung" if "verteidigung" in item else "Accessoire"
        text = f"{item['name']} ({item['seltenheit']})\n"
        if "wert" in item: text += f"Typ: {item_type}\nWert: {item['wert']}"
        if "bonus" in item: text += f"Bonus: {item['bonus']}"
        return text

    def get_rarity_color(self, item):
        return {"common": COLOR_COMMON, "rare": COLOR_RARE, "epic": COLOR_EPIC, "legendary": COLOR_LEGENDARY}.get(item['seltenheit'], TEXT_COLOR)

    def equip_item(self, index):
        item_to_equip = self.player.inventory[index]
        if item_to_equip:
            self.player.equip(item_to_equip, index)
            self.game.log(f"{item_to_equip['name']} ausgerüstet.", COLOR_HEALTH)
            self.redraw()
            self.game.update_status_display()
    
    def on_close(self):
        self.game.root.attributes('-disabled', False)
        self.destroy()

class SkillSelectionWindow(tk.Toplevel):
    def __init__(self, parent, game, choices):
        super().__init__(parent)
        self.game = game
        self.player = game.player
        self.choices = choices
        self.configure(bg=FRAME_COLOR)
        self.title("Fähigkeit wählen!")
        self.resizable(False, False)
        self.protocol("WM_DELETE_WINDOW", self.on_close)
        self.transient(parent)
        self.setup_ui()

    def setup_ui(self):
        tk.Label(self, text="LEVEL AUFSTIEG!", font=FONT_BIG, bg=FRAME_COLOR, fg=COLOR_LEGENDARY).pack(pady=10)
        tk.Label(self, text="Wähle eine neue Fähigkeit:", font=FONT_BOLD, bg=FRAME_COLOR, fg=TEXT_COLOR).pack(pady=5)
        for skill in self.choices:
            frame = tk.Frame(self, bg=BG_COLOR, bd=2, relief="sunken")
            frame.pack(padx=10, pady=5, fill="x")
            btn_text = f"{skill['name']} ({skill['cost']} Mana)"
            btn = tk.Button(frame, text=btn_text, command=lambda s=skill: self.choose_skill(s), bg=COLOR_EPIC, fg=TEXT_COLOR)
            btn.pack(pady=5)
            tk.Label(frame, text=skill['desc'], font=FONT_NORMAL, bg=BG_COLOR, fg="#ccc", wraplength=300).pack(pady=5)

    def choose_skill(self, skill):
        self.player.skills.append(skill)
        self.player.skill_points -= 1
        self.game.log(f"Fähigkeit '{skill['name']}' gelernt!", COLOR_LEGENDARY)
        self.on_close()

    def on_close(self):
        if self.player.skill_points > 0: self.player.skill_points = 0 # Verhindert Endlosschleife
        self.game.root.attributes('-disabled', False)
        self.game.start_exploring()
        self.destroy()

class MetaShopWindow(tk.Toplevel):
    def __init__(self, parent, game):
        super().__init__(parent)
        self.game = game
        self.configure(bg=BG_COLOR)
        self.title("Shop der Seelen")
        self.protocol("WM_DELETE_WINDOW", self.on_close)
        self.transient(parent)
        self.upgrades_frames = {}
        self.setup_ui()

    def setup_ui(self):
        main_frame = tk.Frame(self, bg=BG_COLOR)
        main_frame.pack(padx=10, pady=10)
        
        header_frame = tk.Frame(main_frame, bg=BG_COLOR)
        header_frame.pack(pady=5)
        tk.Label(header_frame, text="Shop der Seelen", font=FONT_BIG, bg=BG_COLOR, fg=COLOR_EPIC).pack()
        self.kristalle_label = tk.Label(header_frame, text=f"Abyssale Kristalle: {self.game.meta_progress.get('kristalle', 0)}", font=FONT_BOLD, bg=BG_COLOR, fg=COLOR_CRYSTAL)
        self.kristalle_label.pack()

        for key, upgrade in META_UPGRADES.items():
            frame = tk.Frame(main_frame, bg=FRAME_COLOR, bd=2, relief="groove")
            frame.pack(fill="x", pady=5)
            
            level = self.game.meta_progress.get("upgrades", {}).get(key, 0)
            
            info_label = tk.Label(frame, text=f"{upgrade['name']} [{level}/{upgrade['max_level']}]", font=FONT_BOLD, bg=FRAME_COLOR, fg=TEXT_COLOR)
            info_label.pack()
            desc_label = tk.Label(frame, text=upgrade['desc'], font=FONT_NORMAL, bg=FRAME_COLOR, fg="#aaa")
            desc_label.pack()
            
            cost = upgrade['cost'] * (level + 1)
            buy_btn = tk.Button(frame, text=f"Kaufen ({cost} Kristalle)", command=lambda k=key: self.buy_upgrade(k), bg="#555", fg=TEXT_COLOR)
            buy_btn.pack(pady=5)
            
            if level >= upgrade['max_level'] or self.game.meta_progress.get('kristalle', 0) < cost:
                buy_btn.config(state="disabled")

            self.upgrades_frames[key] = (info_label, buy_btn)

    def buy_upgrade(self, key):
        upgrades = self.game.meta_progress.setdefault("upgrades", {})
        level = upgrades.get(key, 0)
        upgrade_data = META_UPGRADES[key]
        cost = upgrade_data['cost'] * (level + 1)

        if level < upgrade_data['max_level'] and self.game.meta_progress['kristalle'] >= cost:
            self.game.meta_progress['kristalle'] -= cost
            upgrades[key] = level + 1
            self.game.save_meta_progress()
            self.redraw()

    def redraw(self):
        self.kristalle_label.config(text=f"Abyssale Kristalle: {self.game.meta_progress.get('kristalle', 0)}")
        for key, upgrade in META_UPGRADES.items():
            info_label, buy_btn = self.upgrades_frames[key]
            level = self.game.meta_progress.get("upgrades", {}).get(key, 0)
            info_label.config(text=f"{upgrade['name']} [{level}/{upgrade['max_level']}]")
            cost = upgrade['cost'] * (level + 1)
            buy_btn.config(text=f"Kaufen ({cost} Kristalle)")
            if level >= upgrade['max_level'] or self.game.meta_progress.get('kristalle', 0) < cost:
                buy_btn.config(state="disabled")
            else:
                buy_btn.config(state="normal")
                
    def on_close(self):
        self.game.root.attributes('-disabled', False)
        self.destroy()

# ============== HAUPTSPIEL-KLASSE ==============
# (Die Game-Klasse ist hier vollständig und enthält die gesamte Spiellogik)
class Game:
    def __init__(self, root):
        self.root = root; self.player = None; self.dungeon_map = {}; self.current_gegner = None
        self.game_state = "difficulty_selection"; self.current_floor = 1; self.selected_char_preview = None
        self.difficulty_mod = 1.0; self.difficulty = "Normal"
        self.meta_progress = self.load_meta_progress()
        self.setup_ui()
        self.start_difficulty_selection()

    def load_meta_progress(self):
        if os.path.exists("meta_save.json"):
            try:
                with open("meta_save.json", "r") as f: return json.load(f)
            except json.JSONDecodeError: return {"kristalle": 0, "upgrades": {}}
        return {"kristalle": 0, "upgrades": {}}

    def save_meta_progress(self):
        with open("meta_save.json", "w") as f: json.dump(self.meta_progress, f)

    def get_meta_bonuses(self):
        bonuses = {}; upgrades = self.meta_progress.get("upgrades", {})
        for key, level in upgrades.items():
            if key in META_UPGRADES: bonuses[key] = META_UPGRADES[key]['bonus'] * level
        return bonuses

    def setup_ui(self):
        self.root.title("Dungeon Crawler - Chroniken des Abgrunds")
        self.root.configure(bg=BG_COLOR)
        self.root.bind("<KeyPress-i>", self.open_inventory)
        self.root.bind("<Up>", lambda e: self.move_player("n")); self.root.bind("<Down>", lambda e: self.move_player("s"))
        self.root.bind("<Left>", lambda e: self.move_player("w")); self.root.bind("<Right>", lambda e: self.move_player("o"))
        self.root.bind("<h>", lambda e: self.use_potion("heiltrank")); self.root.bind("<m>", lambda e: self.use_potion("manatrank"))
        self.main_frame = tk.Frame(self.root, bg=BG_COLOR); self.main_frame.pack(fill="both", expand=True)
        self.map_frame = tk.Frame(self.main_frame, bg=BG_COLOR); self.map_frame.grid(row=0, column=0, padx=10, pady=10, rowspan=3, sticky="ns")
        self.info_frame = tk.Frame(self.main_frame, bg=FRAME_COLOR, bd=2, relief="sunken"); self.info_frame.grid(row=0, column=1, padx=10, pady=10, sticky="ns")
        self.stat_upgrade_frame = tk.Frame(self.main_frame, bg=BG_COLOR); self.stat_upgrade_frame.grid(row=1, column=1, padx=10, pady=0, sticky="nsew")
        self.action_frame = tk.Frame(self.main_frame, bg=FRAME_COLOR, bd=2, relief="sunken"); self.action_frame.grid(row=2, column=1, padx=10, pady=10, sticky="nsew")
        self.map_canvas = tk.Canvas(self.map_frame, width=MAP_SIZE * CELL_SIZE, height=MAP_SIZE * CELL_SIZE, bg="black", highlightthickness=0); self.map_canvas.pack()
        self.log_text = tk.Text(self.action_frame, height=15, width=55, bg="#111", fg=TEXT_COLOR, state="disabled", font=FONT_NORMAL, wrap="word", bd=0, highlightthickness=0)
        self.log_text.pack(side="top", padx=5, pady=5, expand=True, fill="both")
        self.button_frame = tk.Frame(self.action_frame, bg="#111"); self.button_frame.pack(side="bottom", fill="x", pady=5)

    def setup_game_ui(self):
        for widget in self.info_frame.winfo_children(): widget.destroy()
        self.floor_label = tk.Label(self.info_frame, text="", font=FONT_BIG, bg=FRAME_COLOR, fg=COLOR_LEGENDARY); self.floor_label.pack(padx=5, pady=5, anchor="w")
        self.status_text = tk.StringVar(); self.status_label = tk.Label(self.info_frame, textvariable=self.status_text, font=FONT_NORMAL, bg=FRAME_COLOR, fg=TEXT_COLOR, justify="left"); self.status_label.pack(padx=5, pady=5, anchor="w")
        self.equipment_text = tk.StringVar(); self.equipment_label = tk.Label(self.info_frame, textvariable=self.equipment_text, font=FONT_NORMAL, bg=FRAME_COLOR, fg=TEXT_COLOR, justify="left"); self.equipment_label.pack(padx=5, pady=5, anchor="w")
        xp_frame = tk.Frame(self.info_frame, bg=FRAME_COLOR); xp_frame.pack(fill="x", padx=5, pady=5)
        self.xp_bar_canvas = tk.Canvas(xp_frame, width=200, height=18, bg="#444", highlightthickness=0); self.xp_bar_canvas.pack(side="left", padx=5)
        inv_button = tk.Button(self.info_frame, text="Inventar (I)", command=self.open_inventory, bg="#555", fg=TEXT_COLOR); inv_button.pack(fill="x", padx=5, pady=10)

    def clear_all_frames(self):
        self.clear_buttons()
        for widget in self.info_frame.winfo_children(): widget.destroy()
        for widget in self.stat_upgrade_frame.winfo_children(): widget.destroy()
        self.map_canvas.delete("all")
        self.log_text.config(state="normal"); self.log_text.delete(1.0, tk.END); self.log_text.config(state="disabled")

    def log(self, message, color=TEXT_COLOR):
        self.log_text.config(state="normal"); self.log_text.tag_configure(color, foreground=color)
        self.log_text.insert(tk.END, message + "\n", color); self.log_text.see(tk.END); self.log_text.config(state="disabled")

    def clear_buttons(self):
        for widget in self.button_frame.winfo_children(): widget.destroy()

    def update_status_display(self):
        if not self.player: return
        self.floor_label.config(text=f"Etage {self.current_floor} ({self.difficulty})")
        status = (f"Lvl {self.player.level} {self.player.name}\n"
                  f"Leben: {self.player.leben} / {self.player.max_leben}\nMana: {self.player.mana} / {self.player.max_mana}\n\n"
                  f"STR: {self.player.staerke} | GES: {self.player.geschick} | INT: {self.player.intelligenz}\n\n"
                  f"Angriff: {self.player.get_total_schaden()}\nVerteidigung: {self.player.get_total_verteidigung()}\n"
                  f"Krit. Chance: {self.player.get_crit_chance()*100:.1f}%\nAusweichchance: {self.player.get_dodge_chance()*100:.1f}%\n\n"
                  f"Gold: {self.player.gold}\nHeiltränke (H): {self.player.heiltränke}\nManatränke (M): {self.player.manatränke}")
        self.status_text.set(status)
        weapon = self.player.equipment.get("weapon"); armor = self.player.equipment.get("armor"); ring = self.player.equipment.get("ring"); amulet = self.player.equipment.get("amulet")
        eq_text = (f"\n-- Ausrüstung --\nWaffe: {weapon['name'] if weapon else 'Leer'}\nRüstung: {armor['name'] if armor else 'Leer'}\n"
                   f"Ring: {ring['name'] if ring else 'Leer'}\nAmulett: {amulet['name'] if amulet else 'Leer'}")
        self.equipment_text.set(eq_text)
        self.update_xp_bar(); self.update_stat_upgrade_ui(); self.draw_map()

    def update_xp_bar(self):
        self.xp_bar_canvas.delete("all")
        if self.player.xp_to_next_level > 0 : xp_percentage = self.player.xp / self.player.xp_to_next_level
        else: xp_percentage = 1
        bar_width = int(200 * xp_percentage)
        self.xp_bar_canvas.create_rectangle(0, 0, bar_width, 18, fill=COLOR_XP, outline="")
        self.xp_bar_canvas.create_text(100, 9, text=f"XP: {self.player.xp} / {self.player.xp_to_next_level}", font=FONT_NORMAL, fill="white")
    
    def update_stat_upgrade_ui(self):
        for widget in self.stat_upgrade_frame.winfo_children(): widget.destroy()
        if self.player and self.player.stat_points > 0:
            lbl = tk.Label(self.stat_upgrade_frame, text=f"Attributpunkte: {self.player.stat_points}", font=FONT_BOLD, bg=BG_COLOR, fg=COLOR_GOLD); lbl.pack()
            btn_str = tk.Button(self.stat_upgrade_frame, text="[+] Stärke", command=lambda: self.upgrade_stat("staerke"), bg="#555", fg=TEXT_COLOR); btn_str.pack(fill="x", padx=5)
            btn_dex = tk.Button(self.stat_upgrade_frame, text="[+] Geschick", command=lambda: self.upgrade_stat("geschick"), bg="#555", fg=TEXT_COLOR); btn_dex.pack(fill="x", padx=5)
            btn_int = tk.Button(self.stat_upgrade_frame, text="[+] Intelligenz", command=lambda: self.upgrade_stat("intelligenz"), bg="#555", fg=TEXT_COLOR); btn_int.pack(fill="x", padx=5)
    
    def upgrade_stat(self, stat_name):
        if self.player.stat_points > 0:
            self.player.base_stats[stat_name] += 1; self.player.stat_points -= 1
            self.player.recalculate_stats()
            self.log(f"{stat_name.capitalize()} wurde permanent erhöht!", COLOR_GOLD); self.update_status_display()

    def draw_map(self):
        self.map_canvas.delete("all")
        if not self.player: return
        px, py = self.player.position
        for y in range(MAP_SIZE):
            for x in range(MAP_SIZE):
                key = f"({x}, {y})"; fill_color = "#222"
                if key in self.dungeon_map and self.dungeon_map[key].get("besucht"):
                    event = self.dungeon_map[key].get("event")
                    if event == "boss": fill_color = "#500"
                    elif event == "merchant": fill_color = "#050"
                    elif event == "stairs": fill_color = "#530"
                    elif event == "shrine": fill_color = "#550"
                    else: fill_color = FRAME_COLOR
                self.map_canvas.create_rectangle(x * CELL_SIZE, y * CELL_SIZE, (x + 1) * CELL_SIZE, (y + 1) * CELL_SIZE, fill=fill_color, outline="#444")
        self.map_canvas.create_oval(px * CELL_SIZE + 5, py * CELL_SIZE + 5, (px + 1) * CELL_SIZE - 5, (py + 1) * CELL_SIZE - 5, fill=COLOR_RARE, outline="white")

    def generate_dungeon(self):
        self.dungeon_map = {}
        start_pos_key = f"({self.player.position[0]}, {self.player.position[1]})"
        possible_coords = [(x, y) for x in range(MAP_SIZE) for y in range(MAP_SIZE) if f"({x}, {y})" != start_pos_key]
        random.shuffle(possible_coords)
        target_key = f"({possible_coords.pop()})"
        merchant_key = f"({possible_coords.pop()})"
        shrine_key = ""
        if self.current_floor != BOSS_FLOOR: shrine_key = f"({possible_coords.pop()})"
        for y in range(MAP_SIZE):
            for x in range(MAP_SIZE):
                key = f"({x}, {y})"
                if key == target_key: event = "boss" if self.current_floor == BOSS_FLOOR else "stairs"
                elif key == merchant_key: event = "merchant"
                elif key == shrine_key: event = "shrine"
                elif key == start_pos_key: event = "leer"
                else: event = random.choices(["gegner", "truhe", "leer"], weights=[0.55, 0.1, 0.35], k=1)[0]
                self.dungeon_map[key] = {"besucht": False, "event": event}

    def start_difficulty_selection(self):
        self.clear_all_frames()
        tk.Label(self.info_frame, text="Chroniken des Abgrunds", font=FONT_BIG, bg=FRAME_COLOR, fg=COLOR_LEGENDARY).pack(pady=20)
        self.log("Wähle deinen Schwierigkeitsgrad:")
        normal_btn = tk.Button(self.button_frame, text="Normal", command=lambda: self.set_difficulty("Normal"), bg="#555", fg=TEXT_COLOR, font=FONT_BOLD); normal_btn.pack(fill="x", padx=10, pady=5)
        nightmare_btn = tk.Button(self.button_frame, text="Albtraum", command=lambda: self.set_difficulty("Albtraum"), bg="#800", fg=TEXT_COLOR, font=FONT_BOLD); nightmare_btn.pack(fill="x", padx=10, pady=5)

    def set_difficulty(self, choice):
        self.difficulty = choice
        if choice == "Albtraum": self.difficulty_mod = 1.5
        self.start_character_selection()
        
    def start_character_selection(self):
        self.clear_all_frames(); self.game_state = "char_selection"
        tk.Label(self.info_frame, text="Charakterauswahl", font=FONT_BIG, bg=FRAME_COLOR, fg=COLOR_LEGENDARY).pack(pady=20)
        self.log("Wähle deine Klasse für eine Vorschau.", "#aaaaaa")
        class_list_frame = tk.Frame(self.button_frame, bg="#111"); class_list_frame.pack(side="left", fill="y", padx=5)
        self.preview_frame = tk.Frame(self.button_frame, bg="#111"); self.preview_frame.pack(side="right", expand=True, fill="both", padx=5)
        for char_key, char_val in CHARAKTER_VORLAGEN.items():
            btn = tk.Button(class_list_frame, text=char_val["name"], bg="#555", fg=TEXT_COLOR, command=lambda k=char_key: self.preview_character(k)); btn.pack(fill="x", pady=2)
        shop_btn = tk.Button(class_list_frame, text="Shop der Seelen", bg=COLOR_EPIC, fg="white", command=self.open_meta_shop); shop_btn.pack(fill="x", pady=(20,2))
        if os.path.exists("savegame.json"):
            load_btn = tk.Button(class_list_frame, text="Spielstand laden", bg=COLOR_RARE, fg=TEXT_COLOR, command=self.load_game); load_btn.pack(fill="x", pady=2)
            
    def preview_character(self, char_key):
        self.selected_char_preview = char_key
        for widget in self.preview_frame.winfo_children(): widget.destroy()
        template = CHARAKTER_VORLAGEN[char_key]
        tk.Label(self.preview_frame, text=template['name'], font=FONT_BOLD, bg="#111", fg=COLOR_RARE).pack(anchor="w")
        tk.Label(self.preview_frame, text=template['beschreibung'], font=FONT_NORMAL, bg="#111", fg=TEXT_COLOR, justify="left", wraplength=250).pack(anchor="w", pady=5)
        stats = (f"Leben: {template['max_leben']} | Mana: {template['max_mana']}\n"
                 f"STR: {template['staerke']} | GES: {template['geschick']} | INT: {template['intelligenz']}")
        tk.Label(self.preview_frame, text=stats, font=FONT_NORMAL, bg="#111", fg=TEXT_COLOR, justify="left").pack(anchor="w", pady=5)
        skill = template['skills'][0]
        skill_text = f"Startfähigkeit: {skill['name']} ({skill['cost']} Mana)"
        tk.Label(self.preview_frame, text=skill_text, font=FONT_NORMAL, bg="#111", fg=TEXT_COLOR, justify="left").pack(anchor="w")
        confirm_btn = tk.Button(self.preview_frame, text=f"{template['name']} wählen", bg=COLOR_HEALTH, fg="black", font=FONT_BOLD, command=self.select_character); confirm_btn.pack(pady=10)

    def select_character(self):
        meta_bonuses = self.get_meta_bonuses()
        self.player = Player(CHARAKTER_VORLAGEN[self.selected_char_preview], meta_bonuses)
        self.clear_all_frames(); self.setup_game_ui()
        self.log(f"Du hast den {self.player.name} gewählt. Möge das Schicksal dir gnädig sein!", COLOR_RARE)
        self.start_new_floor()
        
    def open_inventory(self, event=None):
        if self.game_state not in ["exploring", "combat", "merchant", "stairs", "shrine"]: return
        self.root.attributes('-disabled', True)
        inv_win = InventoryWindow(self.root, self)
        inv_win.grab_set()

    def open_skill_selection(self):
        self.root.attributes('-disabled', True); self.game_state = "skill_selection"
        all_learnable = []
        char_type = self.player.char_type
        if char_type in SKILL_DATABASE:
            all_learnable = [s for s in SKILL_DATABASE[char_type] if s['level'] <= self.player.level and s['id'] not in [ps['id'] for ps in self.player.skills]]
        if not all_learnable:
            self.log("Keine neuen Fähigkeiten zu lernen.", "#aaaaaa"); self.player.skill_points = 0
            self.root.attributes('-disabled', False); self.start_exploring(); return
        choices = random.sample(all_learnable, k=min(2, len(all_learnable)))
        skill_win = SkillSelectionWindow(self.root, self, choices)
        skill_win.grab_set()
        
    def open_meta_shop(self):
        self.root.attributes('-disabled', True)
        shop_win = MetaShopWindow(self.root, self)
        shop_win.grab_set()
    
    def start_new_floor(self):
        self.player.position = [MAP_SIZE // 2, MAP_SIZE // 2]; self.generate_dungeon(); self.start_exploring()
        self.enter_room(tuple(self.player.position), is_new_floor=True)

    def start_exploring(self):
        self.game_state = "exploring"; self.clear_buttons()
        save_btn = tk.Button(self.button_frame, text="Spiel speichern", command=self.save_game, bg=COLOR_RARE, fg=TEXT_COLOR); save_btn.pack(fill="x", padx=5, pady=5)
        self.update_status_display()
        if self.player.skill_points > 0: self.open_skill_selection()
        else: self.log("Du erkundest die Etage. (I: Inventar)", "#aaaaaa")

    def move_player(self, direction):
        if self.game_state not in ["exploring"]: return
        if "stun" in self.player.status_effects:
            self.log("Du bist betäubt und kannst dich nicht bewegen!", COLOR_STUN)
            self.process_player_turn_effects(); return
        self.process_player_turn_effects() 
        if self.player.leben <= 0: self.game_over(); return
        dx, dy = 0, 0
        if direction == "n": dy = -1
        elif direction == "s": dy = 1
        elif direction == "w": dx = -1
        elif direction == "o": dx = 1
        new_pos = (self.player.position[0] + dx, self.player.position[1] + dy)
        if 0 <= new_pos[0] < MAP_SIZE and 0 <= new_pos[1] < MAP_SIZE:
            self.player.position = list(new_pos); self.enter_room(new_pos)
        else: self.log("Du stehst vor einer massiven Wand.", "#aaaaaa")

    def enter_room(self, pos, is_new_floor=False):
        key = str(pos); room = self.dungeon_map.get(key)
        if not room: return
        if is_new_floor: self.log(f"Du betrittst Etage {self.current_floor}. Die Schatten werden tiefer.", COLOR_RARE)
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
        self.log("Du hast eine Treppe gefunden, die tiefer in den Abgrund führt.", COLOR_LEGENDARY)
        descend_btn = tk.Button(self.button_frame, text=f"Abstieg zu Etage {self.current_floor + 1}", command=self.descend_floor, bg=COLOR_LEGENDARY, fg="black"); descend_btn.pack(fill="x", padx=5, pady=5)
        leave_btn = tk.Button(self.button_frame, text="Noch nicht...", command=self.start_exploring, bg="#aaa", fg="black"); leave_btn.pack(fill="x", padx=5, pady=5)
    
    def descend_floor(self): self.current_floor += 1; self.start_new_floor()

    def find_treasure(self):
        self.log(f"🧰 Du findest eine Schatztruhe!", COLOR_GOLD)
        gold_found = int(random.randint(10, 30) * self.difficulty_mod * self.current_floor)
        self.player.gold += gold_found; self.log(f"Darin sind {gold_found} Goldmünzen.", COLOR_GOLD)
        
        if random.random() < (0.25 * self.difficulty_mod):
            rarities = ["common", "rare", "epic", "legendary"]
            weights = [0.6, 0.3, 0.09, 0.01]
            chosen_rarity = random.choices(rarities, weights, k=1)[0]
            item_type = random.choice(list(EQUIPMENT_DATABASE.keys()))
            possible_items = [item for item in EQUIPMENT_DATABASE[item_type] if item['seltenheit'] == chosen_rarity]
            if possible_items:
                item = random.choice(possible_items).copy()
                if not self.player.add_to_inventory(item): self.log(f"{item['name']} konnte nicht aufgenommen werden (Inventar voll).", "#ff4444")
                else: self.log(f"Du findest: {item['name']}!", {"common": COLOR_COMMON, "rare": COLOR_RARE, "epic": COLOR_EPIC, "legendary": COLOR_LEGENDARY}.get(chosen_rarity))
        elif random.random() < 0.5:
            trank_typ = random.choice(["Heiltrank", "Manatrank"])
            if trank_typ == "Heiltrank": self.player.heiltränke += 1
            else: self.player.manatränke += 1
            self.log(f"Außerdem findest du einen {trank_typ}!", "#ffff00")

    def enter_shrine(self):
        self.game_state = "shrine"; self.clear_buttons()
        self.log("Du findest einen alten, pulsierenden Schrein.", COLOR_SHRINE)
        pray_btn = tk.Button(self.button_frame, text="Am Schrein beten", command=self.pray_at_shrine, bg=COLOR_SHRINE, fg="black"); pray_btn.pack(fill="x", padx=5, pady=5)
        leave_btn = tk.Button(self.button_frame, text="Den Schrein ignorieren", command=self.start_exploring, bg="#aaa", fg="black"); leave_btn.pack(fill="x", padx=5, pady=5)

    def pray_at_shrine(self):
        self.dungeon_map[f"({self.player.position[0]}, {self.player.position[1]})"]["event"] = "leer"
        outcomes = ["heal", "stat_boost", "curse", "nothing"]
        outcome = random.choices(outcomes, weights=[0.4, 0.2, 0.2, 0.2], k=1)[0]
        if outcome == "heal":
            self.player.leben = self.player.max_leben; self.player.mana = self.player.max_mana
            self.log("Eine Welle heilender Energie durchströmt dich!", COLOR_HEALTH)
        elif outcome == "stat_boost":
            stat = random.choice(["staerke", "geschick", "intelligenz"])
            self.player.base_stats[stat] += 1; self.player.recalculate_stats()
            self.log(f"Du spürst neue Kraft! Deine {stat.capitalize()} wurde permanent um 1 erhöht!", COLOR_LEGENDARY)
        elif outcome == "curse":
            self.player.leben = max(1, self.player.leben - 10)
            self.log("Der Schrein leuchtet dunkelrot! Du verlierst 10 Leben!", COLOR_CRIT)
        else: self.log("Du betest, aber nichts geschieht.", "#aaaaaa")
        self.update_status_display(); self.root.after(1500, self.start_exploring)

    def enter_merchant(self):
        self.game_state = "merchant"; self.clear_buttons(); self.log("Ein Händler bietet dir seine Waren an:", COLOR_HEALTH)
        buy_hp_btn = tk.Button(self.button_frame, text=f"Heiltrank kaufen ({ITEMS['heiltrank']['preis']} G)", command=lambda: self.buy_item("heiltrank"), bg="#2ca02c", fg="white"); buy_hp_btn.pack(fill="x", padx=5, pady=2)
        buy_mp_btn = tk.Button(self.button_frame, text=f"Manatrank kaufen ({ITEMS['manatrank']['preis']} G)", command=lambda: self.buy_item("manatrank"), bg="#007acc", fg="white"); buy_mp_btn.pack(fill="x", padx=5, pady=2)
        leave_btn = tk.Button(self.button_frame, text="Händler verlassen", command=self.start_exploring, bg="#aaa", fg="black"); leave_btn.pack(fill="x", padx=5, pady=10)

    def buy_item(self, item_name):
        preis = ITEMS[item_name]['preis']
        if self.player.gold >= preis:
            self.player.gold -= preis
            if item_name == "heiltrank": self.player.heiltränke += 1
            else: self.player.manatränke += 1
            self.log(f"Du hast einen {item_name.replace('_', ' ')} gekauft.", COLOR_HEALTH); self.update_status_display()
        else: self.log("Du hast nicht genug Gold!", "#ff4444")

    def use_potion(self, potion_type):
        if self.game_state not in ["exploring", "combat"]: return
        int_bonus_factor = 1 + (self.player.intelligenz / 20.0) 
        if potion_type == "heiltrank" and self.player.heiltränke > 0:
            if self.player.leben < self.player.max_leben:
                base_heal = ITEMS['heiltrank']['leben']; total_heal = int(base_heal * int_bonus_factor)
                self.player.heiltränke -= 1; self.player.leben = min(self.player.max_leben, self.player.leben + total_heal)
                self.log(f"Heiltrank benutzt. Leben +{total_heal}.", COLOR_HEALTH); self.update_status_display()
            else: self.log("Dein Leben ist bereits voll.", "#aaaaaa")
        elif potion_type == "manatrank" and self.player.manatränke > 0:
            if self.player.mana < self.player.max_mana:
                base_mana = ITEMS['manatrank']['mana']; total_mana = int(base_mana * int_bonus_factor)
                self.player.manatränke -= 1; self.player.mana = min(self.player.max_mana, self.player.mana + total_mana)
                self.log(f"Manatrank benutzt. Mana +{total_mana}.", COLOR_MANA); self.update_status_display()
            else: self.log("Dein Mana ist bereits voll.", "#aaaaaa")

    def start_combat(self, gegner_template, is_boss=False):
        self.game_state = "combat"; self.current_gegner = gegner_template.copy()
        scaling_factor = 1 + ((self.current_floor - 1) * 0.25 * self.difficulty_mod)
        self.current_gegner["leben"] = int(self.current_gegner["leben"] * scaling_factor)
        self.current_gegner["staerke"] = int(self.current_gegner["staerke"] * scaling_factor)
        self.current_gegner["xp"] = int(self.current_gegner["xp"] * scaling_factor)
        self.current_gegner["gold"] = int(self.current_gegner["gold"] * scaling_factor)
        self.log(f"\n⚔️ Du triffst auf einen {self.current_gegner['name']}! ⚔️", "#ff4444"); self.update_status_display(); self.setup_combat_buttons()

    def setup_combat_buttons(self):
        self.clear_buttons()
        if not self.current_gegner: return
        self.log(f"Gegner: {self.current_gegner['name']} | Leben: {self.current_gegner['leben']}", "#ff4444")
        attack_btn = tk.Button(self.button_frame, text="Angriff", command=self.player_attack, bg="#cc2222", fg="white"); attack_btn.pack(fill="x", padx=5, pady=2)
        for skill in self.player.skills:
            btn = tk.Button(self.button_frame, text=f"{skill['name']} ({skill['cost']} Mana)", bg="#9933ff", fg="white", command=lambda s=skill: self.player_special_attack(s)); btn.pack(fill="x", padx=5, pady=2)
        flee_btn = tk.Button(self.button_frame, text="Fliehen", command=self.flee_combat, bg="#aaa", fg="black"); flee_btn.pack(fill="x", padx=5, pady=10)

    def process_player_turn_effects(self):
        if "stun" in self.player.status_effects:
            self.log("Du bist betäubt!", COLOR_STUN)
            del self.player.status_effects['stun']
            return False # Zug aussetzen
        effects_to_remove = []
        for key, effect in list(self.player.status_effects.items()):
            if key == "poison":
                damage = effect['damage']; self.player.leben -= damage
                self.log(f"Du erleidest {damage} Giftschaden.", COLOR_HEALTH)
            effect['duration'] -= 1
            if effect['duration'] <= 0:
                effects_to_remove.append(key)
                self.log(f"Der Effekt '{effect.get('name', key)}' ist abgeklungen.", "#aaaaaa")
        for key in effects_to_remove:
            if key in self.player.status_effects: del self.player.status_effects[key]
        self.player.recalculate_stats(); self.update_status_display()
        return True

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
        if not self.process_player_turn_effects(): self.check_combat_status(); return
        if self.player.leben <= 0: self.game_over(); return
        base_damage = self.player.get_total_schaden()
        schaden = random.randint(base_damage // 2, base_damage)
        is_crit = random.random() < self.player.get_crit_chance()
        self.inflict_damage_to_enemy(schaden, "normal", is_crit)

    def player_special_attack(self, skill):
        if not self.process_player_turn_effects(): self.check_combat_status(); return
        if self.player.leben <= 0: self.game_over(); return
        if self.player.mana >= skill["cost"]:
            self.player.mana -= skill["cost"]; self.log(f"Du setzt '{skill['name']}' ein!", COLOR_EPIC)
            if "heal_amount" in skill:
                heal_bonus = self.player.intelligenz // 2; total_heal = skill['heal_amount'] + heal_bonus
                self.player.leben = min(self.player.max_leben, self.player.leben + total_heal)
                self.log(f"Du heilst dich um {total_heal} Leben.", COLOR_HEALTH); self.check_combat_status(); return
            
            if "effect" in skill: self.apply_effect(self.player, skill["effect"], is_player_buff=True)

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
        if self.current_gegner and self.current_gegner["leben"] <= 0: self.win_combat()
        else: self.root.after(500, self.enemy_attack)

    def enemy_attack(self):
        if not self.current_gegner: return
        if random.random() < self.player.get_dodge_chance():
            self.log(f"Du weichst dem Angriff des {self.current_gegner['name']} geschickt aus!", COLOR_DODGE)
            self.root.after(500, self.setup_combat_buttons); return
            
        special = self.current_gegner.get("special")
        if special and random.random() < special["chance"]:
            self.log(f"Der {self.current_gegner['name']} setzt seine Spezialfähigkeit ein!", "#ff9900")
            if special['type'] == 'heal':
                self.current_gegner['leben'] += special['amount']; self.log(f"Er heilt sich um {special['amount']} Leben.", COLOR_HEALTH)
            elif special['type'] == 'stun':
                self.apply_effect(self.player, special); self.log("Du wurdest betäubt!", COLOR_STUN)
            else: self.apply_effect(self.player, special); self.log(f"Du wurdest mit {special['type']} belegt!", COLOR_CRIT)
        else:
            schaden = self.current_gegner["staerke"] - self.player.get_total_verteidigung()
            schaden = max(1, random.randint(schaden // 2, schaden))
            self.player.leben -= schaden
            self.log(f"Der {self.current_gegner['name']} greift an und fügt dir {schaden} Schaden zu.", "#ff4444")
        
        self.update_status_display()
        if self.player.leben <= 0: self.game_over()
        else: self.setup_combat_buttons()

    def apply_effect(self, target, effect_data, is_player_buff=False):
        effect_copy = effect_data.copy()
        target_effects = target.status_effects
        if "chance" in effect_copy and random.random() > effect_copy['chance']: return # Effekt hat nicht ausgelöst
        
        if is_player_buff:
            effect_copy['name'] = effect_data.get('type')
            target_effects[effect_copy['type']] = effect_copy
            self.log(f"Du erhältst den Buff '{effect_copy['name']}'!", COLOR_RARE)
        else:
            target_effects[effect_copy['type']] = effect_copy
        
    def win_combat(self):
        kristalle = self.current_gegner.get("kristalle", 0)
        if kristalle > 0:
            self.meta_progress['kristalle'] = self.meta_progress.get('kristalle', 0) + kristalle
            self.save_meta_progress()
            self.log(f"Du erhältst {kristalle} Abyssale Kristalle!", COLOR_CRYSTAL)

        gold_reward = self.current_gegner["gold"]; xp_reward = self.current_gegner["xp"]
        self.player.gold += gold_reward
        self.log(f"Du hast den {self.current_gegner['name']} besiegt!", COLOR_HEALTH)
        self.log(f"Du erhältst {gold_reward} Gold.", COLOR_GOLD)
        base_xp, bonus_xp, level_up = self.player.gain_xp(xp_reward)
        log_msg = f"Du erhältst {base_xp} XP"
        if bonus_xp > 0: log_msg += f" (+{bonus_xp} Intelligenz-Bonus!)"
        self.log(log_msg, COLOR_XP)

        self.dungeon_map[f"({self.player.position[0]}, {self.player.position[1]})"]["event"] = "leer"
        if "Drache" in self.current_gegner["name"]: self.victory(); return
        
        self.current_gegner = None
        if level_up:
            self.log(f"LEVEL UP! Du hast Level {self.player.level} erreicht!", COLOR_LEGENDARY)
            self.update_status_display()
            self.root.after(1000, self.start_exploring)
        else: self.start_exploring()

    def victory(self):
        self.game_state = "game_over"; self.clear_buttons(); self.log("\n🎉 SIEG! 🎉", COLOR_LEGENDARY)
        self.log(f"Du hast den mächtigen {BOSS_GEGNER['name']} besiegt!", COLOR_LEGENDARY)
        messagebox.showinfo("Sieg!", "Herzlichen Glückwunsch! Du hast das Spiel gewonnen!")
        self.root.quit()

    def game_over(self):
        self.game_state = "game_over"; self.clear_buttons(); self.log("\n☠️ GAME OVER ☠️", COLOR_CRIT)
        messagebox.showerror("Game Over", "Deine Reise endet hier.")
        self.root.quit()
        
    def save_game(self):
        if not self.player: return
        game_state = {"player": self.player.to_dict(), "dungeon_map": self.dungeon_map, "current_floor": self.current_floor, "difficulty": self.difficulty}
        try:
            with open("savegame.json", "w") as f: json.dump(game_state, f, indent=4)
            self.log("Spiel erfolgreich gespeichert!", COLOR_RARE)
        except Exception as e: messagebox.showerror("Fehler", f"Spiel konnte nicht gespeichert werden: {e}")

    def load_game(self):
        try:
            with open("savegame.json", "r") as f: game_state = json.load(f)
            meta_bonuses = self.get_meta_bonuses()
            self.player = Player.from_dict(game_state["player"], meta_bonuses)
            self.dungeon_map = game_state["dungeon_map"]; self.current_floor = game_state["current_floor"]
            self.difficulty = game_state.get("difficulty", "Normal")
            self.difficulty_mod = 1.5 if self.difficulty == "Albtraum" else 1.0
            
            self.clear_all_frames(); self.setup_game_ui()
            self.log("Spielstand erfolgreich geladen!", COLOR_RARE)
            self.start_exploring()
        except Exception as e:
            messagebox.showerror("Fehler", f"Konnte Spielstand nicht laden: {e}"); self.start_difficulty_selection()

# ============== SPIELSTART ==============
if __name__ == "__main__":
    root = tk.Tk()
    game = Game(root)
    root.mainloop()
