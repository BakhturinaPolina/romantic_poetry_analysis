from ebooklib import epub, ITEM_DOCUMENT
from bs4 import BeautifulSoup, Tag
from pathlib import Path
import json
import os

output = []

# Expected directory structure:
# rootdir
#         author_name_dir
#                   book.epub

# This is a recursive function, which will enter folder, iterate over contents, if the content is a subfolder,
# it will call itself again on that subfolder, i.e. iterate over contents. If the contet is a file,
# which we expect to be an epub, process it.
def extract_poems_from_epubs(rootdir):
          for path in Path(rootdir).iterdir():  # iterate though all subdirs in rootdir
                    if path.is_dir():
                              extract_poems_from_epubs(path)  # call this function on the subdir
                    if path.is_file():
                              # read content from each book in a subdir using ebooklib module
                              book = epub.read_epub(path)
                              # Exctract chapters with .get_items_of_type method of epub, and map them to chapters list
                              chapters = list(
                                        book.get_items_of_type(ITEM_DOCUMENT))
                              # This part of the code is optional and needed to log which book is being proccesed.
                              author_name = Path(rootdir).stem
                              print(f"Parsing book {Path(path).stem} by {author_name}")

                              for chapter in chapters:  # apply the function "extract_poems_and_titles()" for each chapter.
                                        soup = BeautifulSoup(chapter.get_body_content(), 'html.parser')
                                        text = soup.text
                                        text_lines = text.split('\n')
                                        output.extend(text_lines)


rootdir = os.getcwd()
extract_poems_from_epubs(f"{rootdir}/input")

# Open new json file in a writing mode (i.e. create) and add write `output` to it.
with open('text_lines.json', 'w') as fp:
          json.dump(output, fp, indent=2)
