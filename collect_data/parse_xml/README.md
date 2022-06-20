# Description

Extract text from XML. 
* Expects the format of the [British Library News Datasets](https://bl.iro.bl.uk/collections/353c908d-b495-4413-b047-87236d2573e3?locale=en).
* Outputs a list of strings
* `reduce_set.py` was needed because the parsed output had over 27 million lines of text, which was too much for the project, so a random sample of 1 million lines was extracted for our needs.

# To run
* `python3 parse_text_from_xmls.py`

# Example
* `/input` is included as sample input.
* `newspaper_lines.json` is included as sample output.