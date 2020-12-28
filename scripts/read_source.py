import json
from collections import OrderedDict
from pathlib import Path
import re

source_directory = Path(Path.cwd().parent.parent / "fork" / "_posts")

master_spell_dict = OrderedDict()

for file_path in source_directory.iterdir():
    current_file_text = file_path.read_text(encoding = "utf-8")
    current_file_lines = current_file_text.splitlines()

    title = ""
    sources_list = None
    tags_list = None
    re_level = None

    level = None
    casting_time = None
    range = None
    components = None
    duration = None
    description = []

    dash_count = 0
    for line in current_file_lines:

        line = line.replace("­", "")
        if "|" not in line:
            line = " ".join(line.split())

        if dash_count == 2:
            if line.strip():

                if re.search("^\*\*(.{3})-level ", line):
                    re_level = re.search("^\*\*(.{3})-level ", line).group(1)
                    level = line.replace("**", "*")
                    continue
                else:
                    if re.search("^\*\*.* cantrip\*\*", line):
                        re_level = "0th"
                        level = line.replace("**", "*")
                        continue
                    if re.search("^\*\*.* Cantrip\*\*", line):
                        re_level = "0th"
                        level = line.replace("Cantrip", "cantrip").replace("**", "*")
                        continue

                if re.search("^\*\*Casting Time\*\*:", line):
                    casting_time = line
                    continue

                if re.search("^\*\*Range\*\*:", line):
                    range = line
                    continue

                if re.search("^\*\*Components\*\*:", line):
                    components = line
                    continue

                if re.search("^\*\*Duration\*\*:", line):
                    duration = line
                    continue

                if duration is not None:
                    description.append(line.strip().replace("\t", "").replace("• ", " * "))
                    continue

        if re.search("^title: *\"(.*)\"", line):
            title = re.search("^title: *\"(.*)\"", line).group(1)
            continue

        if re.search("^sources: *\[(.*)]", line):
            string_separated = re.search("^sources: *\[(.*)]", line).group(1)
            sources_list = re.split(" *, *", string_separated)
            continue

        if re.search("^tags: *\[(.*)]", line):
            string_separated = re.search("^tags: *\[(.*)]", line).group(1)
            tags_list = re.split(" *, *", string_separated)
            continue

        if re.search("---", line):
            dash_count += 1
            continue

    current_spell_dict = OrderedDict()
    current_spell_dict["level"] = level
    current_spell_dict["casting_time"] = casting_time
    current_spell_dict["range"] = range
    current_spell_dict["components"] = components
    current_spell_dict["duration"] = duration
    current_spell_dict["description"] = description
    current_spell_dict["sources"] = sources_list
    current_spell_dict["tags"] = tags_list

    if re_level not in master_spell_dict:
        master_spell_dict[re_level] = {}

    master_spell_dict[re_level][title] = current_spell_dict

for spell_level in master_spell_dict:
    master_spell_dict[spell_level] = {k: master_spell_dict[spell_level][k] for k in sorted(master_spell_dict[spell_level])}

output_file = Path("../script_output/spells.json")
output_file.touch(exist_ok = True)
master_spell_dict = {k: master_spell_dict[k] for k in sorted(master_spell_dict)}
output_file.write_text(json.dumps(master_spell_dict, indent = 4, ensure_ascii = False), encoding = "utf-8")
