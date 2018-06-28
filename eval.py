from gensim.models import FastText
import function
model = FastText.load_fasttext_format("./data/model.bin")


for token in model.most_similar("machine"):
    print(token)

tokens = ["I", "am", "a", "soccer", "fan", "and", "I", "am", "also", "a", "basketball", "fan"]
print(tokens)
vocabulary, cooccurrence_matrix = function.create_cooccurrence_matrix(tokens, 3)

sim = [[0 for x in range(len(vocabulary))] for x in range(len(vocabulary))]

for word,index in vocabulary.items():
    for word2, index2 in vocabulary.items():
        if index == index2:
            continue

        sim[index][index2] = model.similarity(word, word2)


bow = function.tok2bow(tokens, vocabulary)
pmi = function.calc_pmi(cooccurrence_matrix.toarray(), bow, len(tokens))

outedge = function.calc_outedge(cooccurrence_matrix)

M = function.calc_weight(sim, pmi, outedge)

#要旨ベクトルの計算、要旨ベクトルとvocaburalyの類似度計算（行列）
