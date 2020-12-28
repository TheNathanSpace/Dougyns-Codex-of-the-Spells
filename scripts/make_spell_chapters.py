import json
from pathlib import Path

master_spell_file = Path("../script_output/spells.json")
chapter_output_directory = Path("../script_output/spell_chapters/")
chapter_output_directory.mkdir(exist_ok = True)

spells_dict = json.loads(master_spell_file.read_text(encoding = "utf-8"))

for spell_level in spells_dict:
    spell_chapter_gm = ""

    for spell in spells_dict[spell_level]:
        spell_chapter_gm += f"#### {spell}" + "\n"
        spell_chapter_gm += spells_dict[spell_level][spell]["level"] + "\n"
        spell_chapter_gm += "___" + "\n"
        spell_chapter_gm += "- " + spells_dict[spell_level][spell]["casting_time"] + "\n"
        spell_chapter_gm += "- " + spells_dict[spell_level][spell]["range"] + "\n"
        spell_chapter_gm += "- " + spells_dict[spell_level][spell]["components"] + "\n"
        spell_chapter_gm += "- " + spells_dict[spell_level][spell]["duration"] + "\n\n"

        for description_line in spells_dict[spell_level][spell]["description"]:
            spell_chapter_gm += description_line + "\n\n"

    output_file = chapter_output_directory / f"{spell_level}.txt"

    output_file.write_text(spell_chapter_gm, encoding = "utf-8")
