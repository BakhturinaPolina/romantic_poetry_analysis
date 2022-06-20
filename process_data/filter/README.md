# Description

Try to approximate which lines of text are poetry, and remove non-conforming lines. This method is not perfect, but it will remove most of the non-poetry lines, which is good enough for our purposes.
 
* Takes a list of strings `.json` and outputs a list of strings `.json` with the "non-poetry" lines removed.

# To run
* `python3 filter_out_non_poetry_lines.py input.json` will output `input_filtered.json`.

# Example
* `input.json` is included as sample input.
* `input_filtered.json` is included as sample output.