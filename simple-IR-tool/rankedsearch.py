"""
Ranked IR search based on TFIDF (called in cw1exec.py)
"""
import tokenize_stem as ts
import tfidf


def RankedSearch(index,querypath,n):

	#QUERY PROCESSING & TFIDF
	queries = []
	with open(querypath, 'r') as f:
			for line in f:
				query = line.strip("\n").strip("\r")
				query.split(" ")
				query = ts.stem_tokens(ts.removestops(ts.tokenizeText(query)))
				queries.append(query)

	#TFIDF
	resultmatrix = []
	for query in queries:
		result = tfidf.TFIDF(query,index,n)
		print(str(query))
		print(str(len(result))+" documents found. Top 10:")
		for line in result[:10]:
			print(str(line[0])+" 0 "+str(line[2])+" 0 "+str(line[4])+" 0")	
		resultmatrix.append(result)
		print("\n")

	##OUTPUT
	##another output file version:
	#with open("tfidf_results.txt", 'w') as f:
	#	for i, results in enumerate(resultmatrix):
	#		f.write("Query: "+str(queries[i])+"\n")
	#		for line in results[:10]:
	#			f.write(str(line).replace(','," ")+"\n")
	#		f.write("\n")

	with open("results.ranked.txt", 'w') as f:
		for i, results in enumerate(resultmatrix):
			f.write("Query: "+str(queries[i])+"\n")
			if len(results)>1000:
				results = results[:1000]
			for line in results:
				f.write(str(line[0])+" 0 "+str(line[2])+" 0 "+str(line[4])+" 0 \n")
			f.write("\n")

	return resultmatrix
