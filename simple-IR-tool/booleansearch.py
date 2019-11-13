"""
Boolean search (called in cw1exec.py)
"""
import querysearch
import outputter


def BooleanSearch(index,querypath,docindex):
	#search queries
	querylist = []
	with open(querypath, 'r') as f:
			for line in f:
				line = line[2:]
				querylist.append(line.strip("\n").strip("\r"))

	#return doc indices & retrieved document contents:
	result_docIDs = []
	result_docs = []
	for i, query in enumerate(querylist):
		print("Query "+str(i+1)+": "+str(query))
		#get docIDs
		docIDs = querysearch.FindDocs(query,index)
		print("Query matches "+str(len(docIDs))+" documents in collection.")
		result_docIDs.append(docIDs)
		#get doc contents
		docs = querysearch.GetDocContent(docindex,docIDs)
		result_docs.append(docs)
		print("\n")

	#print all output to file:
	outfilepath1 = "results.boolean.txt"
	outfilepath2 = "boolquery.resultdocs.txt"
	outputter.ResultsToFile(querylist,result_docIDs,result_docs,outfilepath1,outfilepath2)

	return result_docIDs


