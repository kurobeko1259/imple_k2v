from gensim.models import FastText
import function
import numpy as np
import preprocess


def rank_candidate(thesis_sentence, document):
    model = FastText.load_fasttext_format("./data/model.bin")

    #tokens = preprocess.preprocess(document)
    tokens = document

    vocabulary, cooccurrence_matrix = function.create_cooccurrence_matrix(tokens, 2)

    sim = [[0 for x in range(len(vocabulary))] for x in range(len(vocabulary))]

    for word,index in vocabulary.items():
        for word2, index2 in vocabulary.items():
            if index == index2:
                continue

            sim[index][index2] = model.similarity(word, word2)

    bow = function.tok2bow(tokens, vocabulary)
    pmi = function.calc_pmi(cooccurrence_matrix.toarray(), bow, len(tokens))

    outedge = function.calc_outedge(cooccurrence_matrix.toarray())

    M = function.calc_weight(sim, pmi, outedge)

    #title_tokens = preprocess.preprocess(thesis_sentence)
    title_tokens = thesis_sentence

    title_vec_list = [model[token] for token in title_tokens]
    thesis_vec = function.calc_thesis_vec(np.array(title_vec_list))
    word_thesis_sim = []

    for word in vocabulary.keys():
        word_thesis_sim.append(function.calc_cossim(thesis_vec, model[word]))

    rank_value = function.pagerank(np.array(word_thesis_sim), np.array(M), 0.85)

    rank_dict = {}

    for candidate, index in vocabulary.items():
        rank_dict.setdefault(candidate, rank_value[index])

    return rank_dict

documents = []
with open("./data/corpus.txt", "r") as f:
    line = f.readline()

    while line:
        documents.append(line)
        line = f.readline()

j = 0
while j != len(documents):
    i = 0
    while documents[j][i] == " ":
        i += 1
    documents[j] = documents[j][i:].split(" ")
    j += 1



thesis_sentences = []
with open("./data/corpus_lbl.txt", "r") as f:
    line = f.readline()

    while line:
        thesis_sentences.append(line)
        line = f.readline()

j = 0
while j != len(thesis_sentences):
    i = 0
    while thesis_sentences[j][i] == " ":
        i += 1
    thesis_sentences[j] = thesis_sentences[j][i:].split(" ")
    j += 1

titles = []
with open("./data/arxiv_lbl.txt", "r") as f:
    line = f.readline()

    while line:
        titles.append(line)
        line = f.readline()

crude_documents = []
with open("./data/arxiv.txt", "r") as f:
    line = f.readline()

    while line:
        crude_documents.append(line)
        line = f.readline()

document_index = 20000

ranking = function.topn_ranking(rank_candidate(thesis_sentences[document_index][:-1], documents[document_index][:-1]), 5)


print(titles[document_index])
print(crude_documents[document_index])
for word, value in ranking.items():
    print(word + "\t\t\t\t\t" + ":" + str(float(value)))
