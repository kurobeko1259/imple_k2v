import fasttext

model = fasttext.skipgram(input_file="corpus.txt", output="model", ws=5, dim=100, epoch=10)

vocabulary = model.words

print(list(vocabulary))
