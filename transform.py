import preprocess
import copy

document = []

label = []

with open("./data/arxiv.txt", "r") as f:
    line = f.readline()
    while line:
        vocab = []
        vocab = line.split("|")

        vocab[0] = int(vocab[0])

        if len(vocab) > 2:
            x = ""
            i = 1
            for i in range(len(vocab)):
                x += str(vocab[i])
            vocab[1] = x

            del vocab[2:]

        document.append(copy.deepcopy(vocab))
        line = f.readline()

with open("./data/arxiv_lbl.txt", "r") as g:
    line = g.readline()
    while line:
        vocab = []
        vocab = line.split("|")

        vocab[0] = int(vocab[0])

        if len(vocab) > 3:
            x = ""
            i = 2
            for i in range(len(vocab)):
                x += str(vocab[i])
            vocab[2] = x

            del vocab[3:]

        label.append(copy.deepcopy(vocab))
        line = g.readline()

doc = []

i = 0
for token in label:
    i += 1
    doc.extend(preprocess.preprocess(token[2]))

i = 0
while i != len(doc):
    doc[i] = doc[i].replace(" ", "_")
    i += 1

doc = ' '.join(doc)
with open("corpus_lbl.txt", "a") as f:
    f.write(doc)