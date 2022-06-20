import json
import os
import re
import ijson
import nltk
import spacy
import string  # Import a string of punctuation and digits to remove. That includes !”#$%&\’()*+,-./:;<=>?@[\\]^_`{|}~’ and all numbers.
import sys
from stanfordcorenlp import StanfordCoreNLP

# Load the English Language Model of Spacy.
spacy_client = spacy.load('en_core_web_sm')
# Here I'm going to remove personal pronouns from `nlp.Defaults.stop_words`. They will be needed for the further text analysis.
spacy_client.Defaults.stop_words -= {'i', 'you', 'he', 'she', 'it', 'we', 'they', 'me', 'him', 'her', 'us', 'them'}
spacy_client.Defaults.stop_words |= {"'", "-", "‘", "“", "««"}
all_stopwords = spacy_client.Defaults.stop_words

nltk.download('punkt', quiet=True)  # download the most recent punkt package

# Standford CoreNLP is chosen for lemmatization of all tokens in our sample both because it's better in performing
# the task comparing with the standard NLTK Lemmatizer, and because it's able to preprocess pronouns (they will be
# highly needed in future analysis) comparing with high-quality Spacy Lemmatizer.

# Connect to the CoreNLP server we just started.

nlp = StanfordCoreNLP('http://localhost', port=9000, timeout=15000, memory='8g')

# Define properties needed to get lemma.

props = {'annotators': 'lemma',
         'pipelineLanguage': 'en',
         'outputFormat': 'json'}

# Our dataset is too bit to process at once. So the file will be open while the JSON parser is reading from
# the file on demand, iterating over the records. The items() takes a query string that tells which part
# of the record to return. In this case, "item" just means “each item in the top-level list we’re iterating over”

final_text_for_vocabulary = []

root = os.getcwd()

file = open(sys.argv[1], 'r')

for record in ijson.items(file, "item"):
          try:
                    # Apply a tokenizer optimized for English as provided by the Natural Language ToolKit (NLTK), and segment each
                    # document in corpus into a list of word tokens:

                    record = re.sub(r'[^A-Za-z \']+', '', record)
                    record = re.sub('\s+', ' ', record)

                    tokens = nltk.tokenize.word_tokenize(record, language='english')

                    # Given the current word segmentation, removing isolated punctuation marks can be accomplished by filtering
                    # non-punctuation tokens.
                    # This is the 3-argument version of str.maketrans with arguments (x, y, z):
                    #      (I) 'x' and 'y' must be equal-length strings;
                    #      (II) characters in 'x' are replaced by characters in 'y'.
                    #      (III)'z' is a string where each character in the string is mapped to None (`exitlist` here)
                    exclist = (
                            string.punctuation + string.digits)  # remove any character that is in string.punctuation and string.digits.
                    table_ = str.maketrans('', '', exclist)
                    no_punkt_poetry = record.translate(table_)

                    # The functions lower() returns the string by converting all the characters of the string to lower case.
                    tokenized_poetry_lower = no_punkt_poetry.lower()

                    # The lemma is embedded in the output of the annotate() method of the StanfordCoreNLP connection object
                    parsed_str = nlp.annotate(tokenized_poetry_lower, properties=props)
                    # The output of `nlp.annotate()` is converted to a dictionary using json.loads
                    parsed_dict = json.loads(parsed_str)
                    # Extract the lemma for each word. Then form line of poetry and return it.
                    lemma_list = [d["lemma"] for d in parsed_dict['sentences'][0]['tokens']]

                    # Iterate through each word in the 'lemma_list' and if the word exists in the stop word set, the word is removed.
                    tokens_without_sw = [word for word in lemma_list if word not in all_stopwords]

                    final_text_for_vocabulary.append(tokens_without_sw)

          except Exception as e:
                    # If no text was extracted from the line, an exception will occur
                    print(e)
                    print(f"Faulty line: {record}")

with open(f'{sys.argv[1].split(".")[0]}_preprocessed.json', 'w+') as fp:
          json.dump(final_text_for_vocabulary, fp, indent=2)