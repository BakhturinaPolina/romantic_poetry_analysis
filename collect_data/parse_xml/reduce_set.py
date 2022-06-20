import os
import json
import random

root = os.getcwd()

file = open(f"{root}/newspaper_lines.json", 'r')

contents = json.loads(file.read())

output = random.sample(contents, 1000000)

with open('newspaper_lines_reduced.json', 'w+') as fp:
          json.dump(output, fp, indent=4, sort_keys=False)

