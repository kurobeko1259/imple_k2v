import spacy
import re


nlp =  spacy.load('en')

def preprocess(document):

	docs = nlp(document.lower())

	sentence = nlp(u"I am a boy, and you are crazy in school in 1990s")

	NE_list = []
	NC_list = []

	for token in docs.ents:
		digit_flag = False
		NEflag = False

		for word in token:
			if word.is_digit:

				digit_flag = True


		if not digit_flag:
			if token.label_ == "DATE" or token.label_ == "TIME" or token.label_ == "PERCENT" or token.label_ == "MONEY" or token.label_ == "QUANTITY" or token.label_ == "ORDINAL" or token.label_ == "CARDINAL":
				NEflag = True


		if not digit_flag and not NEflag:
			NE_list.append([token, token.start, token.end])

	word_list = []

	for token in docs:
		SWflag = False
		Pflag = False

		if token.is_stop:
			SWflag = True

		if not SWflag:
			if token.pos_ == "PUNCT" and not token.text == "-":
					Pflag = True

		if not SWflag and not Pflag:
			word_list.append([token, token.i, token.i])

	for token in docs.noun_chunks:
		digit_flag = False
		for word in token:
			if word.is_digit:
				digit_flag = True


		if not digit_flag:
			NC_list.append([token, token.start, token.end])

	NE_list_pro = []
	NC_list_pro = []

	for token in NE_list:
		first_offset = 0
		last_offset = None

		if len(token) >= 2:
			if token[0][0].tag_ == "AFX" or token[0][0].tag_ == "DT":
				first_offset = 1

			if token[0][-1].tag_ == "AFX" or token[0][-1].tag_ == "DT":
				last_offset = -1

			if token[0][0].pos_ == "INTJ" or token[0][0].pos_ == "AUX" or token[0][0].pos_ == "CCONJ" or token[0][0].pos_ == "ADP" or token[0][0].pos_ == "DET" or token[0][0].pos_ == "NUM" or token[0][0].pos_ == "PART" or token[0][0].pos_ == "PRON" or token[0][0].pos_ == "SCONJ" or token[0][0].pos_ == "PUNCT" or token[0][0].pos_ == "SYM" or token[0][0].pos_ == "X" or token[0][0].pos_ == "ADP":
				first_offset = 1

			if token[0][-1].pos_ == "INTJ" or token[0][-1].pos_ == "AUX" or token[0][-1].pos_ == "CCONJ" or token[0][-1].pos_ == "ADP" or token[0][-1].pos_ == "DET" or token[0][-1].pos_ == "NUM" or token[0][-1].pos_ == "PART" or token[0][-1].pos_ == "PRON" or token[0][-1].pos_ == "SCONJ" or token[0][-1].pos_ == "PUNCT" or token[0][-1].pos_ == "SYM" or token[0][-1].pos_ == "X" or token[0][-1].pos_ == "ADP":
				last_offset = -1

			if token[0][0].is_stop:
				first_offset = 1

			if token[0][-1].is_stop:
				last_offset = -1



			NE_list_pro.append([token[0][first_offset:last_offset], token[1], token[2]])

		else:
			if not token[0][0].is_stop:
				NE_list_pro.append([token[0][first_offset:last_offset], token[1], token[2]])



	for token in NC_list:
		first_offset = 0
		last_offset = None


		if len(token[0]) >= 2:
			if token[0][0].tag_ == "AFX" or token[0][0].tag_ == "DT":
				first_offset = 1

			if token[0][-1].tag_ == "AFX" or token[0][-1].tag_ == "DT":
				last_offset = -1

			if token[0][0].pos_ == "INTJ" or token[0][0].pos_ == "AUX" or token[0][0].pos_ == "CCONJ" or token[0][0].pos_ == "ADP" or token[0][0].pos_ == "DET" or token[0][0].pos_ == "NUM" or token[0][0].pos_ == "PART" or token[0][0].pos_ == "PRON" or token[0][0].pos_ == "SCONJ" or token[0][0].pos_ == "PUNCT" or token[0][0].pos_ == "SYM" or token[0][0].pos_ == "X" or token[0][0].pos_ == "ADP":
				first_offset = 1

			if token[0][-1].pos_ == "INTJ" or token[0][-1].pos_ == "AUX" or token[0][-1].pos_ == "CCONJ" or token[0][-1].pos_ == "ADP" or token[0][-1].pos_ == "DET" or token[0][-1].pos_ == "NUM" or token[0][-1].pos_ == "PART" or token[0][-1].pos_ == "PRON" or token[0][-1].pos_ == "SCONJ" or token[0][-1].pos_ == "PUNCT" or token[0][-1].pos_ == "SYM" or token[0][-1].pos_ == "X" or token[0][-1].pos_ == "ADP":
				last_offset = -1

			if token[0][0].is_stop:
				first_offset = 1

			if token[0][-1].is_stop:
				last_offset = -1


			NC_list_pro.append([token[0][first_offset:last_offset], token[1], token[2]])

		else:
			if not token[0][0].is_stop:
				NC_list_pro.append([token[0][first_offset:last_offset], token[1], token[2]])


	doc_preprocessed = []

	first_cnt = 0
	last_cnt = 0

	if len(word_list) == 0:
		return [""]

	if len(NC_list_pro) == 0:
		NE_list_pro.append(["", word_list[-1][2] + 1, word_list[-1][2] + 1])
	elif word_list[-1][2] <= NC_list_pro[-1][2] - 1:
		NE_list_pro.append(["", NC_list_pro[-1][2]+1, NC_list_pro[-1][2]+1])
	else:
		NE_list_pro.append(["", word_list[-1][2]+1, word_list[-1][2]+1])



	for token1 in NE_list_pro:
		if last_cnt == token1[1]:
			doc_preprocessed.append(str(token1[0]))
			first_cnt = token1[1]
			last_cnt = token1[2]
		else:
			while last_cnt < token1[1]:
				i = 0
				NC_flag = False
				while i != len(NC_list_pro):
					if last_cnt == NC_list_pro[i][1]:
						doc_preprocessed.append(str(NC_list_pro[i][0]))
						first_cnt = NC_list_pro[i][1]
						last_cnt = NC_list_pro[i][2]
						NC_flag = True
						break
					elif NC_list_pro[i][1] > last_cnt:
							break
					else:
						i += 1

				if not NC_flag:
					i = 0
					while i != len(word_list):
						if last_cnt == word_list[i][1]:
							doc_preprocessed.append(str(word_list[i][0]))
							first_cnt = word_list[i][1]
							last_cnt = word_list[i][2] + 1
							break
						elif last_cnt < word_list[i][1]:
							last_cnt += 1
							break
						else:
							i += 1
			if last_cnt < token1[1]:
				del doc_preprocessed[-1]

			doc_preprocessed.append(str(token1[0]))
			first_cnt = token1[1]
			last_cnt = token1[2]

	return doc_preprocessed[:-1]

def handmade_preprocess(token_list):
	i = 0
	while i != len(token_list):
		if 0 < i < len(token_list) - 1:
			if token_list[i] == '-':
				token_list[i-1] = token_list[i-1] + token_list[i] + token_list[i+1]
				del token_list[i:i+2]
				i -= 1

			if token_list[i][0] == '-' or token_list[i][0] == '\'':
				token_list[i-1] = token_list[i-1] + token_list[i]
				del token_list[i]

			if token_list[i][-1] == '-' or token_list[i][-1] == '\'':
				token_list[i] = token_list[i] + token_list[i+1]
				del token_list[i+1]

		i += 1

	return token_list
