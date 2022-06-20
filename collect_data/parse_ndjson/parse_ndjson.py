# https://github.com/aparrish/gutenberg-poetry-corpus

# The dataset is in gzipped newline delimited JSON format: there's a JSON object on each line. The following cell will
# read in the file and create a list `all_lines` that contains all of these JSON objects.

import gzip
import json

all_lines = [
    json.loads(line.strip()) for line in gzip.open(
        "/home/polina/PycharmProjects/romanticpoetry_OCR/gutenberg-poetry-v001.ndjson.gz"
    )
]

poetry_lines = [line['s'] for line in all_lines]  # extract only lines with poetry text

with open('general_poetry.json', 'w') as fp:  # create new json file for all poetry lines
          json.dump(poetry_lines, fp, indent=2)
