# Description
Extract text from EPUB using `BeautfifulSoup`. 
* `parse_all_text_from_epub.py` will output all lines of the book in a list.
* `parse_structured_text_from_epub.py` will try to output the poems in structured format. It tries to extract all text between two headers, and use the first headers as the title and the text as the content. However, as the formatting of EPUBs is extremely inconsistent, there maybe be errors using this approach.

# To run
* Install deps: `pip install ebooklib`
* Launch file: `python3 parse_all_text_from_epub.py` or `python3 parse_structured_text_from_epub.py`

# Example
* `/input` is included as sample input.
* `text_lines.json` and `structured_poems.json` are included as sample output.