from scipy import sparse
import math
import numpy as np

def create_cooccurrence_matrix(token_list, window_size):
    vocabulary = {}
    data = []
    row = []
    col = []
    for pos,token in enumerate(token_list):
        i = vocabulary.setdefault(token,len(vocabulary))
        start = max(0, pos - window_size)
        end = min(len(token_list), pos+window_size)
        for pos2 in range(start, end):
            if pos2 == pos:
                continue

            j = vocabulary.setdefault(token_list[pos2], len(vocabulary))
            data.append(1.)
            row.append(i)
            col.append(j)
    cooccurrence_matrix = sparse.coo_matrix((data, (row, col)))
    return vocabulary, cooccurrence_matrix

def tok2bow(token_list, vocabulary):
    data = [0 for x in range(len(vocabulary))]

    for word, index in vocabulary.items():
        for token in token_list:
            if word == token:
                data[index] += 1

    return data

def calc_pmi(cooccurrence_matrix, bow, length):
    pmi = np.zeros((len(bow), len(bow)))
    for i in range(len(bow)):
        for j in range(len(bow)):
            if cooccurrence_matrix[i][j] != 0:
                x = cooccurrence_matrix[i][j] * length / bow[i] / bow[j]
                pmi[i][j] = math.log2(x)

    return pmi