import json
from collections import OrderedDict
from pathlib import Path

master_spell_file = json.loads(Path("../script_output/spells.json").read_text(encoding = "utf-8"))
all_spells = {}
for spell_level in master_spell_file:
    for spell in master_spell_file[spell_level]:
        all_spells[spell] = master_spell_file[spell_level][spell]

input_spell = input("Enter spell name (will be converted to title case): ").title()
spell_dict = all_spells[input_spell]

card_dict = OrderedDict()
card_dict["count"] = 1
card_dict["color"] = "maroon"
card_dict["title"] = input_spell
card_dict["icon"] = "white-book-1"
card_dict["icon_back"] = "robe"

contents = []
subtitle = str("subtitle | " + spell_dict["level"]).replace("*", "")
contents.append(subtitle)
contents.append("rule")
casting_time = str(spell_dict["casting_time"]).replace("*", "")
contents.append(f"property | Casting time | {casting_time}")
range = str(spell_dict["range"]).replace("*", "")
contents.append(f"property | Range | {range}")
components = str(spell_dict["components"]).replace("*", "")
contents.append(f"property | Components | {components}")
contents.append("rule")
contents.append("fill | 2")

text = "text | "
for description_line in spell_dict["description"]:
    contents.append(text + str(description_line).replace("*", ""))
contents.append("fill | 3")

card_dict["contents"] = contents


print(json.dumps([card_dict], ensure_ascii = False, indent = 4))