from pathlib import Path
import json
import xml.etree.ElementTree as ET
import os

text = []

# Will navigate down any number of subdirs until it reaches an .xml file, which will then be processed.
def extract_text_from_xml(rootdir):
          for path in Path(rootdir).iterdir():  # iterate though all subdirs in rootdir
                    if path.is_dir():
                              extract_text_from_xml(path)  # call this function on the subdir
                    if path.is_file() and Path(path).suffix == '.xml':
                              print(f"Parsing {path}...")
                              tree = ET.parse(path) # create XML element tree from the file
                              root = tree.getroot() # get element tree root
                              # The file structure has the words inside CONTENT attribute of a String tag, which is contained within the TextLine tag
                              for TextLine in root.iter('TextLine'): # find all TextLine tags in the tree
                                  line_words_list = []
                                  for String in TextLine.findall('String'): # find all String tags inside the TextLine tag
                                      word = String.get("CONTENT") # extract the word stored in the CONTENT attribute
                                      line_words_list.append(word) # add the word to the list of words from the line
                                  joined_line = " ".join(line_words_list) # join the list of words into a string
                                  # Only add strings over 40 char length, to avoid adding some of the weird non-text lines
                                  if len(joined_line) > 40:
                                      text.append(joined_line)

root = os.getcwd()
source_dir = f"{root}/input"
extract_text_from_xml(source_dir)

with open('newspaper_lines.json', 'w+') as fp:
          json.dump(text, fp, indent=4, sort_keys=False)
                              
