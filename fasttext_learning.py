import fasttext

model = fasttext.skipgram(input_file="./data/corpus.txt", output="./data/model", ws=5, dim=100, epoch=10)

vocabulary = model.words

print(list(vocabulary))
