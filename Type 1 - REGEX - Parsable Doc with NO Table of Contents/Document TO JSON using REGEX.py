# THIS SCRIPT accepts document with a structure similar to RAMA.pdf, Extracts Text, 
# Formats the Content to allow REGEX to extract each HEADING/HEADING CONTENT/PARA 
# in the document without Table of Contents AND CONVERTS INTO A CLEAN JSON structure like below:
""" 
[{
heading_id: 1,
heading_name: 'XYZ', 
heading_content:[{'p1':'abc..'},{'p2':'asfd..'},{'p3':'ehr..'}]
},{
heading_id: 1,
heading_name: 'XYZ', 
heading_content:[{'p1':'abc..'},{'p2':'asfd..'},{'p3':'ehr..'}]
}] 
"""

import fitz
import re
import json
doc = fitz.open("RAMA.pdf")

# (?<=\n\n).*(?=\n\n) TO EXTRACT HEADINGS !!!
# [^\r\n]+((\r|\n|\r\n)[^\r\n]+)* TO EXTRACT PARAS !!!

# Regex to extract paragraphs in the Format : <spacing> Multiline Text <spacing>
regex = "[^\r\n]+((\r|\n|\r\n)[^\r\n]+)*"

for page in doc:

    # Write File contents to a Text File
    with open('Document_TEXT.txt', 'a+') as f:
        text = page.getText()
        f.write(text)
    
    # Read File to append Multiple Line Breaks for each Line Break (To separate Heading and Content for applying Regex)
    with open('Document_TEXT.txt', 'r') as f1:
        lines = f1.readlines()
        for n, i in enumerate(lines):
            if i == ' \n':
                lines[n] = '\n\n\n'
    
    # Replace File Content with Newly Added Lines
    with open('Document_TEXT.txt', 'w') as f2:
        f2.writelines(lines)


with open('Document_TEXT.txt', 'r') as f3:
    content = f3.read()

# Search for Entire Content of Each Heading
matches = re.finditer(regex, content, re.MULTILINE)
headingsList = []
headingContentsList = []

para = ''
Json = {}
paraDict = {}
paraList = []
headingContentDict = {}
headingContent = []

# Extract Each Heading's Entire Content and Save in a new Text File
for matchNum, match in enumerate(matches, start=1):

    # Considering TEXT LENGTH LESS THAN 100 characters to be HEADINGS.
    if len(match.group())<100:
        headingsList.append(match.group())

    # In this case, this does not affect individual paras under the same heading as individual paras are not
    # separated by a NEWLINE delimiter.
    if len(match.group())>100:
        headingContentsList.append(match.group())

hNo = 1
# Add Line Breaks to split Each paragraph in File
for j in range(0, len(headingContentsList)):
    contentLines = headingContentsList[j].split('\n')
    pNo = 1
    for i in range(0,len(contentLines)):
        
        # Assumption: Lines with less than 60 character is the last line of it's PARA.
        if len(contentLines[i]) > 60:
            para = para + ' ' + contentLines[i]
        else:
            para = para + ' ' + contentLines[i]
            paraDict['paragraph_id'] = pNo
            paraDict['paragraph_content'] = para
            dictionary_copy = paraDict.copy()  # As Dictionary are reference based, values cannot be assigned directly
            paraList.append(dictionary_copy)
            para = ''
            pNo = pNo + 1
    
    # The below is under assumption that "headingsList" has the same number of values
    # as "headingContentsList". If below throws error, possible reason is because 
    # of the above assumptions as below: 
    # (1) Paras under same heading's content DOES NOT have a LINE BREAK
    # (2) Headings length is under 100 characters
    
    headingContentDict = {'heading_id': hNo, 'heading_name':headingsList[j],'heading_content': paraList}
    headingDictionary_copy = headingContentDict.copy() # As Dictionary are reference based, values cannot be assigned directly
    headingContent.append(headingDictionary_copy)
    paraList = []
    hNo = hNo + 1

json_object = json.dumps(headingContent, ensure_ascii=False, indent = 4).encode('utf8')

with open('Document_JSON.json', 'a+') as f:
    f.write(json_object.decode())




