# Description
Visualize `Word2Vec` Vectors in 2D plots. Maps `Wor2Vec` vectors to 2D with `TSNE` and creates an image with `matplotlib`. The idea taken from https://github.com/sismetanin/word2vec-tsne.

# To run
* Install deps: `pip install gensim sklearn matplotlib numpy`
* Place the models into this folder.
* `python3 generate_model_vector_map.py`

# Notes
* This particular code is not model-agnostic, it expects our models.
* Output images are included in `/output`