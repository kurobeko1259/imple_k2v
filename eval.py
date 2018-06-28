from gensim.models import FastText
import function
model = FastText.load_fasttext_format("./data/model.bin")


for token in model.most_similar("machine"):
    print(token)

tokens = ["I", "am", "a", "soccer", "fan", "and", "I", "am", "also", "a", "basketball", "fan"]
print(tokens)
vocabulary, cooccurrence_matrix = function.create_cooccurrence_matrix(tokens, 3)
bow = function.tok2bow(tokens, vocabulary)
print(vocabulary)
print(cooccurrence_matrix.toarray())
print(bow)
pmi = function.calc_pmi(cooccurrence_matrix.toarray(), bow, len(tokens))
print(pmi)