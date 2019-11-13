"""
Create index
Input: document filepath
Output files: indexvar.txt & indexnice.txt, docindexvar.txt
"""

import sys 
import pickle
from timeit import default_timer as timer

#from own files
import fileprep
import tokenize_stem as ts
import indexer

starttime = timer()
filepath = sys.argv[1]

#CREATE INDEX
# list of documents (where documents are lists: ID, HEADLINE, TEXT)
doclist = fileprep.docseparator(filepath)
#tokenize & stem docs -> tokenize_stem.py:
term_docs = []
for doc in doclist:
	doc_id = doc[0]
	head = "".join(doc[1])
	text = "".join(doc[2])
	headline_toks = ts.stem_tokens(ts.removestops(ts.tokenizeText(head)))
	text_toks = ts.stem_tokens(ts.removestops(ts.tokenizeText(text)))
	tdoc=[doc_id,headline_toks,text_toks]
	term_docs.append(tdoc)
print("tokenization, stopping, stemming DONE.")
timestep1 = timer()
print("after "+str(timestep1-starttime)+" seconds.")
##create token file
#with open("tokens.txt", 'w') as f:
#	for doc in term_docs:
#		f.write(str(doc[0])+"\n")
#		f.write(str(doc[1]+doc[2])+"\n")
#create index for docs -> indexer.py
index = indexer.Indexer(term_docs)


#SAVE INDEX VARIABLE for the query search
with open("indexvar.txt",'wb')as f:
	pickle.dump(index,f,protocol=-1)


#SAVE PRINT VERSION OF INDEX for viewing
indexer.PrintIndex2Text(index,"index.txt")

print("Positional inverted index created, find print version: 'index.txt'")
timestep2 = timer()
print("after "+str(timestep2-timestep1)+" seconds.")
##########################################
"""
Extra variable: A simple document index, so when document IDs
matching a query are found, we can also return the actual 
document contents.
"""
#DOCUMENT INDEX:
docindex = indexer.MakeDocIndex(filepath)

#SAVE INDEX VARIABLE for the query search
with open("docindexvar.txt",'wb')as f:
	pickle.dump(docindex,f,protocol=-1)

endtime = timer()
print("All DONE after "+str(endtime-starttime)+" seconds.")
print("You can now run cw1exec.py with your queries.")
