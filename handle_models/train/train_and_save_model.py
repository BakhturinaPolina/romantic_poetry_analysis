import json
import logging
from gensim.models.word2vec import Word2Vec

logging.basicConfig(format="%(levelname)s - %(asctime)s: %(message)s", datefmt='%H:%M:%S', level=logging.INFO)

import os

root = os.getcwd()

input_file = open(f"{root}/input.json", 'r')
poetry_list = json.loads(input_file.read())

w2v_model = Word2Vec(sentences=poetry_list, min_count=10, vector_size=400)

wv = w2v_model.wv

print(wv.most_similar(positive=["death"]))

# Save model to be loaded with Word2VecLater
w2v_model.save('MODEL_NAME.model')

# Save model as plaintext that can be manually parsed later
wv.save_word2vec_format("MODEL_NAME.dm")
