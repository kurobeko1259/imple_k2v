from gensim.models import FastText
model = FastText.load_fasttext_format("model.bin")


for token in model.most_similar("machine_learning"):
    print(token)