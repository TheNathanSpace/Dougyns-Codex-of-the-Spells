import json
import re
from pathlib import Path

spells_file = Path("../script_output/spells.json")
output_file = Path("../script_output/tags.json")

spell_json_dict = json.loads(spells_file.read_text(encoding = "utf-8"))
tags_dict = {}

for spell_level in spell_json_dict:
    for spell in spell_json_dict[spell_level]:
        if re.search("^\*(.{3})-level ", spell_json_dict[spell_level][spell]['level']):
            re_level = re.search("^\*(.{3})-level ", spell_json_dict[spell_level][spell]['level']).group(1)
        else:
            if re.search("^\*.* cantrip\*", spell_json_dict[spell_level][spell]['level']):
                re_level = "0th"

        spell_name = spell + f" ({re_level})"

        for tag in spell_json_dict[spell_level][spell]["tags"]:
            if tag in tags_dict:
                tags_dict[tag].append(spell_name)
            else:
                tags_dict[tag] = [spell_name]

output_file.write_text(json.dumps(tags_dict, ensure_ascii = False, indent = 4), encoding = "utf-8")
