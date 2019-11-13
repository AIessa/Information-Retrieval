"""
- Indexer(term_docs)
- MakeDocIndex(filepath)
- PrintIndex2Text(index,filename)

NOTE: if we want to enable search specifically in head or text,
(there is no query function for this for now), uncomment the part
that includes this info in index.
"""
import re

def Indexer(term_docs):
	#hash posting list: { term : [ (doc,[positions]) ] }
	terms = {}
	for doc in term_docs:
		doc_id = doc[0]
		head = doc[1]
		text = doc[2]
		alltokens = head+text
		## create or update terms "head" & "text" with {term : [doc,[range]]}
		#if not(head ==[]):
		#	if 'struct_head' in terms:
		#		terms['struct_head'] = terms['struct_head']+[(doc_id,[0,len(head)-1])]
		#	else:
		#		terms['struct_head'] = [(doc_id,[0,len(head)-1])]
		#if not(text ==[]):
		#	if 'struct_text' in terms: #fix range!
		#		terms['struct_text'] = terms['struct_text']+[(doc_id,[len(head),len(alltokens)-1])]
		#	else:
		#		terms['struct_text'] = [(doc_id,[len(head),len(alltokens)-1])]
		#add terms from content:
		alltokens = doc[1]+doc[2]
		for pos, t in enumerate(alltokens):
			if not(t in terms):
				terms[t]=[(doc_id,[pos])]
			else:
			# t already in terms, terms[t]=[(id,[pos])]
				if terms[t][len(terms[t])-1][0] == doc_id: #already pointer to doc
					firstups = terms[t][:len(terms[t])-1]
					lastup = terms[t][len(terms[t])-1]
					lastup[1].append(pos)
				else: #new in doc
					firstups = terms[t]
					lastup = (doc_id,[pos])
				
				terms.update({t:firstups+[lastup]})
	return terms

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

def PrintIndex2Text(index,filename):
	with open(filename, 'w') as f:
	    for term in index:
	        f.write(term+":\n")
	        for doc in index[term]:
	        	f.write("        "+str(doc[0])+": "+str(doc[1]).strip('[]')+"\n")

