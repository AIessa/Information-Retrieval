"""
main

*****PLEASE RUN cw1createindex.py first, 
if indexvar.py & docindexvar.py are NOT in the directory.

Execute in console:
$ python3 cw1exec.py CW1collection/queries.boolean.txt
$ python3 cw1exec.py CW1collection/queries.ranked.txt


(Simple IR tool)
This is the search execution module that loads the index & allows 
- Boolean search
- Phrase search
- Proximity search
- Ranked IR based on TFIDF
"""

import sys
#import querysearch
import pickle

import rankedsearch as r
import booleansearch as b

querypath = sys.argv[1]
search = 'boolean' if "boolean" in querypath else 'ranked'
print(search+" search.")

# load existing index for document collection
indexfile = open("indexvar.txt","rb")
index = pickle.load(indexfile)

#load existing docindex (to get content of top matching documents)
docindexfile = open("docindexvar.txt","rb")
docindex = pickle.load(docindexfile)
n = len(docindex)#number of documents in collection (for ranked search)

if search == 'boolean':
	output = b.BooleanSearch(index,querypath,docindex)
	print("Results in results.boolean.txt")
	print("You can view the first line of each retrieved document in boolquery.resultdocs.txt")


elif search == 'ranked':
	output = r.RankedSearch(index,querypath,n)
	print("Ranked results in results.ranked.txt (cutoff at 1000 documents)")

