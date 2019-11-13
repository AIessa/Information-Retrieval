"""
These functions are used in booleansearch.py

Functions:
- FindDocs(query,index) -> returns matching documents
- MakeDocIndex(filepath) -> creates an index of document IDs with their content
- GetDocContent(docindex,docIDs) -> returns given document contents
"""

import re
from nltk.stem import PorterStemmer


def FindDocs(query,hash_index):
	#check for bool in query (assumption: can only use one AND or OR element & NOT can only appear once)
	if re.match(".+AND.+",query):
		query = query.split(" AND ")
		if re.match(".*NOT.+",query[0]):
			query = ["NOT"]+[query[0].strip("NOT")]+[query[1]]
		elif re.match(".*NOT.+",query[1]):
			query = ["NOT"]+[query[1][4:]]+[query[0]]
		else:
			query = ["AND"]+query
	elif re.match(".+OR.+",query):
		query = query.split("OR")
		query = ["OR"]+query
	elif re.match(".+NOT.+",query): #assuming query looks like income NOT taxes
		query = query.split("NOT")
		query = ["NOT"]+[query[1]]+[query[0]]
	else:
		query = ["NOBOOL"]+[query]

	#function to check further type of query (phrase or proximity)
	def querycheck(q):
		if (re.match("\".+\"",q) or re.match(".+ .+",q)) and (not re.match("#[0-9]*(.+)",q)): #check whether phrase search
			content = q.split(" ")
			q = ["PHRASE",0,[]]
			for c in content:
				if re.match(".*[a-z].*",c): #avoid " "
					q[2].append(c)
		elif re.match("#[0-9]*(.+)",q) or re.match(" #[0-9]*(.+)",q):
			if re.match(" #[0-9]*(.+)",q):
				q=q[1:]
			prox=int(re.sub('\(.*', '', q)[1:])
			content=re.sub('#[0-9]*\(', '', q)
			content=content[:len(content)-1]
			q=["PROX",prox]+[content.split(",")]
		return q

	#apply querycheck
	q = [query[0]]
	query1=querycheck(query[1])
	q.append(query1)
	if len(query)>2:
		query2=querycheck(query[2])
		q.append(query2)

	
	#query to console
	print("query: "+str(q))

	#now that query type is tagged, all terms must be shaped correctly:
	#assuming query contains no stopwords
	ps = PorterStemmer()
	def wordprep(word):
		term=word
		term = term.strip("\"") #remove leftover ""
		term = term.replace(" ","") # remove potential white spaces
		term = term.lower()
		term = ps.stem(term)
		print("searchterm:"+term)
		return term
	
	#docIDs: hash_index[ps.stem(q)]

	#FUNCTIONS FOR SIMPLE & PROXIMITY/PHRASE SEARCH:
	#simple searchfunction, no linear merge
	def searchSIMPL(q):
		q = wordprep(q) #q=ps.stem(q.replace(" ","")).lower()
		if q in hash_index:
			posting_list = hash_index[ps.stem(q).lower()]
			doclist = [doc for (doc,pos) in posting_list]
			return doclist#relevant document IDs
		else:
			print("term can't be found")
			return [] #in case term couldn't be found in index


	#proximity searchfunction, linear merge (also for phrasesearch)
	def searchPROX(q):
		# e.g. q=['PHRASE', 0, ['middle', 'east']]
		qtype = q[0] #either "PHRASE" or "PROX"
		prox = q[1]
		#retrieve postinglists of both terms:
		q1=wordprep(q[2][0]) #ps.stem(q[2][0].replace(" ","")).lower()
		q2=wordprep(q[2][1]) #ps.stem(q[2][1].replace(" ","")).lower()

		if q1 in hash_index:
			q1_docs=hash_index[q1]
		else:
			q1_docs=[] #in case term couldn't be found in index
			print("first term can't be found")
		if q2 in hash_index:
			q2_docs=hash_index[q2]
		else:
			q2_docs=[] #in case term couldn't be found in index
			print("second term can't be found")
		
		#linear merge with proximity/phrase criteria:
		doclist=[]
		while q1_docs and q2_docs:
			#start in q1 unless q2 has smaller value
			startdoc = q2_docs[0][0] if q1_docs[0][0] > q2_docs[0][0] else q1_docs[0][0]
			#check whether starter is in both lists
			if startdoc == q1_docs[0][0] and startdoc == q2_docs[0][0]:
				#FOR PHRASE SEARCH
				if qtype == "PHRASE": #order matters, prox == 0
					for pos in q1_docs[0][1]:
						if pos+1 in q2_docs[0][1]:
							doclist.append(startdoc) #MATCH!
							break
				#FOR PROXIMITY SEARCH
				elif qtype == "PROX": #order doesn't matter
					match = False
					for pos in q1_docs[0][1]:
						for pos2 in q2_docs[0][1]:
							#pos2 can be in range 
							posrange=range(pos-prox-1,pos+prox+1)
							if pos2 in posrange:
								doclist.append(startdoc) #MATCH!
								match=True
								break
						if match==True:
							break
				#after adding docID (or not) to doclist, remove doc from postinglists
				q1_docs = q1_docs[1:]
				q2_docs = q2_docs[1:]
			elif startdoc == q1_docs[0][0]: #not in q2
				q1_docs = q1_docs[1:]
			elif startdoc == q2_docs[0][0]: #not in q1
				q2_docs = q2_docs[1:]
		# return relevant document IDs (query match)
		return doclist


	# Not boolean search:
	if q[0]=="NOBOOL":
		#simple or proximity/phrase search
		#q[1] e.g. ['PHRASE', 0, ['middle', 'east']]
		result = searchPROX(q[1]) if type(q[1])==list else searchSIMPL(q[1])

	# Boolean search:
	else:
		d1 = searchPROX(q[1]) if type(q[1])==list else searchSIMPL(q[1])
		d2 = searchPROX(q[2]) if type(q[2])==list else searchSIMPL(q[2])

		if q[0]=="AND":
			#relevant documents retrieved for two queries, now apply "AND"
			result = []
			alldocs = d1+d2
			for d in alldocs:
				if (d in d1) and (d in d2) and not(d in result):
					result.append(d)

		elif q[0]=="OR":
			#relevant documents retrieved for two queries, now apply "OR"
			result = d1
			for d in d2:
				if not(d in result):
					result.append(d)

		elif q[0]=="NOT":
			#relevant documents retrieved for two queries, now apply "NOT"
			result = []
			#we want all qdocs[1] without docs listed in qdocs[0]:
			for d in d2:
				if not(d in d1):
					result.append(d)
	return result


def MakeDocIndex(filepath):
	doc_index = {}
	currentkey = 0
	with open(filepath, 'r') as f:
		for line in f:
		  if re.match('ID: [0-9]+',line):
		  	doc_id = re.search("ID: [0-9]+",line).group(0)
		  	currentkey = int(doc_id[4:])
		  	doc_index[currentkey] = [ ]
		  doc_index[currentkey] = doc_index[currentkey] + [line.strip("\n").strip("\r")]
	return doc_index


def GetDocContent(docindex,docIDs):
	contents=[]
	for doc in docIDs:
		document = docindex[int(doc)]
		contents.append(document)
	return contents







