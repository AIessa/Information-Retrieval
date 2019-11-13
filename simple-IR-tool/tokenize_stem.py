"""
Functions to tokenize, remove stopwords & stem, can be imported from other .py

-tokenizeText(data)
-removestops(tokenized)
-stem_tokens(tokens)

"""
import sys
import re
from nltk.stem import PorterStemmer


#TOKENIZE
def tokenizeText(data):
    tokens = data.lower()
    tokens = tokens.replace("-"," ")
    tokens = tokens.replace("\'"," . ")
    tokens = re.findall("[A-Z]{2,}(?![a-z])|[A-Z][a-z]+(?=[A-Z])|[\'\w\-]+",tokens)
    return tokens


#REMOVE STOPWORDS
def removestops(tokenized):
	stopwords=[]
	with open('englishST.txt', 'r') as f:
		for line in f:
			stopwords.append(line.replace("\n","").replace("\r",""))
	nostops=[]
	for token in tokenized:
		#removing stopwords and "ft"
		if not(token in stopwords) and not(token == 'ft'):
			nostops.append(token)
	return nostops


#STEMMING
def stem_tokens(tokens):
	ps = PorterStemmer()
	stemmed=[]
	for token in tokens:
		stem = ps.stem(token)
		# ADDED exception to get "east" separated
		if bool(re.search("east",stem)) and not(stem=='easter') and not(bool(re.match("[a-z]east",stem))):
			if bool(re.match("[a-z]+east",stem)):
				tok1 = stem.replace("east","")
				tok2 = "east"
				stemmed.append(ps.stem(tok1))
				stemmed.append(ps.stem(tok2))
			elif bool(re.match("east[a-z]*",stem)):
				tok1 = "east"
				tok2 = stem.replace("east","")
				stemmed.append(ps.stem(tok1))
				if not(tok2=="ern"):
					stemmed.append(ps.stem(tok2))
		else:
			stemmed.append(stem)
	return stemmed



