import requests
import urllib.request
from urllib.parse import urljoin
import time
from bs4 import BeautifulSoup
import json
from datetime import datetime

# If for some reason it stops partway through, just run it again. I ran into that problem a couple of times.

def make_spells(json_data):
	entry = ""
	newline = "\n"
	bullet = "- "
	for spell in json_data:
		spell_dict = json_data.get(spell)
		entry = entry + newline + newline
		entry = entry + "#### " + spell + newline + spell_dict.get("Type") + newline + "___" + newline
		entry = entry + bullet + spell_dict.get("Casting Time") + newline + bullet + spell_dict.get("Range") + newline + bullet + spell_dict.get("Components") + newline + bullet + spell_dict.get("Duration")
		
		for line in spell_dict.get("Description"):
			entry = entry + newline + newline + line
	
	return entry

startTime = datetime.now()
	
url = "https://thebombzen.com/grimoire/"
response = requests.get(url)

print(response)

contents = BeautifulSoup(response.text, "html.parser")
spell_links = contents.findAll("a", {"class": "post-link"})
json_data = {}

print(len(spell_links))
for spell_link in spell_links:
	spell_url = urljoin(url, spell_link["href"])
	spell_response = requests.get(spell_url)
	spell_contents = BeautifulSoup(spell_response.text, "html.parser")
	spell_post = spell_contents.find("div", {"class": "post"})

	spell_title = spell_post.find("header", {"class": "post-header"})

	spell_name = spell_title.find("h1", {"class": "post-title"}).find(text = True, recursive = False)
	print(spell_name)
	
	if spell_name == "Animate Objects" or spell_name == "Tiny Servant":
		print("Skipping!")
		continue

	spell_contents = spell_post.find("article", {"class": "post-content"})
	spell_paragraphs = spell_contents.findAll(recursive = False)

	type = "*" + spell_paragraphs[0].string + "*"
	del spell_paragraphs[0]
	casting_time = "**Casting Time:** " + spell_paragraphs[0].find(text = True, recursive = False).strip(": ")
	del spell_paragraphs[0]
	range = "**Range:** " + spell_paragraphs[0].find(text = True, recursive = False).strip(": ")
	del spell_paragraphs[0]
	components = "**Components:** " + spell_paragraphs[0].find(text = True, recursive = False).strip(": ")
	del spell_paragraphs[0]
	duration = "**Duration:** " + spell_paragraphs[0].find(text = True, recursive = False).strip(": ")
	del spell_paragraphs[0]
	
	# You can restart, get rid of the first couple results...
	spell_paragraphs = spell_contents.findAll()
	
	# Knock-off for loop because for some reason I keep getting an error for range()
	x = 0
	while x < 10:
		del spell_paragraphs[0]
		x += 1

	description_list = []
	current_paragraph = 1
		
	for paragraph in spell_paragraphs:
		if paragraph.name == "em":
			paragraph.string.replace_with("*" + paragraph.string + "*")
		if paragraph.name == "strong":
			paragraph.string.replace_with("**" + paragraph.string + "**")

	skip_next = False
	
	for paragraph in spell_paragraphs:
		if skip_next:
			skip_next = False
			continue
			
		elif paragraph.name == "ul" or paragraph.name == "ol":
			continue
				
		elif paragraph.name == "a":
			continue
			
		elif paragraph.name == "li":
			description_list.append(" * " + paragraph.text.replace("\n", ""))
			if len(paragraph.findAll("p")) > 0:
				skip_next = True
		
		elif paragraph.name == "strong" or paragraph.name == "em":
			continue
					
		else:
			description_list.append(paragraph.text.replace("\n", "")) # If nothing special then just add it
		
		current_paragraph += 1

	spell_dictionary = {}
	spell_dictionary["Type"] = type
	spell_dictionary["Casting Time"] = casting_time
	spell_dictionary["Range"] = range
	spell_dictionary["Components"] = components
	spell_dictionary["Duration"] = duration
	spell_dictionary["Description"] = description_list

	json_data[spell_name] = spell_dictionary
		
	time.sleep(1.5)

string_json = json.dumps(json_data, indent = 4, ensure_ascii = False)
with open("Output_JSON.txt", "w+", encoding = "utf-8") as output_file:
	output_file.write(string_json)
	
with open("Output_TEXT.txt", "w+", encoding = "utf-8") as output_file:	
	output = make_spells(json_data)
	output_file.write(output)
	
print("Time taken (minutes): " + str(datetime.now() - startTime))