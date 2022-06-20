import json
import re
import sys


def clean(s):
          """removes leading numbers and trailing numbers with whitespace"""
          match = re.search(r"( {3,}\d+\.?)$", s)
          if match:
                    s = s[:match.start()]
          s = re.sub(r"\[\d+\]", "", s)
          return s


# Criteria for determining if a line of text is a line of  "poetry." each function receives the text of the line
# to check along with the text of the previous line. all checks must succeed for the line to be included.

checks = {
          # between five and sixty-five characters (inclusive)
          'length': lambda prev, line: 5 <= len(line) <= 65,
          # not all upper-case
          'case': lambda prev, line: not (line.isupper()),
          # doesn't begin with a roman numeral
          'not_roman_numerals': lambda prev, line: \
                    not (re.search("^[IVXDC]+\.", line)),
          # if the last line was long and this one is short, it's probably the end of
          # a paragraph
          'not_last_para_line': lambda prev, line: \
                    not (len(prev) >= 65 and len(line) <= 65),
          # less than 25% of the line is punctuation characters
          'punct': lambda prev, line: \
                    (len([ch for ch in line if ch.isalpha() or ch.isspace()]) / \
                     (len(line) + 0.01)) > 0.75,
          # doesn't begin with a bracket (angle or square)
          'no_bracket': lambda prev, line: \
                    not (any([line.startswith(ch) for ch in '[<'])),
          # isn't in title case
          'not_title_case': lambda prev, line: not (line.istitle()),
          # isn't title case when considering only longer words
          'not_mostly_title_case': lambda prev, line: \
                    not (" ".join([w for w in line.split() if len(w) >= 4]).istitle()),
          # not more than 50% upper-case characters
          'not_mostly_upper': lambda prev, line: \
                    (len([ch for ch in line if ch.isupper()]) / (len(line) + 0.01)) < 0.5,
          # doesn't begin or end with a digit
          'not_number': lambda prev, line: \
                    not (re.search("^\d", line)) and not (re.search("\d$", line)),

}


with open(f"{sys.argv[1]}", 'r') as j:
          contents = json.loads(j.read())


          # Returns True if the provided string is poetry (i.e. passed the defined checks)
          def line_is_poetry(line):
                    line = clean(line.strip())

                    check_results = {k: v("", line) for k, v in checks.items()}

                    return all(check_results.values())


          # Receives a list of strings, returns a list of strings which passed the poetry filter
          def filter_poetry_lines(lines):
                    poetry_lines = []
                    non_poetry_lines = []

                    for line in lines:

                              if line_is_poetry(line):
                                        print(f"✅: {line}")
                                        poetry_lines.append(line)
                              else:
                                        print(f"❌: {line}")
                                        non_poetry_lines.append(line)

                    print(f"🤖 Removed {len(non_poetry_lines)} of {len(lines)} lines")

                    return poetry_lines


          lines = contents

          poetry_lines = filter_poetry_lines(lines)

          with open(f'{sys.argv[1].split(".")[0]}_filtered.json', 'w+') as f:
                    json.dump(poetry_lines, f, indent=2)
