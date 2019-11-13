
import math
from operator import itemgetter

def TFIDF(query,index,n):
	query_id = query[0]
	terms = query[1:len(query)]
	rel_docs = []
	#TERMWEIGHTING
	# N = n , number of documents in collection
	w_per_term = []#this is per document
	for term in terms:
		w = {}
		docs_of_term = index[term] #[(docID,[pos])]
		df = len(docs_of_term)
		idf = math.log10(n/df)

		#tf dep. on document
		tf = {} #number of times term appears in document
		for tupl in docs_of_term: 
			tf[tupl[0]] = len(tupl[1])
			if not(tupl[0] in rel_docs):
				rel_docs.append(tupl[0])
		
		for doc in tf:
			w[doc]=1 + math.log10(tf[doc])*idf
		
		w_per_term.append(w) # term-weights in each doc (append from this term)


	output_matrix = []
	#w_per_term has term-weights of each term.
	for doc in rel_docs:
		score = 0.0000
		for doc_weights in w_per_term: #fetch weight dictionary of term in query
			if doc in doc_weights:
				score = score + doc_weights[doc]
		vector = [query_id,0,doc,0,score,0]
		output_matrix.append(vector)

	output = sorted(output_matrix, key=itemgetter(4))
	out = output[::-1]
	return out



