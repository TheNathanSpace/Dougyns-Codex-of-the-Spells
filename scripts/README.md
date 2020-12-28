This directory contains all of the scripts used to process the spell files and make them compatible with GMBinder.

---

`read_source` reads the spell files in the directory defined in `source_directory`. It outputs a `.json` file of every spell. Every other script depends on that `.json` file.

---

`make_sources` counts up how many spells are in each sourcebook:

 - Player's Handbook
 - Sword Coast Adventurer's Guide
 - Tasha's Cauldron of Everything
 - Elemental Evil Player’s Companion
 - Xanathar's Guide to Everything
 
---

`make_spell_chapters` creates `.txt` files for each spell level that are ready to go into GMBinder. You'll have to manually add column/page breaks and that sort of thing, but this does all the text formatting for you.

---

`make_tags` creates a `.json` file that has lists of spells associated with each tag. Here are some examples of the tags:

 - `conjuration`
 - `bard`
 - `gnome (forest)`
 - `ritual`
 - `level1`
 
---

`make_spell_lists` creates `.txt` files for each class' spell list that are ready to go into GMBinder. It depends on the `tags.json` file created by the `make_tags` script.