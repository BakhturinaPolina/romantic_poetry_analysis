from ebooklib import epub, ITEM_DOCUMENT
from bs4 import BeautifulSoup, Tag
from pathlib import Path
import json
import os

poems = {}  # This is an empty object where all poetry text will be stored. Here it's used for creating our final
# json file for Romantic Poetry dataset, which will be structured in a following way:
# {Author's name: {poem's title: "text of the poem"}}.

# This function is aimed to extract all poetry text with titles from our html source.
def extract_poems_and_titles(chapter, author_name):
          # Here I'm putting the `chapter` object I need to parse into BeautifulSoup constructor. Function "get_body_content"
          # returns book content, which is then parsed by BS using the HTML parser (epub format stores data in HTML).
          soup = BeautifulSoup(chapter.get_body_content(), 'html.parser')
          # The primary hypothesis here is that all poems are stored between headers, therefore we need to find all
          # tags for headers in our html, which are coded as <h2>
          for header in soup.find_all('h2'):

                    nextNode = header  # This is a specified Node object, which will be used for navigating through
                    # the text. In our case, we need to navigate from one header to another one and getting all in
                    # between, including the header itself.
                    full_text_array = []  # creating an empty list where all poetry text for each poem will be stored

                    # This function extracts the poem title from the header, which is used as a key, and assigns the text of the poem
                    # as a value.
                    def write_result_to_poems():
                              # Extracting poem title from header:
                              #         1. Use BS get_text() method to get the string from the tag
                              #         2. Use python's strip() method to remove spaces
                              #         3. Convert to upper case for uniformity
                              parsed_header = header.get_text(
                                        strip=True).strip().upper()

                              # The hasattr() function returns True if the specified object has the specified
                              # attribute. If the object `poems[author_name]` doesn't have an attribute
                              # `parsed_header` and if `full_text_array` is not empty, then the divided text of the
                              # poem which is stored as elements of the `full_text_array` is joined into a single
                              # string, and this string is assigned to the object poems[authors_name] as a value of
                              # the key `parsed_header`.
                              if not hasattr(
                                      poems[author_name],
                                      parsed_header
                              ) and full_text_array:
                                        joined_text = ' '.join(full_text_array)
                                        poems[author_name][parsed_header] = joined_text

                    while True:
                              # Depending on what's the next node, which we know by looking at nextSibling,
                              # we do different things:
                              #         1. If the next node is null, which means we've reached the end of the document, we write
                              #         all the collected text to `poems`
                              #         2. If it's an HTML tag, depending on what the tag is, we either:
                              #                   1. If the next tag is a header, we write the collected text to `poems`
                              #                   2. If it's something else, we extract the text, and append it to `full_text_array`
                              nextNode = nextNode.nextSibling
                              if nextNode is None:
                                        write_result_to_poems()
                                        break
                              # Each book is formatted in a different way. Generally, we expect the poem text to be contained
                              # between HTML header tags, i.e. h1, h2, h3, etc. While this is not perfect approach, as
                              # in some books a poem (rarely) would be contained between <p> tags, or some other, this should extract most
                              # of the poems from most of the books.
                              if isinstance(nextNode, Tag):  # check that nextSibling is an HTML tag
                                        if "h" in nextNode.name:  # if the tag name contains "h", its most likely a header tag
                                                  write_result_to_poems()  # that means, we've reached the end of this poem, so we write it to `poems`
                                                  break
                                        else:  # if it's not a header tag, then it's probably our poem text
                                                  parsed = nextNode.get_text(
                                                            strip=True).strip()  # extract truncated string from the tag
                                                  if len(parsed) > 0:  # if it's not empty, append to our collection of extracted strings for this poem
                                                            full_text_array.append(parsed)


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
                              # If this is a directory, we extract the author's name by using .stem,
                              # initiate an author object in `poems`, and navigate into the folder.
                              author_name = Path(
                                        path).stem  # .stem returns the last element of the path, which in our case is author name
                              poems[author_name] = {}
                              extract_poems_from_epubs(path)  # call this function on the subdir
                    if path.is_file():
                              # read content from each book in a subdir using ebooklib module
                              book = epub.read_epub(path)
                              # Extract chapters with .get_items_of_type method of epub, and map them to chapters list
                              chapters = list(
                                        book.get_items_of_type(ITEM_DOCUMENT))
                              # This part of the code is optional and needed to log which book is being processed.
                              author_name = Path(rootdir).stem
                              print(f"Parsing book {Path(path).stem} by {author_name}")

                              for chapter in chapters:  # apply the function "extract_poems_and_titles()" for each chapter.
                                        extract_poems_and_titles(chapter, author_name)


rootdir = os.getcwd()
extract_poems_from_epubs(f"{rootdir}/input")

# Open new json file in a writing mode (i.e. create) and add write `poems` to it. "Sort_keys=False" means that our
# poems will be sorted in the same order as they were originally extracted from a book, not in alphabetical order.
with open('structured_poems.json', 'w') as fp:
          json.dump(poems, fp, indent=2)
