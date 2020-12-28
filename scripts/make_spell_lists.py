import json
import re
from collections import OrderedDict
from pathlib import Path

tags_file = Path("../script_output/tags.json")
spell_lists_directory = Path("../script_output/spell_lists/")
spell_lists_directory.mkdir(exist_ok = True)

tags_dict = json.loads(tags_file.read_text(encoding = "utf-8"))

classes_dict = {"artificer", "bard", "cleric", "druid", "paladin", "ranger", "sorcerer", "warlock", "wizard"}

for class_name in classes_dict:
    class_spell_list_gmbinder = \
        f"""

### {class_name.title()} Spells
<div style='margin-top:50px'></div>
<div class='spellList'>

"""

    cantrips_title = "##### Cantrips (0 Level)"

    class_spell_list = tags_dict[class_name]
    split_spells = OrderedDict()

    for spell in class_spell_list:
        parsed = re.search("(.*) \((\d.{2})\)", spell)
        spell_name = parsed.group(1)
        spell_level = parsed.group(2)

        if spell_level in split_spells:
            split_spells[spell_level].append(spell_name)
        else:
            split_spells[spell_level] = [spell_name]

    split_spells = {k: split_spells[k] for k in sorted(split_spells)}

    for spell_level in split_spells:

        if not (spell_level == "0th"):
            class_spell_list_gmbinder += f"\n##### {spell_level} Level"
        else:
            class_spell_list_gmbinder += f"\n##### Cantrips (0 Level)"

        split_spells[spell_level].sort()

        for spell in split_spells[spell_level]:
            class_spell_list_gmbinder += f"\n- {spell}"
        class_spell_list_gmbinder += "\n"

    class_spell_list_gmbinder += \
"""</div>

<br>
<br>

\pagebreak

"""

    output_file = spell_lists_directory / f"{class_name}.txt"

    output_file.write_text(class_spell_list_gmbinder, encoding = "utf-8")

# ### Artificer Spells
# <div style='margin-top:50px'></div>
#
# <div class='spellList'>
#
# ##### Cantrips (0 Level)
# - Acid Splash
# - Create Bonfire
#
# ##### 1st Level
# - Absorb Elements
