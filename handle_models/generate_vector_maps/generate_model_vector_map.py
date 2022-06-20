from gensim.models.word2vec import Word2Vec
import pprint
from sklearn.manifold import TSNE
import matplotlib.pyplot as plt
import matplotlib.cm as cm

pp = pprint.PrettyPrinter(indent=4)
import numpy as np

newspapers_model = Word2Vec.load('newspapers.model')
romantic_poetry_model = Word2Vec.load('romantic_poetry.model')
general_poetry_model = Word2Vec.load('general_poetry.model')


models = {"Romantic Poetry": romantic_poetry_model, "General Poetry": general_poetry_model, "Newspapers": newspapers_model}

def tsne_plot_2d(label, embeddings, words=[], a=1):
    plt.figure(figsize=(16, 9))
    colors = cm.rainbow(np.linspace(0, 1, 1))
    x = embeddings[:,0]
    y = embeddings[:,1]
    plt.scatter(x, y, c=colors, alpha=a, label=label)
    for i, word in enumerate(words):
        plt.annotate(word, alpha=0.3, xy=(x[i], y[i]), xytext=(5, 2),
                     textcoords='offset points', ha='right', va='bottom', size=10)
    plt.legend(loc=4)
    plt.grid(True)
    plt.savefig(f"{label}.png", format='png', dpi=150, bbox_inches='tight')
    plt.show()

for model_name, model in models.items():
          words_ak = []
          embeddings_ak = []
          for word in list(model.wv.index_to_key):
                    embeddings_ak.append(model.wv[word])
                    words_ak.append(word)

          tsne_ak_2d = TSNE(perplexity=30, n_components=2, init='pca', n_iter=3500, random_state=32)
          embeddings_ak_2d = tsne_ak_2d.fit_transform(embeddings_ak)
          tsne_plot_2d(model_name, embeddings_ak_2d, a=0.1)
