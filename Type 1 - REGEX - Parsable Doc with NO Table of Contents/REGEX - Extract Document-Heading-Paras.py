# THIS SCRIPT accepts document with a structure similar to RAMA.pdf,
# Extracts Text, Formats the Content to allow REGEX to extract each
# HEADING/HEADING CONTENT/PARA in the document without Table of Contents !

import fitz
import re
doc = fitz.open("RAMA.pdf")

# (?<=\n\n).*(?=\n\n) TO EXTRACT HEADINGS!
# [^\r\n]+((\r|\n|\r\n)[^\r\n]+)* TO EXTRACT PARAS!

# Regex to extract paragraphs in the Format : <spacing> Multiline Text <spacing>
regex = "[^\r\n]+((\r|\n|\r\n)[^\r\n]+)*"

for page in doc:

    # Write File contents to a Text File
    with open('Document Text.txt', 'a+') as f:
        text = page.getText()
        f.write(text)
    
    # Read File to append Multiple Line Breaks for each Line Break (To separate Heading and Content for applying Regex)
    with open('Document Text.txt', 'r') as f1:
        lines = f1.readlines()
        for n, i in enumerate(lines):
            if i == ' \n':
                lines[n] = '\n\n\n'
    
    # Replace File Content with Newly Added Lines
    with open('Document Text.txt', 'w') as f2:
        f2.writelines(lines)


with open('Document Text.txt', 'r') as f3:
    content = f3.read()

# Search for Entire Content of Each Heading
matches = re.finditer(regex, content, re.MULTILINE)

# Extract Each Heading's Entire Content and Save in a new Text File
for matchNum, match in enumerate(matches, start=1):
    # Ignoring Headings by Hardcoding and considering TEXT LENGTH LESS THAN 100 characters to be HEADINGS.
    # In this case, this does not affect individual paras under the same heading as individual paras are not
    # separated by a NEWLINE delimiter.
    if len(match.group())>100:
        with open('paras.txt', 'a+') as f4:
            f4.writelines(match.group())
            f4.writelines("\n\n\n\n")

# Add Line Breaks to split Each paragraph in File
with open('paras.txt', 'r') as f1:
    lines1 = f1.readlines()
    for n, i in enumerate(lines1):
        # Look for every line that has less than 50 characters to consider them as each paragraph's last line.
        if re.search(r'^.{,50}\n', lines1[n]):
            lines1[n] = lines1[n] + '\n\n'

# Extract Each Paragraph
with open('paras.txt', 'w') as f2:
    f2.writelines(lines1)

