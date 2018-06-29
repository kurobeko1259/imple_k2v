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
        end = min(len(token_list), pos+window_size+1)
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

def calc_outedge(cooccurrence_matrix):
    tmp = cooccurrence_matrix.T
    outedge = [0 for x in range(tmp.shape[0])]

    i = 0
    for x in tmp:
        for y in x:
            if y != 0:
                outedge[i] += 1
        i += 1

    return outedge

def calc_weight(sim, coo, outedge):
    weight = sim * coo
    weight = weight.T

    i = 0
    while i != len(weight):
        weight[i] = weight[i]/outedge[i]
        i += 1

    weight = weight.T

    return weight

def calc_cossim(vec1, vec2):
    vec1_norm = np.linalg.norm(vec1)
    vec2_norm = np.linalg.norm(vec2)

    return vec1.dot(vec2.T) / vec1_norm / vec2_norm

def calc_pmi(cooccurrence_matrix, bow, length):
    pmi = np.zeros((len(bow), len(bow)))
    for i in range(len(bow)):
        for j in range(len(bow)):
            if cooccurrence_matrix[i][j] != 0:
                x = cooccurrence_matrix[i][j] * length / bow[i] / bow[j]
                pmi[i][j] = math.log2(x)

    return pmi

def calc_thesis_vec(word_vec_list):
    thesis_vec = [0 for x in range(len(word_vec_list[0]))]

    for vec in word_vec_list:
        thesis_vec += vec

    return thesis_vec

def pagerank(W, M, d=0.85):
    n = len(W)
    P = np.matrix([1./n]*n).T
    W = np.reshape(W, (n,1))
    prev_P = P

    while np.linalg.norm(P - prev_P) < 0.001:
        prev_P = P
        P = (1 - d) * W + d * M.dot(P)

    return P

def topn_ranking(dict, n):
    sorted_dict = sorted(dict.items(), key=lambda x: -x[1])
    i = 0
    ranking = {}
    for word, value in sorted_dict:
        if i >= n:
            break
        else:
            ranking.setdefault(word, value)
            i += 1

    return ranking