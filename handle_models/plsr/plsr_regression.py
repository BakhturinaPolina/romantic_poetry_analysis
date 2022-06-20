import json
import numpy as np
from sklearn.cross_decomposition import PLSRegression
import utils


def mk_training_matrices(pairs, epub_dimension, ocr_dimension, epub_space, ocr_space):
          epub_mat = np.zeros((len(pairs), epub_dimension))
          ocr_mat = np.zeros((len(pairs), ocr_dimension))
          relevant_pairs_len = 0
          for c, p in enumerate(pairs):
                    try:
                              borked, correct = p.split("	")
                              epub_mat[c] = epub_space[correct]
                              ocr_mat[c] = ocr_space[borked]
                              relevant_pairs_len += 1
                    except KeyError:
                              pass  # no embedding for a word in pairs.txt, ignore it...
          print(f"Trained on {relevant_pairs_len} pairs")
          return epub_mat, ocr_mat


def PLSR(mat_source, mat_target, ncomps):
          plsr = PLSRegression(n_components=ncomps)
          plsr.fit(mat_source, mat_target)
          return plsr


results = []


def handle(ncomps, nns, verbose):
          '''Read semantic spaces'''
          epub_space = utils.readDM("data/epub_200.dm")
          ocr_space = utils.readDM("data/ocr_400.dm")

          '''Read all word pairs'''
          all_pairs = []
          with open("data/pairs.txt") as f:
                    for l in f:
                              l = l.rstrip('\n')
                              l = l.split(
                                        "	")  # tab is used to separate entries, as some entries might have spaces e.g. "therewas > there was"
                              l.pop()  # Remove the popularity index from pairs.txt
                              l = "	".join(l)
                              all_pairs.append(l)
          '''Make training/test fold'''
          # Because not all word present in pairs.txt exist in our models, we select a larger range to yield reasonable
          # amount of pairs. The pairs are sorted from most popular descending.
          training_pairs = all_pairs[:1000]  # will yield 109 pairs
          test_pairs = all_pairs[1001:5000]  # will yield 105 pairs

          '''Make training/test matrices and get PLSR model'''
          epub_mat, ocr_mat = mk_training_matrices(training_pairs, 200, 400, epub_space, ocr_space)
          plsr = PLSR(ocr_mat, epub_mat, ncomps)

          ''' Predict with PLSR'''
          score = 0
          relevant_pairs_len = 0  # count how many pairs were present in our models
          for p in test_pairs:
                    try:
                              borked, correct = p.split("	")
                              predicted_vector = plsr.predict(ocr_space[borked].reshape(1, -1))[0]
                              relevant_pairs_len += 1  # will throw before reaching this line, so we know this pair was used
                              nearest_neighbours = utils.neighbours(epub_space, predicted_vector, nns)
                              if correct in nearest_neighbours:
                                        score += 1
                                        if verbose:
                                                  print(borked, correct, nearest_neighbours, "1")
                              elif verbose:
                                        print(borked, correct, nearest_neighbours, "0")
                    except KeyError:
                              pass  # no embedding for a word in pairs.txt, ignore it...

          result = f"nns: {nns} & ncomps: {ncomps} = {score / relevant_pairs_len} ({score}/{relevant_pairs_len})"
          results.append(result)  # write the score to the list of results for easy comparison
          print("Precision PLSR:", result)


for nns in range(3, 6):
          for ncomps in range(10, 13):
                    print(f"Running for {nns} nns & {ncomps} ncomps")
                    handle(ncomps, nns, True)

print(json.dumps(results, indent=2))
