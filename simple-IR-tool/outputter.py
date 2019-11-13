
def ResultsToFile(querylist,result_docIDs,result_docs,outfilepath1,outfilepath2):
	with open(outfilepath1, 'w') as fil:
		with open(outfilepath2, 'w') as f:
		    for i, q in enumerate(querylist):
		        f.write("Query: "+q+"\n")
		        fil.write("Query: "+q+"\n")
		        fil.write("Matches the following document(s):\n")
			for doc in result_docIDs[i]:
				fil.write(str(i+1)+" 0 "+str(doc)+" 0 1 0\n")
		        f.write("\n"+str(len(result_docIDs[i]))+" match(es) found.\n")
		        f.write("First line of matching document(s):\n\n")
		        for doc in result_docs[i]:
		        	f.write(str(doc[:2]))
		        	f.write("\n")
		        f.write("\n\n")
		        fil.write("\n\n")

