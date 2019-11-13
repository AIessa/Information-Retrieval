import tokenize_stem as ts
import re

# create list where each inner list is a document
def docseparator(filepath):
	doclist = []
	doc = []
	text = []
	headline = []
	with open(filepath, 'r') as f:
		for line in f:
		  if re.match('ID: [0-9]+',line):
		  	doclist.append(doc)
		  	doc = []
		  doc.append(line.strip("\r").strip("\n"))

	doclist = doclist[1:] #remove first empty list

	# split documents into substructure -> text,headline...
	# sublists"HEADLINE:" & "TEXT"
	structured_docs = []
	for doc in doclist:
		doc_id = int(doc[0][4:])
		thisdoc = [doc_id]
		doc_head=[]
		doc_text=[]
		head_over=True
		for line in doc:
			if re.match('^ID: ',line):
				pass
			elif re.match('^HEADLINE: ',line): 
			#if line begins with "HEADLINE: "
				doc_head.append(line.strip("\n").strip("\r")[10:])
				head_over=False
			elif re.match('^TEXT: ',line): 
			#if line begins with "TEXT: ", end headline & start text
				head_over == True
				doc_text.append(line.strip("\n").strip("\r")[6:])
			elif head_over == False: # & (not(re.match('^TEXT: ',line))
			#if headline has been started & text hasn't started
				doc_head.append(line.strip("\n").strip("\r")) #add to headline
			else:
			#if line doesn't begin with headline or text & headline is "over" (or there was none)
				doc_text.append(line.strip("\n").strip("\r"))
		#save structured doc to list:
		structured_docs.append(thisdoc+[doc_head]+[doc_text])

	return structured_docs

