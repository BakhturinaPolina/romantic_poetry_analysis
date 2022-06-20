# Description
Preprocess (lemmatize, tokenize, lowercase, remove punctuation and stop-words) a list of strings.

# To run
* Install deps: `pip install stanfordcorenlp spacy nltk ijson`
* Run a StanfordCoreNLP server: 
  * `curl -O -L http://nlp.stanford.edu/software/stanford-corenlp-latest.zip`
  * `unzip stanford-corenlp-latest.zip`
  * `cd stanford-corenlp-4.1.0`
  * (optional, if `java` not installed on your machine) (Ubuntu) `sudo apt install default-jre`
  * `java -mx4g -cp "*" edu.stanford.nlp.pipeline.StanfordCoreNLPServer -annotators "tokenize,ssplit,pos,lemma,parse,sentiment" -port 9000 -timeout 15000 -memory 8g
  `
* `python3 preprocess.py input.json`

# Example
* `input.json` is included as sample input.
* `input_preprocessed.json` is included as sample output.