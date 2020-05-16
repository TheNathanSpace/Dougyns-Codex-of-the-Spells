# This script changes all of the page numbers in a .txt file formatted for Homebrewery by a certain amount. You might want to test that it works properly before using
# it; in its current form it pushes the changes directly to the input file. Make a backup.


def chomp(x):
    if x.endswith("\r\n"): return x[:-2]
    if x.endswith("\n") or x.endswith("\r"): return x[:-1]
    return x
def reversechomp(x):
    if x.startswith("\r\n"): return x[2:]
    if x.startswith("\n") or x.startswith("\r"): return x[1:]
    return x

file = "9th Level.txt"
inputFile = open(file, "r+", encoding = "utf-8")
contentsList = list(inputFile)
inputFile.close()

listCopy = contentsList

for iteration in range(0, len(contentsList)):
    line = contentsList[iteration]
    if line != "":
        line = chomp(line)
        line = reversechomp(line)

        if "<div class='pageNumber'>" in line:
            number = line
            number = number[24:]
            number = number[:-6]
            number = int(number)
            number = number + 17 # THIS IS THE LINE WHERE THE ADJUSTMENT IS MADE.
            listCopy[iteration] = "<div class='pageNumber'>" + str(number) + "</div>"
        else:
            listCopy[iteration] = line
        
contents = ""
for yeet in listCopy:
    if not yeet in ['\n', '\r\n', '\n\r\s']:
        contents = contents + "\n" + yeet

inputFile = open(file, "w", encoding = "utf-8")
inputFile.write(contents)
inputFile.close()