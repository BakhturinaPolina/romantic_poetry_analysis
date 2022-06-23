import json
from gensim.models.word2vec import Word2Vec
import spacy

spacy_client = spacy.load('en_core_web_sm')
all_stopwords = spacy_client.Defaults.stop_words

newspapers_model = Word2Vec.load('newspapers.model')
romantic_poetry_model = Word2Vec.load('romantic_poetry.model')
general_poetry_model = Word2Vec.load('general_poetry.model')

models = {"Romantic Poetry": romantic_poetry_model, "General Poetry": general_poetry_model,
          "Newspapers": newspapers_model}

top_words = {}

for model_name, model in models.items():
          top_words_model = model.wv.index_to_key[:300]  # Get top 300 words descending by popularity
          top_words[model_name] = [
                    word for word in top_words_model
                    if len(word) > 2 and word not in all_stopwords and word not in ['thy', 'thou']
          ]  # Filter out stop words


# Find common elements inside lists, and return a list of common elements
def common_elements(list_of_lists):
          result = set(list_of_lists[0])
          for currSet in list_of_lists[1:]:
                    result.intersection_update(currSet)

          return list(result)


common_top_words = common_elements([value for key, value in top_words.items()])

output = []

# Create output which can be later converted to table
for top_word in common_top_words:
          entry = {"word": top_word}
          for model_name, model in models.items():
                    entry[model_name] = model.wv.most_similar(positive=[top_word]) # Get most_similar words for each top word
          output.append(entry)

print(json.dumps(output, indent=2))

with open('top_words_most_similar.json', 'w') as fp:
          json.dump(output, fp, indent=2, sort_keys=False)
