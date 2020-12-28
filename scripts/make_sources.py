import json
import re
from collections import OrderedDict
from pathlib import Path

master_spell_file = json.loads(Path("../script_output/spells.json").read_text(encoding = "utf-8"))

sources_dict = OrderedDict()

for spell_level in master_spell_file:
    for spell in master_spell_file[spell_level]:
        for source in master_spell_file[spell_level][spell]["sources"]:
            source_string = re.findall("^(\w*).\d*", source)
            if not len(source_string) == 0:
                source_string = source_string[0]
                if source_string in sources_dict:
                    sources_dict[source_string] = sources_dict[source_string] + 1
                else:
                    sources_dict[source_string] = 1
            else:
                if "none" in sources_dict:
                    sources_dict["none"] = sources_dict["none"] + 1
                else:
                    sources_dict["none"] = 1


sources_output_file = Path("../script_output/sources.json")
sources_output_file.write_text(json.dumps(sources_dict, ensure_ascii = False, indent = 4), encoding = "utf-8")
